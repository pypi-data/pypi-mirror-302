from typing import Optional
from io import StringIO
import weakref
from .pybase import decref


# class SpecializedTypes(dict):
#     def get(self, key):
#         if not isinstance(key, tuple):
#             key = (key,)
#         item = super().get(key)
#         if item is not None:
#             item = item[0]
#         return item
    
#     def __getitem__(self, key):
#         if not isinstance(key, tuple):
#             key = (key,)
#         return super().__getitem__(key)[0]
    
#     def __setitem__(self, key, value):
#         if isinstance(key, tuple):
#             def finalize():
#                 _, finalizers = self.pop(key)
#                 (finalizer.detach() for finalizer in finalizers)
#             finalizers = [weakref.finalize(subkey, finalize) for subkey in key]
#             return super().__setitem__(key, (value, finalizers))
#         else:
#             tuple_key = (key,)
#             def finalize():
#                 self.pop(tuple_key)
#             weakref.finalize(key, finalize)
#             return super().__setitem__(tuple_key, (value, None))


class SpecializedTypes(dict):
    def get(self, key):
        if isinstance(key, tuple):
            weakkey = (weakref.ref(each) for each in key)
        else:
            weakkey = weakref.ref(key)
        item = super().get(weakkey)
        if item is not None:
            item = item[0]
        return item
    
    def __getitem__(self, key):
        if isinstance(key, tuple):
            weakkey = (weakref.ref(each) for each in key)
        else:
            weakkey = weakref.ref(key)
        return super().__getitem__(weakkey)[0]
    
    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            weakkey = (weakref.ref(each) for each in key)
            def finalize():
                _, finalizers = self.pop(weakkey)
                (finalizer.detach() for finalizer in finalizers)
            finalizers = [weakref.finalize(subkey, finalize) for subkey in key]
            return super().__setitem__(weakkey, (value, finalizers))
        else:
            weakkey = weakref.ref(key)
            def finalize():
                self.pop(weakkey)
            weakref.finalize(key, finalize)
            return super().__setitem__(weakkey, (value, None))


class generic:
    __type__: Optional[type]
    __types__: tuple[type, ...]
    
    @classmethod
    def __class_getitem__(cls, typelike):
        specialized_types: dict[type, type] = getattr(cls, '__specialized_types')
        result = specialized_types.get(typelike)
        if isinstance(result, weakref.ReferenceType):
            result = result()
        if result is None:
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
            class TypedGeneric(cls): ...
            name = f'{cls.__qualname__}[{inner_name}]'
            TypedGeneric.__name__ = name
            TypedGeneric.__qualname__ = name
            if is_multiple:
                TypedGeneric.__types__ = typelike
            else:
                TypedGeneric.__type__ = typelike
            result = TypedGeneric
            specialized_types[typelike] = weakref.ref(result)
        return result

generic.__specialized_types = SpecializedTypes()