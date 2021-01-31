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
import os
import sys
import shutil
import distutils

from typing import List

VERSION = "1.0.3"

description = "Poetic (poetic-py on PyPi) is a Python package "
description += "based on Natural Language Processing and deep learning models to predict how "
description += "poetic the English language is. It also provides a toolchain for processing "
description += "poetry in English. "
description += "For current development details and guides, "
description += "please refer to http://github.com/kevin931/poetic. "
description += "For detailed documentation, please visit "
description += "https://poetic.readthedocs.io/"


class LicenseCommand(distutils.cmd.Command):
    description = "Add and check license for source files."
    user_options = []
    
    def initialize_options(self):
        pass
    
    
    def finalize_options(self):
        pass
    
    
    def run(self):
        os.system("{} ./utility/source_header.py ./".format(sys.executable))
        

class PypiCommand(distutils.cmd.Command):
    
    description = "Build and upload for PyPi."
    user_options = []
    
    def initialize_options(self):
        pass
    
    
    def finalize_options(self):
        pass
    
    
    def run(self):
        shutil.rmtree("dist/")
        
        wheel_file = "poetic_py-{}-py3-none-any.whl".format(VERSION)
        tar_file = "poetic-py-{}.tar.gz".format(VERSION)
        
        os.system("{} setup.py sdist bdist_wheel".format(sys.executable))
        os.system("twine upload dist/{} dist/{}".format(wheel_file, tar_file))
    
    
class CondaCommand(distutils.cmd.Command):
    
    description = "Build and upload for conda."
    user_options = []
    
    
    @staticmethod
    def move_assets(origin: str, destination: str, exclude: List[str], new_destination_dir: bool) -> None:
        
        if origin[-1] != "\\" and origin[-1] != "/":
            origin += "/"
            
        if destination[-1] != "\\" and destination[-1] != "/":
            destination += "/"
        
        if new_destination_dir:    
            if os.path.isdir(destination):
                raise ValueError("Destination directory already exists.")
            else:
                os.mkdir(destination)
            
        all_files = os.listdir(origin)
        
        for files in all_files:
            if files in exclude:
                pass
            else:
                origin_path = origin + files
                destination_path = destination + files
                shutil.move(origin_path, destination_path)
        
    
    def initialize_options(self):
        pass
    
    
    def finalize_options(self):
        pass
    
    
    def run(self):
        
        self.move_assets("./poetic/data/", "../temp_assets/", ["word_dictionary_complete.txt"], True)
        
        shutil.rmtree("dist_conda/")
        os.system("conda build . --output-folder dist_conda/")
        os.system("anaconda upload ./dist_conda/noarch/poetic-py-{}-py_0.tar.bz2".format(VERSION))
        
        self.move_assets("../temp_assets/", "./poetic/data/", [], False)
        shutil.rmtree("../temp_assets/")
           

setuptools.setup(
    name = "poetic-py",
    version = VERSION,
    url = "https://github.com/kevin931/poetic",
    author = "Kevin Wang",
    author_email = "bridgemarian@gmail.com",
    description = "A poetry predictor and toolkit.",
    long_description = description,
    packages=["poetic"],
    python_requires=">=3.6, <3.9",
    install_requires=["tensorflow>=2",
                      "gensim",
                      "nltk",
                      "numpy"
    ],
    install_package_data=True,
    package_data={"poetic":["./data/word_dictionary_complete.txt"]},
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Natural Language :: English"
    ],
    cmdclass = {"license": LicenseCommand,
                "pypi": PypiCommand,
                "conda": CondaCommand
                }
)