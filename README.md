![Logo](/assets/Logo.png)

# Poetic (poetic-py on PyPi)

> A machine-learning package to gauge your poetic madness.

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/for-you.svg)](https://forthebadge.com)

| Branch | Release | Build Status | Docs | Coverage |
| --- | --- | --- | --- | --- |
| dev (default) | ![Badge1](https://img.shields.io/badge/Version-1.0.0-success) | [![DevBuild](https://travis-ci.com/kevin931/poetic.svg?branch=dev)](https://travis-ci.com/kevin931/poetic) | [![Documentation Status](https://readthedocs.org/projects/poetic/badge/?version=dev)](https://poetic.readthedocs.io/en/latest/?badge=dev) | [![Coverage Status](https://coveralls.io/repos/github/kevin931/poetic/badge.svg?branch=dev)](https://coveralls.io/github/kevin931/poetic?branch=dev)
| main | ![Badge1](https://img.shields.io/badge/Version-1.0.0-success)  | [![DevBuild](https://travis-ci.com/kevin931/poetic.svg?branch=main)](https://travis-ci.com/kevin931/poetic) | [![Documentation Status](https://readthedocs.org/projects/poetic/badge/?version=latest)](https://poetic.readthedocs.io/en/latest/?badge=latest) | [![Coverage Status](https://coveralls.io/repos/github/kevin931/poetic/badge.svg?branch=main)](https://coveralls.io/github/kevin931/poetic?branch=main) |


<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [About](#about)
    - [Why should you care?](#why-should-you-care)
- [Installation](#installation)
    - [Dependencies](#dependencies)
    - [Conda](#conda)
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
Python 3 and pip are required for Poetic to work. There is currently no official build for Conda (although it will work with correct setup documented below), which will be a consideration on the roadmap. The package itself is named as "poetic" after installation.

To install from PyPi:

```shell
  pip install poetic-py
```

PyPi should be able to handle all the dependencies. If pip caching becomes an issue or there are issues with dependencies, try the following:

```shell
  python -m pip install -upgrade pip
  pip install --no-cache-dir poetic-py
```

#### Dependencies
* tensorflow >= 2
* nltk >= 3.4
* gensim >= 3.8, <=4

If you have encountered an issue with installation or dependencies, please open an issue so that I can help you out!

#### Conda
I love Conda (and that is what I use on my development machine)! At this time, poetic itself is not yet hosted on conda or conda-forge. More works to make that happen are on the way. To make sure that everything plays nicely withe each other, install the dependencies first (provided that you already have a conda environment set up):

```shell
  conda install tensorflow
  conda install gensim
  conda install nltk
  pip install poetic-py
```

 For more information on conda environments, [this is a good guide.](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html)

## Usage
Poetic supports both command-line mode and be used as a standard Python package.

### Command-line Mode
A single command is sufficient without need of a python script.

#### Flags
- **-s**        Supply a sentence or a string of text as an input.
- **-f**        Supply the path to a plain text file.
- **-o**        Provide the path to save outputs
- **--GUI**     Launch the GUI regardless of the other flags, except for -h.
- **-h**        Help with flags.
- **--version** Returns the version of the package.

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
Poetic contains two major classes: Predictor and Diagnostics. Predictor makes predictions and returns a predictions object inherited from the Diagnostics. For detailed methods and usage, check the [documentation](https://poetic.readthedocs.io/en/latest/index.html). The util module provides metadata, functionalities for loading and downloading necessary data, and initializing.

Below is the most common usecase:

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
Poetic's official documentation page is live! To read about new details, please head to poetic.readthedocs.io/en/latest/ for the latest official release.

To visit the documentation for the dev branch (which may include broken builds or incomplete documentation), you can use [this link](https://poetic.readthedocs.io/en/dev/). 

## Versions and Updates
* v.1.0.1
  - Now on **conda** as poetic-py
  - Updated documentation for roadmap
  - Fixed type-hinting errors
  - Updated docstring
  - Automated package build process

* All older changes available in our [documentation](https://poetic.readthedocs.io/en/latest/Changelog.html)

## Roadmap
* Major milestones:
  - Support for poetic meter: both parsing and predicting
  - Support for custom models other than the ones provided

* Tentative milestones:
  - Backwards compatibility with Python 3.5 (No older versions support planned).
  - A better GUI
  - Package-level optimization


## Collaboration
Collaborations are welcomed for bug fixing, general improvements, future roadmap implementations, etc. Feel free to open an issue if there is something concrete or head to discussions to present new ideas. You get the point: help, fix, pull request, fork, or whatever you want.

## License
- [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](/LICENSE.txt)
- **[MIT license](/LICENSE.txt)**
- Copyright 2020 © Kevin Wang