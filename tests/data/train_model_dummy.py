import numpy as np
import tensorflow as tf
from tensorflow import keras
import gensim as gs
import os

script_path = os.path.dirname(os.path.realpath(__file__))

# Load Dictionary
dict_dir = script_path + "/../../poetic/data/word_dictionary_complete.txt"
dictionary = gs.corpora.Dictionary.load_from_text(fname=dict_dir)
# Training set
lexical_train = np.random.randint(0, max(dictionary.keys()), 456)
lexical_train = lexical_train.reshape(1, 456)
# Testing set
label_train = np.array([0])

# Training Lexical Model
model_lexical_input = keras.layers.Input(shape = (456, ))
model_lexical_output = keras.layers.Dense(1, activation="sigmoid")(model_lexical_input)

lexical_model = keras.models.Model(inputs = model_lexical_input, outputs = model_lexical_output)
lexical_model.compile(optimizer = "adam", loss="binary_crossentropy", metrics = ["accuracy"])
lexical_model.fit(x = lexical_train, y = label_train, epochs= 1, batch_size = 1)

# serialize model to JSON
lexical_model_json = lexical_model.to_json()
with open(script_path + "/lexical_model_dummy.json", "w") as json_file:
    json_file.write(lexical_model_json)
# serialize weights to HDF5
lexical_model.save_weights(script_path + "/lexical_model_dummy.h5")