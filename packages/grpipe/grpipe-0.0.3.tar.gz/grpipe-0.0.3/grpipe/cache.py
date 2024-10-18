from collections import OrderedDict
from typing import Any


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
