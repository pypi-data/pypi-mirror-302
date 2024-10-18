import logging
import sys
from typing import Any, Optional


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
