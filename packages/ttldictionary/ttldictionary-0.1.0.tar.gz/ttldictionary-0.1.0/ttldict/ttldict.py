import time
import json
from typing import Any, Iterable, Optional, Dict


class TTLDict(dict):
    """
    A dictionary subclass that supports Time-To-Live (TTL) for its keys, allowing for automatic expiration of key-value pairs after a specified duration. This class is designed to be semi-transparent to serializers, meaning it can be serialized like a standard dictionary while managing TTL functionality behind the scenes.

    The TTLDict class provides the following methods:

    Methods:
        - set(key: str, value: Any, ttl: Optional[int] = None) -> None:
            Set a key-value pair with an optional TTL (in seconds). If TTL is provided, the key will expire after the specified duration.

        - update(iterable: Iterable) -> None:
            Update the dictionary with key-value pairs from an iterable, automatically cleaning up expired keys before the update.

        - get(key: str, default: Optional[Any] = None) -> Optional[Any]:
            Retrieve the value for a key, returning the default value if the key is expired or not found.

        - purge() -> None:
            Remove all expired keys from the dictionary.

        - __getitem__(key: str) -> Any:
            Override the dictionary item access to automatically clean up expired keys before returning the value.

        - __setitem__(key: str, value: Any) -> None:
            Override the dictionary item assignment to allow setting TTL when using the dict syntax. If a tuple is provided, the second element is treated as the TTL.

        - __contains__(key: str) -> bool:
            Override the membership test to check for expired keys.

        - __repr__() -> str:
            Return a string representation of the TTLDict, similar to a standard dictionary, while ensuring expired keys are cleaned up.

        - __iter__() -> Iterable[str]:
            Return an iterator over the keys, cleaning up expired keys before iteration.

        - __len__() -> int:
            Return the number of valid keys in the dictionary, excluding expired ones.

        - __getstate__() -> Dict[str, Any]:
            Return the state of the object for serialization, ensuring that expired keys are removed before serialization.

    The TTLDict class is useful in scenarios where temporary data storage is required, such as caching, session management, or any situation where data should automatically expire after a certain period.
    """

    def __init__(self) -> None:
        super().__init__()
        self._ttl: Dict[str, float] = {}  # Store TTL values for each key

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a key-value pair with an optional TTL (in seconds)."""
        super().__setitem__(key, value)
        if ttl is not None:
            self._ttl[key] = time.time() + ttl  # Store the expiration time

    def update(self, iterable: Iterable) -> None:
        self._cleanup()
        return super().update(iterable)

    def get(self, key: str, default: Optional[Any] = None) -> Optional[Any]:
        """Get the value for a key, returning default if the key is expired or not found."""
        self._cleanup()
        return super().get(key, default)

    def purge(self) -> None:
        """Purges all expired keys."""
        self._cleanup()

    def __getitem__(self, key: str) -> Any:
        """Override to automatically clean up expired keys."""
        self._cleanup()
        return super().__getitem__(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Override to allow setting TTL when using the dict syntax."""
        if isinstance(value, tuple) and len(value) == 2:
            super().__setitem__(key, value[0])
            self._ttl[key] = time.time() + value[1]
        else:
            super().__setitem__(key, value)
            if key in self._ttl:
                del self._ttl[key]

    def _cleanup(self) -> None:
        """Remove expired keys from the dictionary."""
        current_time = time.time()
        expired_keys = [
            key
            for key, expiration in self._ttl.copy().items()
            if expiration < current_time
        ]
        for key in expired_keys:
            super().pop(key, None)  # Remove from dict
            self._ttl.pop(key, None)  # Remove from TTL tracking

    def __contains__(self, key: str) -> bool:
        """Override to check for expired keys."""
        self._cleanup()
        return super().__contains__(key)

    def __repr__(self) -> str:
        """Return a string representation of the TTLDict, like a normal dict."""
        self._cleanup()
        return super().__repr__()

    def __iter__(self) -> Iterable[str]:
        """Return an iterator over the keys, cleaning up expired keys."""
        self._cleanup()
        return super().__iter__()

    def __len__(self) -> int:
        """Return the number of valid keys."""
        self._cleanup()
        return super().__len__()

    def __getstate__(self) -> Dict[str, Any]:
        """Return the state of the object for serialization."""
        self._cleanup()
        return dict(self)
