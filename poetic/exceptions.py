from typing import Optional

class InputLengthError(Exception):
    # Raise error for inproper input length
    # Used in Predictor class.

    def __init__(self, message: Optional[str]=None) -> None:
        if message is None:
            message = "The current length is unsupported or out of bound."
        super().__init__(message)


class UnsupportedConfigError(Exception):
    # Check unsupported command line argument configuration.
    # Used in util.Arguments()

    def __init__(self, message: Optional[str]=None) -> None:
        if message is None:
            message = "Unsupported configuration: Please refer to docummentation."
        super().__init__(message)