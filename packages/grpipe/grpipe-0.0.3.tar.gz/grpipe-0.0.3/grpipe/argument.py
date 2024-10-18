from typing import Any, Generic, Optional, TypeVar

from .base import ArgumentError, BaseStep
from .utils import format_value

T = TypeVar("T")


class Argument(BaseStep, Generic[T]):
    """
    Represents an argument that can be bound to a value and passed to a step.

    Methods:
        bind: Bind the argument to a value
        unbind: Unbind the argument
        bound: Check if the argument is bound
        value: Get the value of the argument
    """

    def __init__(self, name: str, *args: Any, **kwargs: Any):
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
        super().__init__(name, *args, **kwargs)
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
