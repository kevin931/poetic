from poetic import exceptions


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
        
        
    def test_input_length_errror_inheritance(self):
        try:
            raise exceptions.InputLengthError()
        except exceptions.InputLengthError as e:
            assert isinstance(e, Exception)
        else:
            assert False
            
              
    def test_unsupported_config_message(self):
        
        try:
            raise exceptions.UnsupportedConfigError()
        except exceptions.UnsupportedConfigError as e:
            message = str(e)
        else:
            assert False
            
        expected = "Unsupported configuration: Please refer to docummentation."
        assert expected in message
        
    
    def test_unsupported_config_inheritance(self):
        try:
            raise exceptions.UnsupportedConfigError()
        except exceptions.UnsupportedConfigError as e:
            assert isinstance(e, Exception)
        else:
            assert False