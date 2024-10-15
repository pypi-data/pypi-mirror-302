import typing
from typing import get_origin, get_args, Union
# from store_functions.store_generic_functions import convert_custom_key

class Pointer:
    def __init__(self, **kwargs):

        # self.args_list = kwargs
        # for key in args:
        #     setattr(self, key, None)
        # # `for key in args:
        # #     setattr(self, key)`

        for key, value in kwargs.items():
            # print(value[0].store_namespace)
            setattr(self, key, [value[0].store_namespace, value[1]])

    # def __repr__(self):
    #     return str(self.__dict__)
    
    def __str__(self):
        return str(self.__dict__)
    
    def serialize(self):
        return self.__dict__

class Schema:
    def __init__(self, **kwargs):
        hints = typing.get_type_hints(self.__class__)
        for key, value in kwargs.items():
            setattr(self, key, value)
        for attribute in hints:
            if not hasattr(self, attribute):
                setattr(self, attribute, None)
        self.validate_types()

    def __repr__(self):
        return str(self.__dict__)
    
    def __str__(self):
        return str(self.__dict__)
    
    def serialize(self):
        # l = []
        # hold_pointers = []
        # for each, v in self.__dict__.items():
        #     if isinstance(v, Pointer):
        #         l.append(each)
        #         hold_pointers.append({each: v.args_list})
        # d = self.__dict__
        # for each in l:
        #     d.pop(each)

        if hasattr(self, "pointers"):
            self.pointers = self.pointers.serialize()
            for k, v in self.pointers.items():
                if v[1].isdigit():
                    # print(v[0].store_namespace)
                    self.pointers[k] = [v[0].store_namespace, str(v[1])]
                # else:
                #     self.pointers[k] = convert_custom_key(v)

        return self.__dict__

    def validate_types(self):
        hints = typing.get_type_hints(self.__class__)
        for attribute, expected_type in hints.items():
            actual_value = getattr(self, attribute)
            
            origin = get_origin(expected_type)


            if origin is Union:

                expected_types = get_args(expected_type)
                if not isinstance(actual_value, expected_types) and actual_value is not None:
                    raise TypeError(
                        f"Attribute '{attribute}' should be one of types {expected_types}, "
                        f"but got '{type(actual_value).__name__}'"
                    )
                                
            elif origin is Pointer:
                if not isinstance(actual_value, Pointer) and actual_value is not None:
                    raise TypeError(
                        f"Attribute '{attribute}' should be of type '{expected_type.__name__}', "
                        f"but got '{type(actual_value).__name__}'"
                    )

            elif origin is None:
                if not isinstance(actual_value, expected_type) and actual_value is not None:
                    raise TypeError(
                        f"Attribute '{attribute}' should be of type '{expected_type.__name__}', "
                        f"but got '{type(actual_value).__name__}'"
                    )
            else:
                if not isinstance(actual_value, origin) and actual_value is not None:
                    raise TypeError(
                        f"Attribute '{attribute}' should be of type '{expected_type}', "
                        f"but got '{type(actual_value).__name__}'"
                    )