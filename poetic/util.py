"""Module for package utility.

This module includes the necessary functionalities to load and
download assets for other module in the package and provide basic
information for the current build and version of the package.

Classes:
    Info(): Provides the basic information of the package.
    Initializer(): Initializes core components of the package.

"""

from tensorflow import keras
import gensim as gs

from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO

from os import path
import argparse
import pkg_resources

class Info():
    """
    Provides the basic information of the package.

    Methods:
        version(): Returns the current version of the package.
        build_status(): Returns the current build status.
    """

    @staticmethod
    def version():
        """
        A single method to return the version of the package.

        Returns:
            VERSION (str): The current version of the package.
        """

        VERSION = "1.0.0b1"
        return VERSION

    @staticmethod
    def build_status():
        """
        Get the build status of the current version.

        Returns:
            BUILD (str): The build status of the current version.
        """

        BUILD = "Dev"
        return BUILD

class Initializer():
    """Initializes core components of the package.

    The Initializer is core part of Poetic that loads and
    downloads models and other necessary assets. It also
    facilitates the command line mode by interacting with
    the _Arguments class.

    Methods:
        initialize():
            Initializes the package with all necessities.
        load_dict():
            Loads the gensim disctionary.
        load_model():
            Loads the Keras model and its weights.
        download_assets():
            Download the Keras model and its weights.
    """

    # Package data directory
    _data_dir = pkg_resources.resource_filename("poetic", "data/")

    @classmethod
    def initialize(cls):
        """Initializes the package.

        This methods checks for any command line arguments,
        and then loads both the gensim dictionary and the
        Keras model with its weights.

        Returns:
            arguments (dict):
                A dictionary of commandline arguments.
            model (tensorflow.python.keras.engine.training.Model, optional):
                A pre-trained Keras model with its weights loaded.
            word_dictionary (gensim.corpora.dictionary.Dictionary):
                A gensim dictionary.

        """

        arguments = _Arguments()
        arguments = arguments._parse()

        model = cls.load_model()
        word_dictionary = cls.load_dict()

        return arguments, model, word_dictionary

    @classmethod
    def load_dict(cls):

        """Loads gensim dictionary.

        Returns:
            word_dictionary (gensim.corpora.dictionary.Dictionary):
                A gensim dictionary.

        """
        dir = cls._data_dir + "word_dictionary_complete.txt"
        word_dictionary = gs.corpora.Dictionary.load_from_text(fname=dir)
        return word_dictionary

    @classmethod
    def load_model(cls):
        """Load Keras models.

        This method uses Keras interface to load the previously
        trained models, which are necessary for the Predictor and
        the GUI.

        Returns:
            model (tensorflow.python.keras.engine.training.Model): Pretrained Keras model

        """
        weights_dir = cls._data_dir+"sent_model.h5"
        model_dir = cls._data_dir+"sent_model.json"

        model_status = not path.exists(model_dir)
        weights_status = not path.exists(weights_dir)
        if model_status and weights_status:
            cls.download_assets()

        json_file = open(model_dir, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = keras.models.model_from_json(loaded_model_json)
        # load weights into new model
        model.load_weights(weights_dir)
        return model

    @classmethod
    def download_assets(cls):
        """Method to download models.

        This method downloads models from the poetic-models
        github repository. Explicitly calling this method will
        initiate a download regardless of whether the model has
        previously been downloaded. Under usual circumstances,
        other functions will download the models automatically.

        """

        url = "https://github.com/kevin931/poetic-models/releases/download/v0.1-alpha/sent_model.zip"

        # Downloading and unzipping
        with urlopen(url) as contents:
            contents = contents.read()
            with ZipFile(BytesIO(contents)) as file:
                file.extractall(cls._data_dir)


class _Arguments():
    # This class parses command line arguments.

    def __init__(self):
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
        self.parser.add_argument("--version", action="version", version=self._version())

    def _parse(self):
        # Parse arguments

        arguments = self.parser.parse_args()
        arguments = vars(arguments)
        # Check for error
        if arguments["Sentence"] is not None and arguments["File"] is not None:
            raise UnsupportedConfigError()

        return arguments

    def _version(self):
        # Format the command-line version output

        v = "Poetry Predictor "
        v += Info.version() + " "
        v += Info.build_status()

        return v

    class UnsupportedConfigError(Exception):
        def __init__(self):
            message_1 = "Unsupported combination: Unable to process sentence and file in one operation.\n"
            message_2 = "For help, please run with '-h' tag."
            super().__init__(message)