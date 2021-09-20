"""
Main module that parses and normalizes the input text file.

Assumptions:
    - Generally, the input file contains pairs of names and working minutes.
    - Elements of the text file are comma-separated.
    - If lowered-cased, identical names would refer to the same person.
"""
import typing
from collections import defaultdict

from striprtf.striprtf import rtf_to_text

# For direct testing
if not __package__:
    from validators import InputValidator
else:
    from .validators import InputValidator


class BaseParser:

    def __init__(self, textfile: str, input_validator: InputValidator = None):
        # Just in case the uploaded file is rtf.
        self.textfile = rtf_to_text(textfile)
        self.validator = input_validator or InputValidator
        self.invalid_items = []

    def get_normalized_items(self) -> typing.Dict[str, list]:
        raise NotImplemented


class BasicParser(BaseParser):
    """
    This module provides basic parsing and normalization functionalities.
    """

    def get_normalized_items(self) -> typing.Dict[str, list]:
        """
        returns list of normalized items:
        :return:
        """
        valid_raw_items = self.get_valid_raw_items()
        final_normalized_items = defaultdict(list)
        for name, time_in_minute in valid_raw_items:
            # Aggregating all the time that belong to the same person
            normalized_name = self._get_normalized_name(name)
            normalized_minute = self._get_normalized_minute(time_in_minute)
            final_normalized_items[normalized_name].append(normalized_minute)
        return final_normalized_items

    def get_valid_raw_items(self):
        """
        Loads all items seperated by `,`
        :return: typing.List[typing.Tuple[str: float]]
        """
        raw_items = self.textfile.split(',')
        valid_raw_items = []
        for item in raw_items:
            try:
                name, working_time_in_minutes = item.split(':')
            # if spliting by `:` returns less or more than two values,
            # it means the item does not to conform to our assumption
            # that our data is in the format of `name:minute`. We keep
            # list of these items to inform the user
            except ValueError:
                self.invalid_items.append(item)
            else:
                if self._name_and_time_are_valid(name=name, time=working_time_in_minutes):
                    valid_raw_items.append((name, working_time_in_minutes))
                else:
                    self.invalid_items.append(item)
        return valid_raw_items

    def _name_and_time_are_valid(self, *, name, time):
        return self.validator(name).is_valid_name() and self.validator(time).is_valid_number()

    def _get_normalized_name(self, name) -> str:
        return name.strip().title()

    def _get_normalized_minute(self, number: float):
        return abs(float(number))


if __name__ == '__main__':
    with open('sample.rtf', 'r') as f:
        ff = f.read()

    ins = BasicParser(textfile=ff)
    print(ins.get_normalized_items())