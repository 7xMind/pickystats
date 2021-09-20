"""
A Simple input validator to validate input text elements.
"""
import typing


class BaseInputValidator:

    def __init__(self, value: typing.AnyStr):
        self.value = value

    def is_valid_name(self):
        raise NotImplemented

    def is_valid_number(self):
        raise NotImplemented


class InputValidator(BaseInputValidator):

    def is_valid_name(self):
        return isinstance(self.value, str)

    def is_valid_number(self) -> bool:
        try:
            int(self.value)
            return True
        except ValueError:
            return False
