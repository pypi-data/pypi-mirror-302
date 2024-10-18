import sys
from collections import defaultdict
from inspect import Parameter, signature
from typing import Any, Callable, Optional

import networkx as nx

from .argument import Argument
from .base import ArgumentError, BaseStep, PipelineError
from .step import Step


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

    def draw(self, params: bool = False) -> str:
        """
        Generate a flowchart of the pipeline using mermaid markdown.

        Args:
            params (bool): Whether to include parameters in the flowchart.

        Returns:
            str: The mermaid markdown representation of the flowchart.
        """
        mermaid = ['%%{init: {"flowchart": {"htmlLabels": false}}}%%\nflowchart TD']
        for step in self.steps.values():
            if isinstance(step, Step):
                step_label = f"{step.name}"
                if params:
                    param_str = "\n".join(f"⚙ {k}={v!s}" for k, v in step.params.items())
                    step_label += f"\n{param_str}"
                mermaid.append(f'{step.name}["{step_label}"]')
                for dep in step.args.values():
                    mermaid.append(f"{dep.name} --> {step.name}")
            elif isinstance(step, Argument):
                mermaid.append(f"{step.name}[({step.name})]")
        return "\n".join(mermaid)

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
            f"{step.name}__{key}": value
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

    def _repr_markdown_(self) -> str:
        return f"```mermaid\n{self.draw(params=False)}\n```"

    def _repr_html_(self) -> str | None:
        if "marimo" in sys.modules:
            html: str = sys.modules["marimo"].mermaid(self.draw(params=False)).text
            return html
        else:
            return None

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

    def __getitem__(self, key: str) -> "Pipeline":
        if key not in self.steps:
            raise PipelineError(key, self.steps)
        ancestor_nodes = nx.ancestors(self.graph, key)
        ancestor_nodes.add(key)
        steps = [self.steps[node] for node in ancestor_nodes]
        return Pipeline(*steps)


def step(
    verbose: bool = False,
    max_cache_size: int = 1000,
    params: dict[str, Any] | None = None,
    **args: Pipeline | Argument,
) -> Callable:
    """
    Decorator to create a pipeline step.

    Args:
        verbose (bool): Whether to enable verbose logging for the step.
        params (dict[str, Any] | None): Parameters for the step.
        max_cache_size (int): Maximum size of the step's cache.

    Returns:
        Callable: A decorator that creates a Pipeline from the decorated function.
    """

    def decorator(function: Callable) -> Pipeline:
        nonlocal args, params

        kwargs = args or {
            key: param.default
            for key, param in signature(function).parameters.items()
            if isinstance(param.default, (Argument, Pipeline))
        }

        parameters = params or {
            key: param.default
            for key, param in signature(function).parameters.items()
            if param.default is not Parameter.empty and not isinstance(param.default, (Argument, Pipeline))
        }

        pipeline_args: dict[str, Step | Argument] = {}
        steps: list[Argument | Step] = []

        for key, val in kwargs.items():
            if isinstance(val, Pipeline):
                steps.extend(val.steps.values())
                pipeline_args[key] = val.output
            if isinstance(val, Argument):
                steps.append(val)
                pipeline_args[key] = val

        steps.append(
            Step(
                function,
                verbose=verbose,
                max_cache_size=max_cache_size,
                args=pipeline_args,
                params=parameters,
            )
        )

        return Pipeline(*steps, verbose=verbose)

    return decorator
