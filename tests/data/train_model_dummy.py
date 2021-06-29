# Package: poetic (poetic-py)
# Author: Kevin Wang
#
# The MIT License (MIT)
#
# Copyright 2020 Kevin Wang
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
import numpy as np
import tensorflow as tf
from tensorflow import keras #type: ignore
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