from inspect import Parameter, Signature, signature
from time import perf_counter
from typing import Any, Callable

from frozendict import frozendict

from .argument import Argument
from .base import ArgumentError, BaseStep, ParameterError
from .cache import LRUCache
from .utils import custom_hash, format_value


class Step(BaseStep):
    """Represents a step in the pipeline."""

    def __init__(
        self,
        function: Callable[..., Any],
        *,
        params: Any = None,
        args: Any = None,
        max_cache_size: int,
        **kwargs: Any,
    ):
        name = function.__name__
        super().__init__(name=name, **kwargs)
        self.__run: Callable[..., Any] = function
        self.__args: dict[str, Step | Argument] = {}
        self.__params: dict[str, Any] = {}
        self.__cache_times: list[float] = []
        self.__run_times: list[float] = []

        self.__args = args or self.__infer_args(signature(self.__run))
        self.__params = params or self.__infer_params(signature(self.__run))

        self.cache: LRUCache = LRUCache(max_cache_size)
        self.__signature__ = signature(self.__run).replace(
            parameters=[
                Parameter(key, Parameter.KEYWORD_ONLY, default=val)
                for key, val in self.__args.items()
                if isinstance(val, Argument) and not val.bound
            ]
        )

    def __infer_args(self, signature: Signature) -> dict[str, Any]:
        args = {}
        for param in signature.parameters.values():
            if isinstance(param.default, (Step, Argument)):
                args[param.name] = param.default

        return args

    def __infer_params(self, signature: Signature) -> dict[str, Any]:
        params = {}
        for key, param in signature.parameters.items():
            if key in self.args:  # Skip bound arguments
                continue
            if param.default is Parameter.empty:
                raise ParameterError(param.name, self.name)
            params[param.name] = param.default

        return params

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
