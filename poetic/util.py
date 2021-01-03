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
"""Module for package utility.

This module includes the necessary functionalities to load and
download assets for other modules in the package and provide basic
information for the current build and version as needed.

Examples:
    To get the build and version information of the package:
    
    .. code-block:: python
    
        poetic.util.Info.version()
        poetic.util.Info.build_status()
        
    Under normal circumstances, the methods in the Initializer class is not needed
    as part of the prediction workflow. One of the most common usage of a first-time
    user is to download the assets:
    
    .. code-block:: python
    
        poetic.util.Initializer.download_assets()
        
    The tensorflow model and gensim models can also be loaded and returned if they 
    theselves are useful (the Predictor class loads the model automatically):
    
    .. code-block:: python
    
        poetic.util.Initializer.load_dict()
        poetic.util.Initializer.load_model()
        
    Both download_assets() and load_model() methods have the force_download parameter
    which controls whether to download the models without taking commandline inputs
    when the model is missing. It is default to False so that it does not take up 
    bandwidth unintendedly, but it can also be set to True in cases necessary. 

"""

from tensorflow import keras
import gensim

from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO

import os
import argparse
import pkg_resources
import re

from poetic import exceptions

from typing import Optional, List, Dict, Union


class Info():
    """Basic information for the package.
    
    Info class provides the basic information of the package: its version and build status.
    This class, by design, is a singleton and has no public interface. 
    
    Raises:
        poetic.exceptions.SingletonError: This exception is raised when an instance of the Info
            class already exists while calling the constructor.
            
    """
    
    __INSTANCE = None
    __VERSION = "1.0.2"
    __BUILD_STATUS = "Dev"
    
    
    def __init__(self, _test: Optional[bool] = False) -> None:
        
        if Info.__INSTANCE is not None:
            message = "Info is a singleton class. Use Info.get_instance() instead."
            raise exceptions.SingletonError(message)
        
        else:
            self.__TEST = _test
            Info.__INSTANCE = self
            
            
    def __str__(self):
        """ String representation for ``str()``.
        
        This string representation returns the basic information of the package:
        name, version, build, and mode. 
        
        Returns:
            str: String representation of the object with str.
        """
        
        string = ("Package: poetic (poetic-py)\n"
                  "Version: {}\n"
                  "Build: {}\n"
                  "Unittest Mode: {}".format(self.__VERSION, self.__BUILD_STATUS, self.__TEST)
                  )
        
        return string
    
    
    def __repr__(self):
        """ String representation for ``repr()``.
        
        This string representation returns a dictionary cast into a string with 
        the basic information of the package with the following keys: 'Package', 
        'Version', 'Build', and 'Unittest mode'. 
        
        Returns:
            str: String representation of the object with repr.
        """
        
        repr_dict = {"Package": "poetic",
                     "Version": self.__VERSION,
                     "Build": self.__BUILD_STATUS,
                     "Unittest Mode": self.__TEST}
        
        return str(repr_dict)

   
    @classmethod           
    def get_instance(cls, _test: Optional[bool] = False) -> "poetic.util.Info":
        """The method to access the singleton Info class. 
        
        The use of this method is recommended over using the constructor
        because the constructor will throw an exception if an instance already exists.
        
        Returns:
            poetic.util.Info: The singleton Info class
        
        """
        
        if Info.__INSTANCE is None:
            Info(_test= _test)
        
        return cls.__INSTANCE


    @classmethod
    def version(cls) -> str:
        """
        A getter method to return the version of the package.

        Returns:
            str: The current version of the package.
        """
                
        return cls.__VERSION


    @classmethod
    def build_status(cls) -> str:
        """
        A getter method to return build status of the current version.

        Returns:
            str: The build status of the current version.
        """

        return cls.__BUILD_STATUS


    def _test(self) -> bool:     
        return self.__TEST
    
    
    def _destructor(self) -> None:
        del Info.__INSTANCE
        Info.__INSTANCE = None


