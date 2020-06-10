#####################
### Loading the necessary files
#####################

## Import necessary module
from tensorflow import keras
import gensim as gs

class Initialize():

    def load_dict(self):
        word_dictionary = gs.corpora.Dictionary.load_from_text(fname="./Models/word_dictionary_complete.txt")
        return word_dictionary

    def load_model(self):
        json_file = open('./Models/sent_model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        sent_model = keras.models.model_from_json(loaded_model_json)
        # load weights into new model
        sent_model.load_weights("./Models/sent_model.h5")

        return sent_model