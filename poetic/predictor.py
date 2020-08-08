"""Module for poetry predictions.

This module provides interfaces for poetry predictions with
the Predictor class. To make prediction, an instance of the
Predictor is needed with the necessary model and gensim
dictionary is needed.

Classes:
    Predictor(model, dict): Class for making predictions.
"""

from tensorflow import keras
from nltk.tokenize import word_tokenize, sent_tokenize
from poetic.results import Diagnostics
from poetic.util import Initializer
from poetic import exceptions

class Predictor():
    """
    This is the class to process and predict inputs.

    Attributes:
        model (tensorflow.python.keras.engine.training.Model, optional):
            The pre-trained keras model.
        dict (gensim.corpora.dictionary.Dictionary, optional):
            Gensim dictionary for word IDs.

    Methods:
        predict(input)
            Predicts the poetic score of the given input.
        predict_file(file)
            Predicts the poetic score from a text file.
        preprocess(input)
            Preprocesses (tokenize, lower case, and pad) the given input.
        tokenize(input)
            Word-tokenizes the given input.
        word_id(input)
            Converts words from tokenized input to indices.
    """

    def __init__(self, model=None, dict=None, force_download_assets=False):
        """
        Parameters:
            model (tensorflow.python.keras.engine.training.Model, optional):
                The pre-trained Keras model used to predict poetic scores.
            dict (gensim.corpora.dictionary.Dictionary, optional):
                The dictionary used to convert words to indices.
            force_download_assets (bool, optional):
                A boolean value on whether the util module's load_model()
                funtion will download the assets for the model without
                asking. If the model parameter is supplied, this parameter
                is effectively ignored.
        """

        self.model = model if model is not None else Initializer.load_model(force_download=force_download_assets)
        self.dict = dict if dict is not None else Initializer.load_dict()
        self._sentences = None

    def predict(self, input):
        """
        Predict poetic score from file.

        Parameters:
            input (str): Text content to be predicted.

        Returns:
            score (list): The predicted scores of the given input.
        """

        input = self.preprocess(input)
        results = self.model.predict(input)
        results = results.tolist()
        score = _Predictions(results, self._sentences)

        return score

    def predict_file(self, path):
        """
        Predict poetic score from file.

        This method essentially loads the text file into a string
        of text and then calls the predict method.

        Parameters:
            path (str): The path to the text file.

        Returns:
            score (list): The predicted scores of the contents of the file.
        """

        input = self._file_load(path)
        score = self.predict(input)

        return score

    def preprocess(self, input):
        """
        Preprocess inputs: tokenize, to lower, and padding.

        Parameters:
            input (str):
                Text either in a single string or a list of strings.

        Returns:
            sent_test (list): A 2-d list of processed inputs.
        """

        sent_token = self.tokenize(input)

        self._check_requirement(sent_token)

        sent_lower = []
        for sentence in sent_token:
            word_lower = [word.lower() for word in sentence]
            sent_lower.append(word_lower)

        id_sent = self.word_id(sent_lower)

        sent_test = keras.preprocessing.sequence.pad_sequences(id_sent, maxlen=456)

        return sent_test

    def _file_load(self, path):
        # Open a specified file.
        # Method used for accepting file input.

        file = open(path, "r", encoding='utf-8')
        file = file.read()

        return file

    def tokenize(self, input):
        """
        Tokenize text input into sentences and then words.

        Parameters:
            input (str): A string or list of strings of text.

        Returns:
            tokens (list): A 2-d list of tokenized words.
        """

        # Sentence tokenization
        sentences = sent_tokenize(input)
        self._sentences = sentences

        # Word tokenize
        tokens = []
        for sentence in sentences:
            words = word_tokenize(sentence)
            tokens.append(words)
        return tokens


    def word_id(self, input):
        """
        Convert tokenized words to word IDs using a gensim dictionary.

        Parameters:
            input (list): A 2-d list of tokenized words.

        Returns:
            id_input (list): A 2-d list of word ids.
        """

        id_input = []
        for sentence in input:
            id_sent = []
            for word in sentence:
                try:
                    self.dict.token2id.get(word) > 0
                    id_sent.append(self.dict.token2id.get(word))
                except:
                    id_sent.append(0)
            id_input.append(id_sent)

        return(id_input)

    def _check_requirement(self,input):
        #Check empty input
        if len(input)==0:
            message = "Input length out of bound: must be between 1 and 465"
            raise exceptions.InputLengthError(message)


class _Predictions(Diagnostics):
    # Class for Predictor outputs
    # Inheriting from Diagnostics class

    def __init__(self, results, sentences):
        results = [prediction[0] for prediction in results]
        super().__init__(predictions=results, sentences=sentences)