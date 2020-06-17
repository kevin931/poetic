###################
##### Predict inuputs
###################

## Load necessary modules
from tensorflow import keras
from nltk.tokenize import word_tokenize, sent_tokenize

class Predictor():

    ## Constructor
    def __init__(self, model=None, dict=None):
        self.model = model
        self.dict = dict

    def predict(self, input):
        ## Preprocess the input
        input = self.proprocess(input)

        result = self.model.predict(input)
        result = result.tolist()
        score = result

        return score

    ## Preprocess the input
    def proprocess(self, input):
        ## Tokenize and to lower
        input = input.lower()
        sent_token = self.tokenize(input)
        ## Check for errors
        self.check_requirement(sent_token)
        ## Word to ID
        id_sent = self.word_id(sent_token)

        ## Padding
        sent_test = keras.preprocessing.sequence.pad_sequences(id_sent, maxlen=456)

        return sent_test

    ## Sentence and word tokenize
    def tokenize(self, input):
        ## Split into sentences first
        sentences = sent_tokenize(input)

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
            raise InputLengthException()

    ## Input length out of bound
    class InputLengthException(Exception):
        def __init__(self):
            message = "Input length out of bound: must be between 1 and 465"
            super().__init__(message)