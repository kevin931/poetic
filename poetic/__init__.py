"""Poetic Package.

This is the Poetic package, which provides functionalities for
predicting how poetic language is using a Keras model trained on
public-domain works. For further documentation and latest releases,
please visit https://github.com/kevin931/poetic.

Modules:
    - predictor
    - results
    - util
    
Package-level Classes:
    - Predictor
    - Diagnostics
    
"""

from poetic.predictor import Predictor
from poetic.results import Diagnostics
from poetic import util