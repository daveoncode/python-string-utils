# -*- coding: utf-8 -*-


class InvalidInputError(TypeError):
    def __init__(self, input_data):
        """
        Custom error used when received object is not a string as expected.

        :param input_data: Any received object
        """
        type_name = type(input_data).__name__
        msg = 'Expected "str", received "{}"'.format(type_name)
        super().__init__(msg)