class Initializer():
    """Initializes core components of the package.

    The Initializer is core part of Poetic that loads and
    downloads models and other necessary assets. It also
    facilitates the command line mode by interacting with
    the _Arguments class.

    """

    # Package data directory
    _data_dir = pkg_resources.resource_filename("poetic", "data/")

    # Model Path
    _weights_dir = _data_dir + "lexical_model.h5"
    _model_dir = _data_dir + "lexical_model.json"
    
    _weights_dir_legacy = _data_dir + "sent_model.h5"
    _model_dir_legacy = _data_dir + "sent_model.json"


    @classmethod
    def initialize(cls, *, _test_args: Optional[Union[List[str], str]]=None):
        """Initializes the package.

        This methods checks for any command line arguments,
        and then loads both the gensim dictionary and the
        Keras model with its weights.

        Returns:
            tuple: Tuple with the following elements
            
                dict: 
                    A dictionary of commandline arguments.
                tensorflow.keras.Model: 
                    A pre-trained Keras model with its weights loaded.
                gensim.corpora.dictionary.Dictionary: 
                    A gensim dictionary.

        """
        
        arguments = _Arguments()
        arguments = arguments.parse(_test_args)

        model = cls.load_model()
        word_dictionary = cls.load_dict()

        return arguments, model, word_dictionary


    @classmethod
    def load_dict(cls, *, dictionary_path: Optional[str]=None) -> gensim.corpora.dictionary.Dictionary:
        """Loads gensim dictionary.
        
        This method loads the gensim dictionary necessary for converting word
        tokens into ids for preprocessing. When 'dictionary_path' is not provided,
        the method loads the default dictionary of the package; otherwise, the
        specified dictionary will be loaded and returned.
        
        Parameters:
            dictionary_path (str, optional):
                The path to the custom gensim dictionary saved using `save_as_text()`
                or a text file in the same format. File extension is not enforced.

        Returns:
            gensim.corpora.dictionary.Dictionary: A gensim dictionary.

        """
        
        if dictionary_path is None:
            dictionary_path = cls._data_dir + "word_dictionary_complete.txt"
            
        word_dictionary = gensim.corpora.Dictionary.load_from_text(fname=dictionary_path)
        return word_dictionary


    @classmethod
    def load_model(cls,
                   force_download: Optional[bool]=False,
                   *,
                   model_path: Optional[str]=None,
                   weights_path: Optional[str]=None) -> "tensorflow.keras.Model":
        """Load Keras models.

        This method uses the Keras interface to load the previously
        trained models, which are necessary for the Predictor and
        the GUI. To use the default models, use all default parameters.
        If the default model does not exist and no custom model is
        provided, the download_assets() method is automatically called 
        for the option to obtain the necessary assets. To use custom
        models, only Keras models saved in .json, .yaml, and .h5 are
        supported by this method.

        Parameters:
            force_download (bool, optional):
                A boolean value on whether to download the default 
                models without asking if they do not exist. This
                parameter ignored when model_path is provided.
            model_path (str, optional):
                The path to the keras model file in json, yaml, or
                h5 format. It is optional when default models are
                intended. When weights_path is provided, model_path
                is mandatory.
            weights_path (str, optional):
                The path to the weights of the model to be loaded.
                It is optional for loading the default model or
                customized models saved in h5 format. It is mandatory
                for json or yaml model files.

        Returns:
            tensorflow.keras.Model: Pretrained Keras model
            
        Raises:
            ValueError: Errors for unsupported model_path and weights_path.

        """
            
        if model_path is None and weights_path is None:
            
            assets = cls.check_assets()
            if not assets["all_exist"]:
                cls.download_assets(assets_status=assets, force_download=force_download)
                
            model_path = cls._model_dir
            weights_path = cls._weights_dir
            
        elif model_path is None:
            raise ValueError("Parameter 'model_path' has to be provided with 'weights_path'.")
        
        model_file = open(model_path, "r")
        loaded_model = model_file.read()
        model_file.close()
        
        if re.search("\\.json$", model_path) is not None:
            model = keras.models.model_from_json(loaded_model)
            
        elif re.search("\\.yaml$", model_path) is not None:
            model = keras.models.model_from_yaml(loaded_model)
            
        elif re.search("\\.h5$", model_path) is not None:
            model = keras.models.load_model(loaded_model)
            return model
        else:
            raise ValueError("The current model format is unsupported: use .json, .yaml, or .h5.")
            
        if weights_path is None:
            raise ValueError("Parameter 'weights_path' has to be provided with json and yaml model files.")
        
        model.load_weights(weights_path)
        return model


    @classmethod
    def check_assets(cls) -> Dict[str,bool]:
        """ Method to check whether assets requirements are met.

        This method checks both the model and its weights in the
        corresponding directory. It reports back their existence
        as part of the package requirement.

        Returns:
            dict: the status of the assets as a dictionary.

        """

        model_status = os.path.exists(cls._model_dir)
        weights_status = os.path.exists(cls._weights_dir)
        
        if not model_status:
            model_status = os.path.exists(cls._model_dir_legacy)
            
            if model_status:
                cls._rename_legacy_assets("sent_model.json", "lexical_model.json")
            
        if not weights_status:
            weights_status = os.path.exists(cls._weights_dir_legacy)
            
            if weights_status:
                cls._rename_legacy_assets("sent_model.h5", "lexical_model.h5")

        status = {}
        status["all_exist"] = True if model_status and weights_status else False
        status["model"] = model_status
        status["weights"] = weights_status

        return status


    @classmethod
    def download_assets(cls, 
                        assets_status: Optional[Dict[str,bool]]=None, 
                        force_download: Optional[bool]=False) -> None:
        
        """Method to download models.

        This method downloads models from the poetic-models
        github repository. Under usual circumstances, other
        functions will download the models automatically if needed.
        If all the models already exist, this function will not
        download them again for package efficiency and bandwidth
        saving.

        If you would like to redownload the assets anyway, a manual
        download from https://github.com/kevin931/poetic-models/releases
        is necessary.

        Parameters:
            assets_status (dict, optional):
                A dictionary generated by ``check_assets()`` method. 
                It has keys "all_exist", "model", and "weights" with all 
                values being boolean.
            force_download (bool, optional):
                A boolean indicating whether assets should be downloaded
                regardless of their existence and user inputs.

        """

        url = "https://github.com/kevin931/poetic-models/releases/download/v1.0.0/lexical_model.zip"

        if assets_status is None:
            assets_status = cls.check_assets()
        
        if assets_status["all_exist"]:
            return None

        # Download Information
        message = "\nThe following important assets are missing:\n"
        message += "-- sent_model.json\n" if not assets_status["model"] else ""
        message += "-- sent_model.h5\n" if not assets_status["weights"] else ""
        message += "\nDownloading from: {}\n".format(url)
        message += "Download size: 835MB.\n\n"
        print(message)

        if not force_download:
            value = input("Would you like to download? [y/n]")
            
            if value.lower() != "y":
                message_2 = "\nYou have declined to download the assets.\n"
                message_2 += "To download in the future, call Predictor()\n"
                message_2 += "or use util.Initializer.download_assets().\n"
                message_2 += "At this time, Predictor is unfunctional without\n"
                message_2 += "the necessary assets. For future features or feature requests\n"
                message_2 += "please visit: https://github.com/kevin931/poetic\n"
                message_2 += "Stay poetic!\n"
                print(message_2)

                return None

        # Download message
        message_3 = "\nDownload in progress...\n"
        message_3 += "This may take quite a while, "
        message_3 += "go grab a coffee and be poetic.\n"
        print(message_3)
        
        if Info.get_instance()._test(): return None
        
        contents = urlopen(url)
        contents = contents.read()
        zip_file = ZipFile(BytesIO(contents))
        zip_file.extractall(cls._data_dir)
    
    
    @classmethod
    def _rename_legacy_assets(cls, old_name: str, new_name: str) -> None:
        old_path = cls._data_dir + old_name
        new_path = cls._data_dir + new_name
        os.rename(old_path, new_path)


