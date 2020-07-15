#####################
### Loading the necessary files
#####################

## Import necessary module
from tensorflow import keras
import gensim as gs
import argparse

class Initializer():

    @classmethod
    def initialize(cls):
        ## Command-line arguments arguments
        arguments = Arguments()
        arguments = arguments.parse()

        ## Load dictionary and model
        model = cls.load_model()
        dict = cls.load_dict()

        return arguments, model, dict

    @staticmethod
    def load_dict():
        word_dictionary = gs.corpora.Dictionary.load_from_text(fname="./data/word_dictionary_complete.txt")
        return word_dictionary

    @staticmethod
    def load_model():
        json_file = open('./data/sent_model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        sent_model = keras.models.model_from_json(loaded_model_json)
        # load weights into new model
        sent_model.load_weights("./data/sent_model.h5")
        return sent_model

## Parsing arguments
class Arguments():
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
        self.parser.add_argument("--version", action="version", version="Poetry Predictor 0.2.0 alpha")

    def parse(self):
        arguments = self.parser.parse_args()
        arguments = vars(arguments)

        ## Check for error
        if arguments["Sentence"] is not None and arguments["File"] is not None:
            raise UnsupportedConfigError()

        return arguments

    class UnsupportedConfigError(Exception):
        def __init__(self):
            message_1 = "Unsupported combination: Unable to process sentence and file in one operation.\n"
            message_2 = "For help, please run with '-h' tag."
            super().__init__(message)