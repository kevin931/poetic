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
    
        poetic.Info.version()
        poetic.Info.build_status()
        
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

from os import path
import argparse
import pkg_resources

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
    __VERSION = "1.0.0"
    __BUILD_STATUS = "Dev"
    
    
    def __init__(self, _test: Optional[bool] = False) -> None:
        
        if Info.__INSTANCE is not None:
            message = "Info is a singleton class. Use Info.get_instance() instead."
            raise exceptions.SingletonError(message)
        
        else:
            self.__TEST = _test
            Info.__INSTANCE = self
            
            
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


class Initializer():
    """Initializes core components of the package.

    The Initializer is core part of Poetic that loads and
    downloads models and other necessary assets. It also
    facilitates the command line mode by interacting with
    the _Arguments class.

    """

    # Package data directory
    _data_dir = pkg_resources.resource_filename("poetic", "data/")
    if _data_dir[-1] != "\\" and _data_dir[-1] != "/":
        _data_dir += "/" # pragma: no cover

    # Model Path
    _weights_dir = _data_dir+"sent_model.h5"
    _model_dir = _data_dir+"sent_model.json"


    @classmethod
    def initialize(cls, *, _test: bool=False, _test_args: Optional[Union[List[str], str]]=None):
        """Initializes the package.

        This methods checks for any command line arguments,
        and then loads both the gensim dictionary and the
        Keras model with its weights.

        Returns:
            dict: A dictionary of commandline arguments.
            tensorflow.keras.Model: A pre-trained Keras model with its weights loaded.
            gensim.corpora.dictionary.Dictionary: A gensim dictionary.

        """
        
        arguments = _Arguments()
        arguments = arguments.parse(_test_args)

        model = cls.load_model(_test=_test)
        word_dictionary = cls.load_dict()

        return arguments, model, word_dictionary


    @classmethod
    def load_dict(cls) -> gensim.corpora.dictionary.Dictionary:
        """Loads gensim dictionary.

        Returns:
            gensim.corpora.dictionary.Dictionary: A gensim dictionary.

        """
        
        dir = cls._data_dir + "word_dictionary_complete.txt"
        word_dictionary = gensim.corpora.Dictionary.load_from_text(fname=dir)
        return word_dictionary


    @classmethod
    def load_model(cls, 
                   force_download: bool=False, 
                   *, 
                   _test: bool=False) -> keras.Model: # pylint: disable=no-member
        """Load Keras models.

        This method uses Keras interface to load the previously
        trained models, which are necessary for the Predictor and
        the GUI. If the model does not exist, the download_assets()
        method is automatically called for the option to obtain
        the necessary assets.

        Parameters:
            force_download (bool, optional):
                A boolean value on whether to download the models
                without asking if the models do not exist.

        Returns:
            tensorflow.python.keras.engine.training.Model: Pretrained Keras model

        """
        
        # Check model assets status
        assets = cls.check_assets()
        if not assets["all_exist"]:
            assets["all_exist"] = True if _test else False
            cls.download_assets(assets_status=assets, force_download=force_download)
            
        model_dir = cls._test_variables()["model"] if _test else cls._model_dir
        weights_dir = cls._test_variables()["weights"] if _test else cls._weights_dir

        json_file = open(model_dir, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = keras.models.model_from_json(loaded_model_json)
        # load weights into new model
        model.load_weights(weights_dir)
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

        model_status = path.exists(cls._model_dir)
        weights_status = path.exists(cls._weights_dir)

        status = {}
        status["all_exist"] = True if model_status and weights_status else False
        status["model"] = model_status
        status["weights"] = weights_status

        return status


    @classmethod
    def download_assets(cls, 
                        assets_status: Optional[Dict[str,bool]]=None, 
                        force_download: bool=False, 
                        *, 
                        _test: bool=False, 
                        _test_input: Optional[str]=None) -> None:
        
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
                A dictionary generated by check_assets() method. It has
                keys "all_exist", "model", and "weights" with all values
                being boolean.
            force_download (bool, optional):
                A boolean indicating whether assets should be downloaded
                regardless of their existence and user inputs.

        """

        url = "https://github.com/kevin931/poetic-models/releases/download/v0.1-alpha/sent_model.zip"

        if assets_status is None:
            assets_status = cls.check_assets()
            if _test and _test_input is None: assets_status["all_exist"] = True
        
        if assets_status["all_exist"]:
            return None

        # Download Message
        message = "\nThe following important assets are missing:\n"
        message += "-- sent_model.json\n" if not assets_status["model"] else ""
        message += "-- sent_model.h5\n" if not assets_status["weights"] else ""
        message += f"\nDownloading from: {url}\n"
        message += "Download size: 835MB.\n\n"
        print(message)

        if not force_download:
            value = input("Would you like to download? [y/n]") if _test_input is None else _test_input
            # Anything other than "y"
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

        # All other conditions, which warrants downloading
        message_3 = "\nDownload in progress...\n"
        message_3 += "This may take quite a while, "
        message_3 += "go grab a coffee and be poetic.\n"
        print(message_3)
        
        with urlopen(url) as contents: # pragma: no cover
            if _test: return contents
            contents = contents.read()
            with ZipFile(BytesIO(contents)) as file:
                file.extractall(cls._data_dir)
                
    
    @classmethod
    def _test_variables(cls) -> Dict[str, str]:
        # Test models for unit testing
        
        module_path = path.dirname(path.realpath(__file__))
        test_model_path = module_path + "/../tests/data/lexical_model_dummy.json"
        test_weights_path = module_path + "/../tests/data/lexical_model_dummy.h5"
        
        return_dict = {"model": test_model_path, "weights": test_weights_path}
        return return_dict


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


    def parse(self, args=None) -> Dict[str, Optional[str]]:
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