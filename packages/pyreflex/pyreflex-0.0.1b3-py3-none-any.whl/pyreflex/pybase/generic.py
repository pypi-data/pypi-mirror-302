from typing import Optional
from io import StringIO
import weakref
from .pybase import decref


class SpecializedTypes(dict):
    def __getitem__(self, key):
        return super().__getitem__(key)[0]
    
    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            def finalize():
                _, finalizers = self.pop(key)
                (finalizer.detach() for finalizer in finalizers)
            finalizers = [weakref.finalize(subkey, finalize) for subkey in key]
            return super().__setitem__(key, (value, finalizers))
        else:
            def finalize():
                self.pop(key)
            weakref.finalize(key, finalize)
            return super().__setitem__(key, (value, None))


class Generic:
    __type__: Optional[type]
    __types__: tuple[type, ...]
    
    @classmethod
    def __class_getitem__(cls, typelike):
        specialized_types: dict[type, type] = getattr(cls, '__specialized_types')
        if isinstance(typelike, type):
            decref(typelike)
            inner_name = typelike.__qualname__
            is_multiple = False
        elif isinstance(typelike, tuple):
            inner_name = StringIO()
            length = len(typelike)
            for i, each_type in enumerate(typelike):
                decref(each_type)
                inner_name.write(each_type.__qualname__)
                if i != length - 1:
                    inner_name.write(', ')
            inner_name = inner_name.getvalue()
            is_multiple = True
        else:
            raise TypeError("argument(s) in the '[]' should be type(s)")
        result = specialized_types.get(typelike)
        if result is None:
            class TypedGeneric(cls): ...
            name = f'{cls.__qualname__}[{inner_name}]'
            TypedGeneric.__name__ = name
            TypedGeneric.__qualname__ = name
            if is_multiple:
                TypedGeneric.__types__ = typelike
            else:
                TypedGeneric.__type__ = typelike
            result = TypedGeneric
            specialized_types[typelike] = result
        return result

Generic.__specialized_types = SpecializedTypes()