class _Arguments():
    # This class parses command line arguments.

    def __init__(self) -> None:
        # New parser with the appropriate flags.

        self.parser = argparse.ArgumentParser(description="Poetry Predictor Command Line Mode")
        self.parser.add_argument("-g", "--GUI", action="store_true",
                                 help="Tag to open GUI anyway. No imput needed.")
        self.parser.add_argument("-s", "--Sentence", action="store",
                                 help="Sentence to be parsed.")
        self.parser.add_argument("-f", "--File", action="store",
                                 help="File to be parsed.")
        self.parser.add_argument("-o", "--Out", action="store",
                                 help="Path to save results.")
        self.parser.add_argument("--version", action="version", version=self.version())


    def parse(self, args: Optional[List[str]]=None) -> Dict[str, Optional[str]]:
        # Parse arguments

        arguments = self.parser.parse_args(args)
        arguments = vars(arguments)
        # Check for error
        if arguments["Sentence"] is not None and arguments["File"] is not None:
            message = "Unsupported configurations: "
            message += "-f and -s tags cannot be both used.\n"
            message += "To make two predictions, please do two operations.\n"
            raise exceptions.UnsupportedConfigError(message)

        return arguments


    def version(self) -> str:
        # Format the command-line version output

        v = "Poetic "
        v += Info.version() + " "
        v += Info.build_status()

        return v