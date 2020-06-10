![Logo](/Docs/Logo.png)

# Poetry Predictor

> A program based on machine learning to gauge your poetic madness.

![Badge1](https://img.shields.io/badge/Version-0.1.1-success) [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](/LICENSE.txt)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [About](#about)
    - [Why should you care?](#why-should-you-care)
- [Installation](#installation)
    - [The Recommended Way:](#the-recommended-way)
    - [The Other ~~Not So Easy~~ Way:](#the-other-not-so-easy-way)
- [Run the Program](#run-the-program)
- [Version](#version)
- [Future Update Plans:](#future-update-plans)
- [License](#license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## About

The Poetry Predictor is a Python desktop application based on Natural Language Processing and deep learning models to predict how poetic sentences are. Trained on 18th- and 19th-century works, the model predicts how likely the given input is poetry.

This initiative is originally part of the Robert Mayer Undergraduate Research Fellowship but now an independent, continuing project.

#### Why should you care?

- Are you ever in awe that a random phrase seems so **sexily poetic**?
- Do you ever wonder whether your love letter is up to the standards of famous poets or are compliments you get merely compliments?
- Can you imagine a software that helps define poetry in the digital age?

Look no further. You have found the poetry predictor.

![Screenshot of program](/Docs/screenshot.png)

**Have fun!!**

## Installation
#### The Recommended Way:
1. **Manual installation** of python and Anaconda required for **all platforms** at this time.
2. For detailed installation steps of Anaconda, please refer to [this guide](https://docs.anaconda.com/anaconda/install/).
3. Clone the GitHub repo (for Windows users without Git installed, downloading the repository using [this link](https://github.com/kevin931/PoetryPredictor/archive/master.zip) is okay, too!):
```shell
git clone https://github.com/kevin931/PoetryPredictor.git
```
4. Virtual environment activation:
```shell
cd DIRECTORY_PATH_OF_PROGRAM
conda env create -f environment.yml
```
5. To verify the program has installed correctly, run
```shell
cd DIRECTORY_PATH_OF_PROGRAM
conda activate PoetryPredictor
python Launch.py
```

#### The Other ~~Not So Easy~~ Way:
* Use of virtual environment is still highly encouraged!
* The program will run with the following packages:
  * python 3.7.7
  * numpy 1.18.1
  * tensorflow 2.1.0
  * gensim 3.8.0
* Support for other versions not guaranteed.

## Run the Program
If everything installs successfully, run the following commands for every subsequent launch:
```shell
cd DIRECTORY_PATH_OF_PROGRAM
conda activate PoetryPredictor
python Launch.py
```

## Update the program
Unfortunately, there is no easy way to update or auto-update at this time.

**For users with git**, run the following command:
```shell
git clone https://github.com/kevin931/PoetryPredictor.git
```

**For those who downloaded the zip file from GitHub**, the same download is necessary
again.

There will **NO** need to update the virtual environment with minor feature
updates or bug fixes.


## Version
* v.0.1.2 beta
  - Fixed a bug displaying score without entering anything
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
#### Short term updates:
- Support poetic meter
- Functionalities for parsing text in files or in batch

#### Long term updates:
- PyPI Package
- Better distribution support

## Collaboration
Collaborations welcomed for bug fixing, general improvements, future roadmap implementations, etc. You get the point: this is an open source project.

## License

- **[MIT license](/LICENSE.txt)**
- Copyright 2020 © Kevin Wang