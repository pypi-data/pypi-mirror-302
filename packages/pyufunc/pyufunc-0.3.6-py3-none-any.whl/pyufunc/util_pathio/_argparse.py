# -*- coding:utf-8 -*-
##############################################################
# Created Date: Sunday, July 9th 2023
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import argparse
import inspect
import functools


def with_argparse(func_or_class):
    @functools.wraps(func_or_class)
    def wrapper(*args, **kwargs):
        parser = argparse.ArgumentParser(description=func_or_class.__doc__)

        # Check if we are dealing with a class
        if inspect.isclass(func_or_class):
            cls = func_or_class
            init_sig = inspect.signature(cls.__init__)
            main_method = getattr(cls, 'main', None)
            if not main_method:
                raise ValueError(
                    "Class must have a 'main' method to use with_argparse.")
            main_sig = inspect.signature(main_method)

            # Skip 'self'
            for name, param in list(init_sig.parameters.items())[1:]:
                parser.add_argument(f'--{name}', type=param.annotation if param.annotation !=
                                    inspect._empty else str, required=param.default == inspect._empty)

            # Skip 'self'
            for name, param in list(main_sig.parameters.items())[1:]:
                parser.add_argument(f'--{name}', type=param.annotation if param.annotation !=
                                    inspect._empty else str, required=param.default == inspect._empty)

            parsed_args = parser.parse_args()
            init_args = {name: getattr(parsed_args, name) for name in list(
                init_sig.parameters.keys())[1:]}  # Skip 'self'
            main_args = {name: getattr(parsed_args, name) for name in list(
                main_sig.parameters.keys())[1:]}  # Skip 'self'

            instance = cls(**init_args)
            return instance.main(**main_args)

        # Otherwise, we are dealing with a function
        else:
            func = func_or_class
            sig = inspect.signature(func)
            for name, param in sig.parameters.items():
                parser.add_argument(f'--{name}', type=param.annotation if param.annotation !=
                                    inspect._empty else str, required=param.default == inspect._empty)

            parsed_args = parser.parse_args()
            func_args = {name: getattr(parsed_args, name)
                         for name in sig.parameters.keys()}

            return func(**func_args)

    # Automatically handle execution if the script is run directly
    if __name__ == "__main__":
        wrapper()

    return wrapper


# @with_argparse
# def example_function(name: str, age: int = 30):
#     """Example function that prints name and age."""
#     print(f'Name: {name}, Age: {age}')
#     return None

# @with_argparse
# class NewClass:
#     """New class with __init__ and main methods."""
#
#     def __init__(self, name: str):
#         self.name = name
#
#     def main(self, age: int = 30):
#         print(f'Name: {self.name}, Age: {age}')

#
# if __name__ == "__main__":
#     # This will execute the function or class based on command-line arguments
#     import sys
#     if len(sys.argv) > 1:
#         script_name = sys.argv[1]
#         sys.argv = sys.argv[1:]
#         if script_name == "example_function":
#             example_function()
#         elif script_name == "ExampleClass":
#             print("Class not implemented yet.")

# How to run this code?
# python _argparse.py example_function --name "John" --age 25
