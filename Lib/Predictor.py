###################
##### Predict inuputs
###################

## Load necessary modules
from tensorflow import keras
from nltk.tokenize import word_tokenize

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
        score = result[0][0]

        return score

    ## Preprocess the input
    def proprocess(self, input):
        ## Tokenize and to lower
        input = input.lower()
        sent_token = word_tokenize(input)

        if len(sent_token)==0:
            raise Exception("No characters entered. Please try again.")

        ## Word to index
        id_sent = []
        for words in sent_token:
            try:
                self.dict.token2id.get(words) > 0
                id_sent.append(self.dict.token2id.get(words))
            except:
                id_sent.append(0)

        ## Padding
        sent_test = [id_sent]
        sent_test = keras.preprocessing.sequence.pad_sequences(sent_test, maxlen=456)

        return sent_test