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