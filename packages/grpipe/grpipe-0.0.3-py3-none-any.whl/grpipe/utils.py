from typing import Any

import numpy as np
import pandas as pd
import polars as pl
import xxhash
from frozendict import frozendict


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
    if isinstance(value, np.ndarray):
        return xxhash.xxh32(value.tobytes(), seed=42).hexdigest()
    if isinstance(value, (pd.DataFrame, pd.Series)):
        return xxhash.xxh32(value.to_numpy().tobytes(), seed=42).hexdigest()
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
