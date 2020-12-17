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
import setuptools

description = "Poetic (poetic-py on PyPi) is a Python package "
description += "based on Natural Language Processing and deep learning models to predict how "
description += "poetic the English language is. It also provides a toolchain for processing "
description += "poetry in English. "
description += "For current development details and guides, "
description += "please refer to http://github.com/kevin931/poetic. "
description += "For detailed documentation, please visit "
description += "https://poetic.readthedocs.io/"

setuptools.setup(
    name = "poetic-py",
    version = "1.0.0",
    url = "https://github.com/kevin931/poetic",
    author = "Kevin Wang",
    author_email = "bridgemarian@gmail.com",
    description = "Let Us Be More poetic: A Poetry Prediction and Processing Package.",
    long_description = description,
    packages=["poetic"],
    python_requires=">=3.5, <3.9",
    install_requires=["tensorflow>=2",
                      "gensim>=3.8, <4",
                      "nltk>=3.4",
                      "numpy"
    ],
    install_package_data=True,
    package_data={"poetic":["./data/word_dictionary_complete.txt"]},
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Natural Language :: English"
    ]
)