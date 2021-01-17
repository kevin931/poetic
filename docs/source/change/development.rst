========================
Versions in Development
========================

This page documents features changed during development for new versions planned.
This is highly subject to change, and it is not guaranteed that features appeared
here will appear in a stable release. Once a version is release, the changelog will
be moved to the **Latest Versions** section under the correct release. 

For developers, please see the **Contribution Guideline** section instructions on
changes.

-------------------------------

****************
Planned Updates
****************

v1.1.0
--------

Corresponding branch: "dev"

Changelog
~~~~~~~~~~

    - Added comparison operator support to the ``Diagnostics`` class
    - Implemented the ``Info`` class as a singleton
    - Added support for using custom model and dictionary in the ``Predictor`` class
    - Added support for loading custom dictionary and model using the ``Initializer`` class
    - Changed "sent model" to "lexical model" for naming accuracy
    - Added theoretical support for python 3.5 (No CI testing)
    - Deprecated function parameters ("input" and "dict") to avoid overwriting builtin functions and methods
    - Optimized unittest infrastructure with more test coverage

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