import warnings
warnings.filterwarnings("ignore")


import numpy as np
import tensorflow as tf
from tensorflow import keras
import gensim as gs
from nltk.tokenize import word_tokenize

json_file = open('./Models/sent_model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
sent_model = keras.models.model_from_json(loaded_model_json)
# load weights into new model
sent_model.load_weights("./Models/sent_model.h5")

print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


print("This is the Meter-O-Meter Project.\nThis programs classifies poetry.")


while True:

    input_sentence = input("\n\n\nWhat is your sentence? ")

    if input_sentence == "Bivin Sadler" or input_sentence == "Tim Cassedy":
        print("This is STATE-OF-THE-ART POETRY. PEFECTION!!")
        continue

    sent_token = word_tokenize(input_sentence)
    sent_lower = []
    for words in sent_token:
        sent_lower.append(words.lower())

    word_dictionary = gs.corpora.Dictionary.load_from_text(fname="./Models/word_dictionary_complete.txt")

    id_sent = []
    for words in sent_lower:
        try:
            word_dictionary.token2id.get(words) > 0
            id_sent.append(word_dictionary.token2id.get(words))
        except:
            id_sent.append(0)

    sent_train = [id_sent]

    sent_train = keras.preprocessing.sequence.pad_sequences(sent_train, maxlen=456)

    result = sent_model.predict(sent_train)
    result = result.tolist()

    score = result[0][0]

    if score > 0.5 :
        print("\nThis sentence is POETRY.\nThe poetic score is " + str(score))

    else:
        print("\nThis sentence is NOT POETRY.\nThe poetic score is " + str(score))
