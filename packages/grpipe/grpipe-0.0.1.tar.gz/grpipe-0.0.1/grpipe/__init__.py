import logging
import sys
from collections import OrderedDict, defaultdict
from inspect import Parameter, Signature, signature
from time import perf_counter
from typing import Any, Callable, Generic, Optional, TypeVar

import networkx as nx
import polars as pl
from frozendict import frozendict

T = TypeVar("T")


class ParameterError(ValueError):
    """Exception raised for errors in the parameter."""

    def __init__(self, param_name: str, message: str):
        super().__init__(f"Parameter {param_name}")


class ArgumentError(ValueError):
    """Exception raised for errors in the argument."""

    def __init__(self, expected: Any, got: Any):
        super().__init__(f"Expected {expected}, got {got}")


class PipelineError(ValueError):
    """Exception raised for errors in the pipeline."""

    def __init__(self, expected: Any, got: Any):
        super().__init__(f"Expected {expected}, got {got}")


def custom_hash(value: Any) -> Any:
    """
    Create a custom hash for various data types.

    Args:
        value (Any): The value to be hashed.

    Returns:
        Any: A hashable representation of the input value.
    """
    if isinstance(value, dict):
        return frozendict({k: custom_hash(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple([custom_hash(v) for v in value])
    if isinstance(value, set):
        return frozenset([custom_hash(v) for v in value])
    if isinstance(value, pl.DataFrame):
        if value.height > 1000:
            return value.sample(n=1000, seed=42).hash_rows().sum()
        else:
            return value.hash_rows().sum()
    if isinstance(value, pl.Series):
        return value.hash().sum()
    if isinstance(value, pl.Expr):
        return value.meta.serialize()
    return hash(value)


def format_value(value: Any) -> str:
    """
    Format a value as a string.

    Args:
        value (Any): The value to be formatted.

    Returns:
        str: A string representation of the input value.
    """
    return str(value)


class BaseStep:
    """Base class for all steps in the pipeline."""

    def __init__(self, name: str, cachable: bool = True, verbose: bool = False):
        self.__name = name
        self.__cachable = cachable
        self.__verbose = verbose
        self.logger = logging.getLogger(name)
        if verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def cachable(self) -> bool:
        return self.__cachable

    @property
    def verbose(self) -> bool:
        return self.__verbose

    def set(self, verbose: Optional[bool] = None, cachable: Optional[bool] = None) -> "BaseStep":
        """
        Set the verbose and cachable properties of the step.

        Args:
            verbose (Optional[bool]): If provided, sets the verbose property.
            cachable (Optional[bool]): If provided, sets the cachable property.

        Returns:
            BaseStep: The updated step instance.
        """
        if verbose is not None:
            self.__verbose = verbose
            self.logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        if cachable is not None:
            self.__cachable = cachable
        return self


class Argument(BaseStep, Generic[T]):
    """
    Represents an argument that can be bound to a value and passed to a step.

    Methods:
        bind: Bind the argument to a value
        unbind: Unbind the argument
        bound: Check if the argument is bound
        value: Get the value of the argument
    """

    def __init__(self, *args: Any, **kwargs: Any):
        """Abstract argument object.

        This object is used to pass arguments to steps in a pipeline. It can be bound to a value and passed to a step as a parameter.

        Args:
            name (str): The name of the argument

        Methods:
            bind: Bind the argument to a value
            unbind: Unbind the argument
            bound: Check if the argument is bound
            value: Get the value of the argument
        """
        super().__init__(*args, **kwargs)
        self.__bound = False
        self.__value: Optional[T] = None

    def bind(self, value: T) -> "Argument[T]":
        """
        Bind the argument to a value.

        Args:
            value (T): The value to bind to the argument.

        Returns:
            Argument[T]: The updated argument instance.
        """
        self.logger.debug(f"Bound {self.name} to {format_value(value)}")
        self.__value = value
        self.__bound = True
        return self

    def unbind(self) -> "Argument[T]":
        """
        Unbind the argument, clearing its value.

        Returns:
            Argument[T]: The updated argument instance.
        """
        self.logger.debug(f"Unbound {self.name}")
        self.__value = None
        self.__bound = False
        return self

    @property
    def bound(self) -> bool:
        return self.__bound

    @property
    def value(self) -> T:
        if not self.__bound or self.__value is None:
            raise ArgumentError(self.name, None)
        return self.__value

    def __repr__(self) -> str:
        return f"Argument({self.name})"


class LRUCache:
    """A Least Recently Used (LRU) cache implementation."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: OrderedDict[Any, Any] = OrderedDict()

    def get(self, key: Any) -> Any | None:
        """
        Retrieve a value from the cache.

        Args:
            key (Any): The key to look up.

        Returns:
            Any | None: The value associated with the key, or None if not found.
        """
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Any, value: Any) -> None:
        """
        Add a key-value pair to the cache.

        Args:
            key (Any): The key to add.
            value (Any): The value to associate with the key.
        """
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def __len__(self) -> int:
        return len(self.cache)

    def clear(self) -> None:
        self.cache.clear()


class Step(BaseStep):
    """Represents a step in the pipeline."""

    def __init__(
        self,
        function: Callable[..., T],
        *,
        params: Any = None,
        args: Any = None,
        max_cache_size: int,
        **kwargs: Any,
    ):
        name = function.__name__
        super().__init__(name=name, **kwargs)
        self.__run: Callable[..., T] = function
        self.__args: dict[str, Step | Argument] = {}
        self.__params: dict[str, Any] = {}
        self.__cache_times: list[float] = []
        self.__run_times: list[float] = []

        if args or params:
            self.__args = args
            self.__params = params
        else:  # Try to infer args and params from function signature
            self.__args, self.__params = self.__infer_args_params(signature(self.__run))

        self.cache: LRUCache = LRUCache(max_cache_size)
        self.__signature__ = signature(self.__run).replace(
            parameters=[
                Parameter(key, Parameter.KEYWORD_ONLY, default=val)
                for key, val in self.__args.items()
                if isinstance(val, Argument) and not val.bound
            ]
        )

    def __infer_args_params(self, signature: Signature) -> tuple[dict[str, Any], dict[str, Any]]:
        args, params = {}, {}
        for param in signature.parameters.values():
            if param.default == Parameter.empty:
                raise ParameterError(param.name, self.name)
            if isinstance(param.default, Step | Argument):
                args[param.name] = param.default
            else:
                params[param.name] = param.default

        return args, params

    def is_cachable(self, bound_args: dict[str, Any], kwargs: dict[str, Any]) -> bool:
        """
        Determine if the step's result can be cached based on the given arguments.

        Args:
            bound_args (dict[str, Any]): The bound arguments.
            kwargs (dict[str, Any]): The keyword arguments.

        Returns:
            bool: True if the result can be cached, False otherwise.
        """
        return all(not (not arg.cachable and arg_name not in bound_args) for arg_name, arg in self.__args.items())

    def get_cache_key(self, bound_args: dict[str, Any], kwargs: dict[str, Any]) -> frozendict:
        """
        Generate a cache key based on the given arguments.

        Args:
            bound_args (dict[str, Any]): The bound arguments.
            kwargs (dict[str, Any]): The keyword arguments.

        Returns:
            frozendict: A hashable cache key.
        """
        cache_dict = self.params.copy()
        cache_dict.update(bound_args)
        cache_dict.update(kwargs)
        return frozendict({k: custom_hash(v) for k, v in cache_dict.items()})

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the step with the given arguments.

        Args:
            *args: Positional arguments (not used).
            **kwargs: Keyword arguments for the step.

        Returns:
            Any: The result of executing the step.
        """
        if args:
            raise ArgumentError(0, f"{len(args)} positional arguments")
        bound_args = {k: v.value for k, v in self.args.items() if isinstance(v, Argument) and v.bound}
        if set(kwargs.keys()) != set(self.args.keys()) - set(bound_args.keys()):
            raise ArgumentError(
                set(self.args.keys()) - set(bound_args.keys()),
                set(kwargs.keys()),
            )

        is_cachable = self.is_cachable(bound_args, kwargs)

        joined_args = self.format_args(**kwargs, **self.params)

        if is_cachable:
            t0 = perf_counter()
            cache_key = self.get_cache_key(bound_args, kwargs)
            t1 = perf_counter()
            self.__cache_times.append(t1 - t0)

            cached_result = self.cache.get(cache_key)
            if cached_result is not None:
                self.logger.debug(
                    f"[{self.__cache_times[-1]:.4f}] Returning cached value {self.name}({joined_args}) = {cached_result}"
                )
                return cached_result

        t0 = perf_counter()
        result = self.__run(**bound_args, **self.params, **kwargs)
        t1 = perf_counter()
        self.__run_times.append(t1 - t0)

        if is_cachable:
            self.cache.put(cache_key, result)
            self.logger.debug(f"[{self.__run_times[-1]:.4f}] Added {self.name}({joined_args}) = {result} to cache")
        else:
            self.logger.debug(
                f"[{self.__run_times[-1]:.4f}] Executed {self.name}({joined_args}) = {result} (not cached)"
            )

        return result

    def reset_cache(self) -> None:
        """Clear the step's cache."""
        self.cache.clear()

    @property
    def params(self) -> dict[str, Any]:
        return self.__params

    def set_params(self, **kwargs: Any) -> "Step":
        """
        Set the parameters for the step.

        Args:
            **kwargs: The parameters to set.

        Returns:
            Step: The updated step instance.
        """
        change = False
        for key, value in kwargs.items():
            if key not in self.params:
                raise ParameterError(key, self.name)
            if self.params[key] != value:
                self.__params[key] = value
                change = True
        if change:
            self.logger.debug(f"Updated parameters {kwargs}")
        return self

    @property
    def args(self) -> dict[str, Any]:
        return self.__args

    def format_args(self, **kwargs: Any) -> str:
        return ", ".join([f"{key}={format_value(value)}" for key, value in kwargs.items()])

    def __repr__(self) -> str:
        return f"{self.name}({self.format_args(**self.args)})"


class Pipeline(BaseStep):
    """Represents a pipeline of steps."""

    def __init__(self, *steps: Step | Argument, **kwargs: Any):
        super().__init__(name="pipeline", cachable=False, **kwargs)
        self.__steps: dict[str, Step | Argument] = {step.name: step for step in steps}

        graph, output_nodes, args = self.__build_graph(*steps)

        self.__graph = graph
        self.__args = {arg: self.__steps[arg] for arg in args}

        if len(output_nodes) != 1 or not isinstance(self.steps[output_nodes[0]], Step):
            raise PipelineError("1", output_nodes)
        self.__output = output_nodes[0]

    def __build_graph(self, *steps: Step | Argument) -> tuple[nx.DiGraph, list[str], list[str]]:
        """
        Build a graph representation of the pipeline.

        Args:
            *steps: The steps in the pipeline.

        Returns:
            tuple[nx.DiGraph, list[str], list[str]]: The graph, output nodes, and argument nodes.
        """
        graph: nx.DiGraph = nx.DiGraph()

        for step in steps:
            if step.name not in graph:
                graph.add_node(step.name, kind="step" if isinstance(step, Step) else "arg")
        for step in steps:
            if isinstance(step, Argument):
                continue
            for dep in step.args.values():
                if dep.name in self.__steps:
                    graph.add_edge(dep.name, step.name)

        output_nodes = [node for node in graph.nodes if graph.out_degree[node] == 0]

        args = [node for node, data in graph.nodes(data=True) if data["kind"] == "arg"]

        return graph, output_nodes, args

    def draw(self) -> None:
        """Draw a visual representation of the pipeline graph."""
        nx.draw(self.graph, with_labels=True)

    def bind(self, **kwargs: Any) -> "Pipeline":
        """
        Bind values to arguments in the pipeline.

        Args:
            **kwargs: The values to bind to arguments.

        Returns:
            Pipeline: The updated pipeline instance.
        """
        for name, value in kwargs.items():
            if name not in self.args:
                raise PipelineError("Argument", name)
            step = self.args[name]
            if not isinstance(step, Argument):
                raise PipelineError("Argument", type(step))
            step.bind(value)
            for child in nx.descendants(self.graph, step.name):
                child_step = self.steps[child]
                if isinstance(child_step, Step):
                    child_step.reset_cache()
        return self

    def unbind(self, *args: str) -> "Pipeline":
        """
        Unbind values from arguments in the pipeline.

        Args:
            *args: The names of arguments to unbind.

        Returns:
            Pipeline: The updated pipeline instance.
        """
        for name in args:
            if name not in self.args:
                raise PipelineError("Argument", name)
            step = self.args[name]
            if not isinstance(step, Argument):
                raise PipelineError("Argument", type(step))
            step.unbind()
            for child in nx.descendants(self.graph, step.name):
                child_step = self.steps[child]
                if isinstance(child_step, Step):
                    child_step.reset_cache()
        return self

    @property
    def graph(self) -> nx.DiGraph:
        return self.__graph

    @property
    def steps(self) -> dict[str, Step | Argument]:
        return self.__steps

    @property
    def args(self) -> dict[str, Argument | Step]:
        return self.__args

    @property
    def output(self) -> Step:
        step = self.steps[self.__output]
        if not isinstance(step, Step):
            raise PipelineError("Step", type(step))
        return step

    @property
    def params(self) -> dict[str, Any]:
        return {
            f"{step}__{key}": value
            for step in self.steps.values()
            if isinstance(step, Step)
            for key, value in step.params.items()
        }

    def set_params(self, **kwargs: Any) -> "Pipeline":
        """
        Set parameters for steps in the pipeline.

        Args:
            **kwargs: The parameters to set, in the format "step__param".

        Returns:
            Pipeline: The updated pipeline instance.
        """
        step_params: Any = defaultdict(dict)
        for k, v in kwargs.items():
            step, param = k.split("__", 1)
            step_params[step][param] = v
        for step, params in step_params.items():
            if step not in self.steps:
                raise PipelineError(self.steps, step)
            child = self.steps[step]
            if not isinstance(child, Step):
                raise PipelineError("Step", type(child))
            child.set_params(**params)
        return self

    def set(self, verbose: Optional[bool] = None, cachable: Optional[bool] = False) -> "Pipeline":
        """
        Set the verbose and cachable properties for all steps in the pipeline.

        Args:
            verbose (Optional[bool]): If provided, sets the verbose property.
            cachable (Optional[bool]): If provided, sets the cachable property.

        Returns:
            Pipeline: The updated pipeline instance.
        """
        super().set(verbose=verbose, cachable=cachable)
        for step in self.steps.values():
            step.set(verbose=verbose)
        return self

    def __repr__(self) -> str:
        args = ", ".join([k for k, v in self.args.items() if not (isinstance(v, Argument) and v.bound)])
        return f"Pipeline({args})"

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Execute the pipeline with the given arguments.

        Args:
            *args: Positional arguments (not used).
            **kwargs: Keyword arguments for the pipeline.

        Returns:
            Any: The result of executing the pipeline.
        """
        bound_args = {k: v.value for k, v in self.args.items() if isinstance(v, Argument) and v.bound}
        if args:
            raise ArgumentError(0, f"{len(args)} positional arguments")
        if set(kwargs.keys()) != set(self.args.keys()) - set(bound_args.keys()):
            raise ArgumentError(
                set(self.args.keys()) - set(bound_args.keys()),
                set(kwargs.keys()),
            )
        results: dict[str, Any] = kwargs | bound_args
        remaining_steps: set[Step] = {x for x in self.steps.values() if isinstance(x, Step)}

        while remaining_steps:
            for step in list(remaining_steps):
                if all(dep.name in results for dep in step.args.values()):
                    step_args = {k: results[v.name] for k, v in step.args.items() if v.name not in bound_args}
                    results[step.name] = step(**step_args)
                    remaining_steps.remove(step)
        return results[self.output.name]


def step(  # noqa: C901
    verbose: bool = False,
    args: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    max_cache_size: int = 1000,
) -> Callable:
    """
    Decorator to create a pipeline step.

    Args:
        verbose (bool): Whether to enable verbose logging for the step.
        args (dict[str, Any] | None): Arguments for the step.
        params (dict[str, Any] | None): Parameters for the step.
        max_cache_size (int): Maximum size of the step's cache.

    Returns:
        Callable: A decorator that creates a Pipeline from the decorated function.
    """

    def decorator(function: Callable) -> Pipeline:
        nonlocal args, params
        steps: list[Argument | Step] = []
        if not args:
            args = {}
            for key, param in signature(function).parameters.items():
                if isinstance(param.default, (Argument, Pipeline)):
                    args[key] = param.default
        if not params:
            params = {}
            for key, param in signature(function).parameters.items():
                if param.default != Parameter.empty and key not in args:
                    params[key] = param.default

        for key in args:
            if isinstance(args[key], Pipeline):
                steps.extend(args[key].steps.values())
                args[key] = args[key].output
            if isinstance(args[key], Argument):
                steps.append(args[key])

        steps.append(
            Step(
                function,
                verbose=verbose,
                max_cache_size=max_cache_size,
                args=args,
                params=params,
            )
        )

        return Pipeline(*steps, verbose=verbose)

    return decorator


if __name__ == "__main__":
    pass
