from threading import Condition
from typing import Any


class Singleton(type):
    """
    A thread-safe singleton metaclass
    """

    _seen: set[type] = (
        set()
    )  # Objects in this have been seen by singleton before and should not be constructed again
    _instances: dict[type, Any] = {}  # Fully constructed singleton objects
    _lock = Condition()

    def __call__(cls, *args, **kwargs):
        # If the object has been seen before, wait for it to be available then return it
        with cls._lock:
            if cls in cls._seen:
                cls._lock.wait_for(lambda: cls in cls._instances)
                return cls._instances[cls]
            cls._seen.add(cls)
        # The object has not been constructed before, create it outside of any lock to avoid delays
        obj = super().__call__(*args, **kwargs)
        with cls._lock:
            cls._instances[cls] = obj
            cls._lock.notify_all()  # Notify other threads of the new object
            return obj
