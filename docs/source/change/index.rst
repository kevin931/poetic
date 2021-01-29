Changelog and Versions
=======================

.. toctree::
    :maxdepth: 1

    previous
    deprecation
    development
    
--------------------

****************
Latest Versions
****************

v1.1.0
--------

Changelog
~~~~~~~~~~

    - Added comparison operator support to the ``Diagnostics`` class
    - Added support for concatenating two ``Diagnostics`` instances using ``+`` and ``+=``
    - Implemented the ``Info`` class as a singleton
    - Added support for using custom model and dictionary in the ``Predictor`` class
    - Added support for loading custom dictionary and model using the ``Initializer`` class
    - Changed "sent model" to "lexical model" for naming accuracy
    - Added theoretical support for python 3.5 (No CI testing)
    - Deprecated function parameters ("input" and "dict") to avoid overwriting builtin functions and methods
    - Optimized unittest infrastructure with more test coverage
    - Added Github README to ``pypi``

Deprecations
~~~~~~~~~~~~~

Some method parameters have been renamed:

    - Renamed "input" to "lexical_input" in the following methods:

        - ``poetic.predictor.Predictor.predict``
        - ``poetic.predictor.Predictor.preprocess``
        - ``poetic.predictor.Predictor.tokenize``
        - ``poetic.predictor.Predictor.word_id``

    - Renamed "dict" to "dictionary" in the ``poetic.predictor.Predictor`` constructor

Positional arguments remain unchanged. Deprecated arguments, "input" or "dict", become
keyword-only arguments for backwards compatibility if they have been explicitly named in
function calls.

v1.0.3
---------

    - Added "**Tutorials and Examples**" section to documentation
    - Fixed file output spacing issues
    - Fixed conda channel priority documentation for python 3.8
    - Fixed documentation code highlighting
    - Fixed type annotation for the ``Predictor`` and ``Predictions`` class
    - Fixed docstrings for multiple returns with tuples
    - Fixed conda platform conversion commands in setup.py
    - Added in-line code highlighting in documentation
    - Added import statements to complete examples
    - Changed CLI help section wording