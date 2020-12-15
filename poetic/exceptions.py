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
""" Module for custom exceptions.

The exceptions module includes custom classes for specific
errors in the poetic package. This is not part of the public
interface.

"""

from typing import Optional

class InputLengthError(Exception):
    
    """ Raises Input Length Error.
    
    This exception is used in the Predictor class for the input length
    of 0.
    
    Args:
        message(str): The error message to display. 
    
    """

    def __init__(self, message: Optional[str]=None) -> None:
        if message is None:
            message = "The current length is unsupported or out of bound."
        super().__init__(message)


class UnsupportedConfigError(Exception):
    
    """ Raises Unsupported Configuration Error.
    
    This exception is used in the _Arguments class for checking
    unsupported commandline flags.
    
    Args:
        message(str): The error message to display. 
    
    """

    def __init__(self, message: Optional[str]=None) -> None:
        if message is None:
            message = "Unsupported configuration: Please refer to docummentation."
        super().__init__(message)
        
        
class SingletonError(Exception):
    
    """ Raises exception for instantiating Singleton class already in existence.
    
    This exception is used for any singleton class in the package. When the singleton
    class already has an instance and the constructor is explicitly called, this exception
    will be thrown. To avoid this exception, use the get_instance() method instead of
    instantiating the class.
    
    Args:
        message(str): The error message to display.
    
    """
    
    def __init__(self, message: Optional[str]=None) -> None:
        if message is None:
            message = "This class is a singleton: unable to instantiate."
            super().__init__(message)
    
    