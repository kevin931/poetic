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
import pytest


class TestExceptions():
    
    @pytest.mark.parametrize("error_class, expected",
                            [(exceptions.InputLengthError, "The current length is unsupported or out of bound."), 
                             (exceptions.UnsupportedConfigError, "Unsupported configuration: Please refer to docummentation."), 
                             (exceptions.SingletonError, "This class is a singleton: unable to instantiate.")]
                            ) 
    def test_error_default_message(self, error_class, expected):      
        try:
            raise error_class()
        except error_class as e:
            message = str(e)
        else:
            assert False
            
        assert expected in message

        
    @pytest.mark.parametrize("error_class",
                            [exceptions.InputLengthError, 
                             exceptions.UnsupportedConfigError, 
                             exceptions.SingletonError]
                            )      
    def test_errror_inheritance(self, error_class):
        try:
            raise error_class()
        except error_class as e:
            assert isinstance(e, Exception)
        else:
            assert False
        
    
    @pytest.mark.parametrize("error_class",
                            [exceptions.InputLengthError, 
                             exceptions.UnsupportedConfigError, 
                             exceptions.SingletonError]
                            )
    def test_single_error_custom_message(self, error_class):
        try:
            raise error_class("Test custom message.")
        except error_class as e:
            message = str(e)
        else:
            assert False
            
        expected = "Test custom message."
        assert message == expected