#####################
### Loading the necessary files
#####################

## Import necessary module
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
    Provide the basic information of the package.

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

        VERSION = "0.2.0"
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

    # Package data directory
    _data_dir = pkg_resources.resource_filename("poetic", "data/")

    @classmethod
    def initialize(cls):
        ## Command-line arguments arguments
        arguments = _Arguments()
        arguments = arguments._parse()

        ## Load dictionary and model
        model = cls.load_model()
        dict = cls.load_dict()

        return arguments, model, dict

    @staticmethod
    def load_dict():
        word_dictionary = gs.corpora.Dictionary.load_from_text(fname="./data/word_dictionary_complete.txt")
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
    def download_assets(self):
        url = "https://github.com/kevin931/MeterOMeter/archive/v.0.1.2.zip"
        with urlopen(url) as contents:
            contents = contents.read()
            with ZipFile(BytesIO(contents)) as file:
                file.extractall()

## Parsing arguments
class _Arguments():
    ## Constructor
    def __init__(self):
        ## New Parser
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
        arguments = self.parser.parse_args()
        arguments = vars(arguments)

        ## Check for error
        if arguments["Sentence"] is not None and arguments["File"] is not None:
            raise UnsupportedConfigError()

        return arguments

    def _version(self):
        """Format the command-line version output"""

        v = "Poetry Predictor "
        v += Info.version() + " "
        v += Info.build_status()

        return v

    class UnsupportedConfigError(Exception):
        def __init__(self):
            message_1 = "Unsupported combination: Unable to process sentence and file in one operation.\n"
            message_2 = "For help, please run with '-h' tag."
            super().__init__(message)