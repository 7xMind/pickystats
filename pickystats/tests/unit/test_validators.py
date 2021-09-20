from ...validators import InputValidator

class TestValidators:

    def test_validator_validates_name_correctly(self):
        """
        Given a name as string
        When is_valid_name is called
        True must be returned
        """
        instance = InputValidator('sample_name')
        assert instance.is_valid_name() is True

    def test_num_validator_returns_false_for_strings(self):
        instance = InputValidator('not a number')
        assert instance.is_valid_number() is False