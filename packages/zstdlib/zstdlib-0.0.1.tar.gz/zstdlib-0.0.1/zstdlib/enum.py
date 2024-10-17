# pylint: disable=bad-mcs-method-argument,bad-mcs-classmethod-argument
class UEnum(type):
    """
    Metaclass for non-instantiable Enum classes with unique values
    These 'Enum' classes may not be modified after creation
    """

    def __new__(mcls, name, bases, attrs, **kwargs):
        def _ni(*_, **__):
            raise NotImplementedError("Cannot instantiate this class")

        # Disallow instantiation
        for bad in ("__init__", "__new__"):
            if bad in attrs:
                raise ValueError("Cannot define __init__ or __new__")
            attrs[bad] = _ni
        # Disallow duplicate values
        values = set()
        for v in (k for i, k in attrs.items() if not i.startswith("__")):
            if v in values:
                raise ValueError(f"Duplicate value: {v}")
            values.add(v)
        # Construct class
        return type.__new__(mcls, name, bases, attrs, **kwargs)

    # Disallow modification

    def __delattr__(self, *_):
        raise AttributeError("This class cannot be modified")

    def __setattr__(self, *_):
        raise AttributeError("This class cannot be modified")
