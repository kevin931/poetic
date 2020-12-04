from poetic import exceptions

from io import StringIO
import sys

class TestExceptions():
    
    def test_input_length_error_default_message(self):      
        try:
            raise exceptions.InputLengthError()
        except exceptions.InputLengthError as e:
            message = str(e)
        else:
            assert False
            
        expected = "The current length is unsupported or out of bound."
        assert expected in message
        
        
    def test_unsupported_config_message(self):
        
        try:
            raise exceptions.UnsupportedConfigError()
        except exceptions.UnsupportedConfigError as e:
            message = str(e)
        else:
            assert False
            
        expected = "Unsupported configuration: Please refer to docummentation."
        assert expected in message