![Logo](/Docs/Logo.png)

# Poetic (poetic-py on pypi)

> A machine-learning package to gauge your poetic madness.

![Badge1](https://img.shields.io/badge/Version-1.0.0b1-success) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](/LICENSE.txt)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [About](#about)
    - [Why should you care?](#why-should-you-care)
- [Installation](#installation)
- [Usage](#usage)
  - [Command-line Mode](#command-line-mode)
    - [Flags](#flags)
    - [Standard application with GUI](#standard-application-with-gui)
    - [Make a sentence prediction](#make-a-sentence-prediction)
    - [Make a file prediction](#make-a-file-prediction)
    - [Save results to csv or text](#save-results-to-csv-or-text)
  - [As a Python Package](#as-a-python-package)
- [Version](#version)
- [Future Update Roadmap:](#future-update-roadmap)
- [Collaboration](#collaboration)
- [License](#license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## About

Poetic (formerly **Poetry Predictor**) is a Python package and application based on Natural Language Processing and deep learning models to predict how poetic the English language is. Trained on 18th- and 19th-century works, the model predicts how likely the given input is or resembles poetry.

This initiative is originally part of the Robert Mayer Undergraduate Research Fellowship but now an independent, open-source project.

#### Why should you care?

- Are you ever in awe that a random phrase seems so **sexily poetic**?
- Do you ever wonder whether your love letter is up to the standards of famous poets or are compliments you get merely compliments?
- Can you imagine a software that helps define poetry in the digital age?

Look no further. You have found poetic.

<img src="/Docs/gui_demo.gif" width="300" height="400" />


**Have fun!!**

## Installation
Python 3 and pip are required for Poetic to work. There is currently no support for Conda, which will be a consideration on the roadmap. The package itself is named as "poetic" after installation.

To install from pypi:
```shell
  pip install poetic-py

```

Pypi should be able to handle all the dependencies. More testing on version compatibility is on the way.


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
  python -m poetic -f "PATH_TO_FILE"
```

#### Save results to csv or text
```shell
  python -m poetic -f "PATH_TO_FILE" -o "PATH.txt"
  python -m poetic -f "PATH_TO_FILE" -o "PATH.csv"
  python -m poetic -s "I am poetic. Are you?" -o "PATH.txt"
```

### As a Python Package

Poetic contains two major classes: Predictor and Diagnostics. Predictor makes predictions, which in turn are inherited from the Diagnostics. For detailed methods and usage, check the docstrings of each class and method, more documentation is on the way. The util module provides metadata, functionalities for loading and downloading necessary data, and initializing.

Below are some common use cases:

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


## Version
* v.1.0.0b1
  - **Now on pypi**
  - Support for command-line mode.
  - Support for processing text file.
  - Added docstring documentation.
  - Revemped Github repo without LFS.
  - Data now hosted on [poetic-models](https://github.com/kevin931/poetic-models)

* v.0.1.2
  - Fixed a bug displaying score without entering anything
  - Optimized error handling in Predictor class
  - Further optimized the directory tree

* v.0.1.1
  - Optimized directory structure
  - Revamped README with detailed guides
  - Added launcher script
  - Easier installation

* v.0.1.0
  - Added GUI for better user experience
  - Executable for Windows without need for installation
  - Updated code structure
  - Updated Project Structure

* v.0.0.1
  - Project initialization on GitHub.
  - Improved interface.
  - Updated model.
  - LFS support for GitHub.

## Future Update Roadmap:
- Support poetic meter
- Support for other and custom Keras models
- More tests and dedicated documentation

## Collaboration
Collaborations welcomed for bug fixing, general improvements, future roadmap implementations, etc. You get the point: help, fork, or whatever you want.

## License

- **[MIT license](/LICENSE.txt)**
- Copyright 2020 © Kevin Wang