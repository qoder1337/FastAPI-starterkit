from typing import Any, Type


class SingletonMeta(type):
    """
    thread-safe Implementation: Singleton-Pattern
    """

    _instances: dict[Type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
