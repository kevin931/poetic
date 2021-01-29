![Logo](/assets/Logo.png)

# Poetic (poetic-py on PyPi)

> A machine-learning package to gauge your poetic madness.

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/for-you.svg)](https://forthebadge.com)

| Branch | Release | Build Status | Docs | Coverage |
| --- | --- | --- | --- | --- |
| dev (default) | ![Badge1](https://img.shields.io/badge/Version-1.1.0-success) | ![devCI](https://github.com/kevin931/poetic/workflows/CI%20Test/badge.svg?branch=dev) | [![Documentation Status](https://readthedocs.org/projects/poetic/badge/?version=dev)](https://poetic.readthedocs.io/en/latest/?badge=dev) | [![codecov](https://codecov.io/gh/kevin931/poetic/branch/dev/graph/badge.svg?token=U24RMH7TA5)](https://codecov.io/gh/kevin931/poetic)
| main | ![Badge1](https://img.shields.io/badge/Version-1.1.0-success)  | ![example branch parameter](https://github.com/kevin931/poetic/workflows/CI%20Test/badge.svg?branch=main) | [![Documentation Status](https://readthedocs.org/projects/poetic/badge/?version=latest)](https://poetic.readthedocs.io/en/latest/?badge=latest) | [![codecov](https://codecov.io/gh/kevin931/poetic/branch/main/graph/badge.svg?token=U24RMH7TA5)](https://codecov.io/gh/kevin931/poetic) |


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [About](#about)
    - [Why should you care?](#why-should-you-care)
- [Installation](#installation)
    - [Dependencies](#dependencies)
- [Usage](#usage)
  - [Command-line Mode](#command-line-mode)
    - [Flags](#flags)
    - [Standard application with GUI](#standard-application-with-gui)
    - [Make a sentence prediction](#make-a-sentence-prediction)
    - [Make a file prediction](#make-a-file-prediction)
    - [Save results to csv or text](#save-results-to-csv-or-text)
  - [As a Python Package](#as-a-python-package)
- [Documentation](#documentation)
- [Versions and Updates](#versions-and-updates)
- [Roadmap](#roadmap)
- [Collaboration](#collaboration)
- [License](#license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## About

Poetic (formerly **Poetry Predictor**) is a Python package and application based on Natural Language Processing and deep learning models to predict how poetic the English language is. Trained on 18th- and 19th-century works, the model predicts how likely the given input is or resembles poetry.

This initiative is originally part of the Robert Mayer Undergraduate Research Fellowship but now an independent, open-source project.

#### Why should you care?
- Are you ever in awe that a random phrase seems so **sexily poetic**?
- Have you ever looked for a poetry prediction tool or a toolchain to work in digital humaninities?
- Would you like to explore the possibilities of letting machine learning models to help define poetry in the digital age?

Look no further. You have found poetic.

<img src="/assets/gui_demo.gif" width="300" height="400" />


**Have fun!!**

## Installation
Python (3.5, 3.6, 3.7, 3.8) and pip (or conda) are required for Poetic to work. Now, poetic officially supports conda as well. Installation from either source will work, but stick to one or the other. 

To install from PyPi:

```shell
  pip install poetic-py
```

To install from conda: 

```shell
  conda install -c kevin931 poetic-py
  python -c "import nltk; nltk.download('punkt')"
```

For installation issues and some caveats, take a look [here](https://poetic.readthedocs.io/en/latest/usage/Installation.html) for some common issues. Or, open an [issue](https://github.com/kevin931/poetic/issues) and I will be glad to help!

#### Dependencies
* tensorflow >= 2
* nltk
* gensim
* numpy

If you have encountered an issue with installation or dependencies, please open an issue so that I can help you out!

## Usage
Poetic supports three modes: command-line usage, python import, and GUI. For a detailed guide on examples and other common usages, visit the [Tutorials and Examples](https://poetic.readthedocs.io/en/latest/usage/index.html) section of the documentation.

### Command-line Mode
A single command is sufficient without need of a python script or launching the GUI.

#### Flags
- ``-s`` or ``--Sentence``:  Supply a sentence or a string of text as an input.
- ``-f`` or ``--File``:      Supply the path to a plain text file.
- ``-o`` or ``--Out``:       Provide the path to save outputs
- ``-g`` or ``--GUI``:       Launch the GUI regardless of the other flags, except for -h.
- ``-h`` or ``--help``:      Help with flags.
- ``--version``:             Returns the version of the package.

#### Standard application with GUI
```shell
  python -m poetic
```

#### Make a sentence prediction
```shell
  python -m poetic -s "I am poetic. Are you?"
```

#### Make a file prediction
```shell
  python -m poetic -f "<PATH_TO_FILE>"
```

#### Save results to csv or text
```shell
  python -m poetic -f "<PATH_TO_FILE>" -o "<PATH>.txt"
  python -m poetic -f "<PATH_TO_FILE>" -o "<PATH>.csv"
  python -m poetic -s "I am poetic. Are you?" -o "<PATH>.txt"
```

### As a Python Package
Poetic contains two major classes: Predictor and Diagnostics. Predictor makes predictions and returns a predictions object inherited from the Diagnostics. For detailed methods and usage, check the [documentation](https://poetic.readthedocs.io/en/latest/index.html) and its [Tutorials and Examples](https://poetic.readthedocs.io/en/latest/usage/index.html#) section. The ``util`` module provides metadata, functionalities for loading and downloading necessary data, and initializing.

Below is the most common use-case as part of the IO and prediction toolchain:

```python
  import poetic

  new_pred = poetic.Predictor()
  sentence_result = new_pred.predict("I am poetic. Are you?")
  file_result = new_pred.predict_file("FILE_PATH.txt")

  # Process results
  sentence_result.run_diagnostics()
  sentence_result.to_file("SAVE_PATH.txt")
  sentence_result.to_csv("SAVE_PATH.csv")

```

## Documentation
Poetic's official [documentation page](https://poetic.readthedocs.io/en/latest/) is live! For more detailed reference, please see the following for a quick guide or follow the navigation on the main page:

  - [Quickstart guide](https://poetic.readthedocs.io/en/latest/usage/Quickstart.html)
  - [Tutorials and examples](https://poetic.readthedocs.io/en/latest/usage/index.html#)
  - [Full documentation](https://poetic.readthedocs.io/en/latest/documentation/index.html)

To visit the documentation for the versions in development or older maintenance versions of ``poetic``, use the version selection at the bottom left of the page for the correct version.

## Versions and Updates

* v1.1.0

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
    - Renamed all method parameter "input" to "lexical_input" in the ``Predictor`` class
    - Renamed "dict" to "dictionary" in the ``poetic.predictor.Predictor`` constructor
    - **For all deprecations, see [here](https://poetic.readthedocs.io/en/latest/change/deprecation.html)**

* v1.0.3
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

* All older changes available in our [documentation's changelog and versions section](https://poetic.readthedocs.io/en/latest/change/index.html)

## Roadmap
Major milestones:
  - [ ] Support for poetic meter: both parsing and predicting
  - [x] Support for custom models other than the default model
  - [ ] Support for more default models

Tentative milestones (subject to change):
  - [x] Backwards compatibility with Python 3.5 (No other versions support planned)
  - [ ] An improved GUI with better front and back end
  - [ ] Package-level optimization

## Collaboration
Collaborations are welcomed for bug fixing, general improvements, future roadmap implementations, etc. Feel free to open an issue if there is something concrete or head to discussions to present new ideas. 

For specific details on how to contribute, see the [Contribution Guideline](https://poetic.readthedocs.io/en/latest/Contributing.html) on our documentation page. BUt you get the point: help, fix, pull request, fork, or whatever you want.

## License
- [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](/LICENSE.txt)
- **[MIT license](/LICENSE.txt)**
- Copyright 2020 © Kevin Wang