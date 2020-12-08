# Package: poetic (poetic-py)
# Author: Kevin Wang
#
# The MIT License (MIT)
#
# Copyright 2020 Kevin Wang
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
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