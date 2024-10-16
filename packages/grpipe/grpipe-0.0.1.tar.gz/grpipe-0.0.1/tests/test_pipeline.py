from typing import Any

import pytest

from grpipe import Argument, step


def test_basic() -> None:
    x: Argument = Argument("x", cachable=False)
    y: Argument = Argument("y", cachable=False)

    @step(verbose=False, args={"x": x, "y": y})
    def test(x: int, y: int, operation: str = "add") -> Any:
        if operation == "add":
            return x + y
        elif operation == "sub":
            return x - y
        else:
            return 0

    @step(verbose=False, args={"x": test})
    def double(x: int) -> int:
        return x * 2

    with pytest.raises(ValueError):
        double()

    with pytest.raises(ValueError):
        double(1)

    with pytest.raises(ValueError):
        double(1, 2)

    with pytest.raises(ValueError):
        double(x=1)

    with pytest.raises(ValueError):
        double(y=1)

    with pytest.raises(ValueError):
        double(x=1, y=2, operation="add")

    with pytest.raises(ValueError):
        double.set_params(test=42)

    with pytest.raises(ValueError):
        double.set_params(x=42)

    with pytest.raises(ValueError):
        double.bind(z=7)

    double.bind(x=1)

    with pytest.raises(ValueError):
        double(x=2, y=3)

    assert double(y=2) == 6


def test_advanced() -> None:
    a: Argument = Argument("a", cachable=True)
    b: Argument = Argument("b", cachable=True)

    @step(verbose=True, args={"a": a, "b": b})
    def multiply(a: int, b: int) -> int:
        return a * b

    @step(verbose=True, args={"result": multiply})
    def square(result: int) -> int:
        return result**2

    with pytest.raises(ValueError):
        square()

    with pytest.raises(ValueError):
        square(1)

    with pytest.raises(ValueError):
        square(1, 2)

    with pytest.raises(ValueError):
        square(result=1)

    with pytest.raises(ValueError):
        square(a=1)

    with pytest.raises(ValueError):
        square(b=1)

    square.bind(a=1, b=2)

    assert square() == 4
