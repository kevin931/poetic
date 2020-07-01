###################
##### Predict inuputs
###################

## Load necessary modules
from tensorflow import keras
from nltk.tokenize import word_tokenize, sent_tokenize
from poetry_predictor.results import Diagnostics

class Predictor():

    ## Constructor
    def __init__(self, model=None, dict=None):
        self.model = model
        self.dict = dict

    def predict(self, input, type=["Content", "Path"]):

        ## Check for file path input
        if type == "Path":
            # Load the file
            input = self.file_load(input)

        ## Preprocess the input
        input = self.proprocess(input)
        ## Prediction
        results = self.model.predict(input)
        results = result.tolist()
        score = _Predictions(results, self._sentences)

        return score

    ## Preprocess the input
    def proprocess(self, input):
        ## Tokenize
        sent_token = self.tokenize(input)
        ## Check for errors
        self.check_requirement(sent_token)
        ## To lower case
        sent_test = sent_token.lower()
        ## Word to ID
        id_sent = self.word_id(sent_test)

        ## Padding
        sent_test = keras.preprocessing.sequence.pad_sequences(id_sent, maxlen=456)

        return sent_test

    ## Preprocess files
    def file_load(self, path):
        # Open and read file
        file = open(path, "r", encoding='utf-8')
        file = file.read()

        return file

    ## Sentence and word tokenize
    def tokenize(self, input):
        ## Split into sentences first
        sentences = sent_tokenize(input)
        ## Store tokenized sentence with the class
        self._sentences = sentences
        ## Word tokenize each sentence
        tokens = []
        for sentence in sentences:
            words = word_tokenize(sentence)
            tokens.append(words)
        return tokens

    ## Word to index
    def word_id(self, input):

        ## Sentence First
        id_input = []
        for sentence in input:
            ## Each word in sentence
            id_sent = []
            for words in sentence:
                try:
                    self.dict.token2id.get(words) > 0
                    id_sent.append(self.dict.token2id.get(words))
                except:
                    id_sent.append(0)
            ## Append sentences
            id_input.append(id_sent)

        return(id_input)

    ## Check Input length requirement
    def check_requirement(self,input):
        ## Check empty input
        if len(input)==0:
            raise InputLengthError()

    ## Input length out of bound
    class InputLengthError(Exception):
        def __init__(self):
            message = "Input length out of bound: must be between 1 and 465"
            super().__init__(message)

## Class for Predictor outputs, inheriting from Diagnostics
class _Predictions(Diagnostics):
    def __init__(self, results, sentences):
        ## Process the results into one single list
        results = [prediction[0] for prediction in results]
        ## Call Diagnostics class constructor
        super().__init__(predictions=results, sentences=sentences)