from tensorflow import keras
from nltk.tokenize import word_tokenize, sent_tokenize
from poetry_predictor.results import Diagnostics

class Predictor():
    """
    This is the class to process and predict inputs.

    Attributes:
        model:The pre-trained keras model.
        dict: Gensim dictionary for word IDs.

    Methods:
        predict(input, type=["Content", "Path"])
            Predicts the poetic score of the given input.
        preprocess(input)
            Preprocesses (tokenize, lower case, and pad) the given input.
        tokenize(input)
            Word-tokenizes the given input.
        word_id(input)
            Converts words from tokenized input to indices.
    """

    def __init__(self, model=None, dict=None):
        """
        Parameters:
            model: keras model, optional
                The pre-trained Keras model used to predict poetic scores.
            dict: gensim dictionary, optional
                The dictionary used to convert words to indices.
        """
        self.model = model
        self.dict = dict

    def predict(self, input, type=["Content", "Path"]):
        """
        Predict poetic score from file or direct input.

        Parameters:
            input (str): Text content or file path.
            type (str): "Content" or "Path" for text or file.

        Returns:
            score (float): The predicted scores of given input.
        """

        if type == "Path":
            input = self._file_load(input)

        input = self.preprocess(input)
        results = self.model.predict(input)
        results = results.tolist()
        score = _Predictions(results, self._sentences)

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
            raise InputLengthError()


    class InputLengthError(Exception):
        # Raise error for inproper input length
        def __init__(self):
            message = "Input length out of bound: must be between 1 and 465"
            super().__init__(message)


class _Predictions(Diagnostics):
    # Class for Predictor outputs
    # Inheriting from Diagnostics class

    def __init__(self, results, sentences):
        results = [prediction[0] for prediction in results]
        super().__init__(predictions=results, sentences=sentences)