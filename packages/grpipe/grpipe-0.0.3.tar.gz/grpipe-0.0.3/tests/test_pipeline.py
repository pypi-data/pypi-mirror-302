from typing import Any

import numpy as np
import pandas as pd
import polars as pl
import pytest

from grpipe import Argument, step


def test_basic() -> None:
    x: Argument = Argument("x", cachable=False)
    y: Argument = Argument("y", cachable=False)

    @step(verbose=False, x=x, y=y)
    def test(x: int, y: int, operation: str = "add") -> Any:
        if operation == "add":
            return x + y
        elif operation == "sub":
            return x - y
        else:
            return 0

    @step(verbose=False, x=test)
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

    @step(verbose=True, a=a, b=b)
    def add_dataframes(a: pd.DataFrame, b: pd.DataFrame) -> pd.DataFrame:
        return a + b

    @step(verbose=True, a=a, b=b)
    def add_polars_dataframes(a: pl.DataFrame, b: pl.DataFrame) -> pl.DataFrame:
        return a + b

    @step(verbose=True, a=a, b=b)
    def add_numpy_arrays(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return a + b

    @step(verbose=True, result=add_dataframes)
    def multiply_dataframe(result: pd.DataFrame) -> pd.DataFrame:
        return result * 2

    @step(verbose=True, result=add_polars_dataframes)
    def multiply_polars_dataframe(result: pl.DataFrame) -> pl.DataFrame:
        return result * 2

    @step(verbose=True, result=add_numpy_arrays)
    def multiply_numpy_array(result: np.ndarray) -> np.ndarray:
        return result * 2

    with pytest.raises(ValueError):
        multiply_dataframe()

    with pytest.raises(ValueError):
        multiply_dataframe(1)

    with pytest.raises(ValueError):
        multiply_dataframe(1, 2)

    with pytest.raises(ValueError):
        multiply_dataframe(result=1)

    with pytest.raises(ValueError):
        multiply_dataframe(a=1)

    with pytest.raises(ValueError):
        multiply_dataframe(b=1)

    multiply_dataframe.bind(a=pd.DataFrame({"a": [1, 2, 3]}), b=pd.DataFrame({"a": [4, 5, 6]}))
    assert multiply_dataframe().equals(pd.DataFrame({"a": [10, 14, 18]}))

    multiply_polars_dataframe.bind(a=pl.DataFrame({"a": [1, 2, 3]}), b=pl.DataFrame({"a": [4, 5, 6]}))
    assert multiply_polars_dataframe().equals(pl.DataFrame({"a": [10, 14, 18]}))

    multiply_numpy_array.bind(a=np.array([1, 2, 3]), b=np.array([4, 5, 6]))
    assert np.array_equal(multiply_numpy_array(), np.array([10, 14, 18]))


def test_realistic() -> None:
    df1: Argument = Argument("df1", cachable=True)
    df2: Argument = Argument("df2", cachable=True)
    arr1: Argument = Argument("arr1", cachable=True)
    arr2: Argument = Argument("arr2", cachable=True)

    @step(verbose=True, df1=df1, df2=df2)
    def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, on: str = "id") -> pd.DataFrame:
        return pd.merge(df1, df2, on=on)

    @step(verbose=True, arr1=arr1, arr2=arr2)
    def concatenate_arrays(arr1: np.ndarray, arr2: np.ndarray, axis: int = 0) -> np.ndarray:
        return np.concatenate((arr1, arr2), axis=axis)

    @step(verbose=True, df=merge_dataframes)
    def calculate_mean(df: pd.DataFrame, column: str = "value1") -> float:
        return df[column].mean()

    @step(verbose=True, arr=concatenate_arrays)
    def calculate_sum(arr: np.ndarray) -> float:
        return np.sum(arr)

    df1.bind(pd.DataFrame({"id": [1, 2, 3], "value1": [10, 20, 30]}))
    df2.bind(pd.DataFrame({"id": [1, 2, 3], "value2": [100, 200, 300]}))
    arr1.bind(np.array([1, 2, 3]))
    arr2.bind(np.array([4, 5, 6]))

    assert merge_dataframes().equals(
        pd.DataFrame({
            "id": [1, 2, 3],
            "value1": [10, 20, 30],
            "value2": [100, 200, 300],
        })
    )
    assert np.array_equal(concatenate_arrays(), np.array([1, 2, 3, 4, 5, 6]))
    assert calculate_mean() == 20.0
    assert calculate_sum() == 21.0
