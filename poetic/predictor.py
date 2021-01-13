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
""" Making poetic predictions using models.

The predictor module provides interfaces for poetry predictions with
the Predictor class. To make prediction, an instance of the
Predictor is needed with the necessary model and gensim
dictionary is needed.

Examples:
    The most common use case for the predictor module is with its default settings.
    To make a prediction with string, below is an example:
    
    .. code-block:: python
    
        import poetic
    
        pred = poetic.Predictor()
        result = pred.predict("This is an example.")
        
    To make a prediction with a text file, use the following codes:
    
    .. code-block:: python
    
        import poetic
    
        pred = poetic.Predictor()
        result = pred.predict_file("<PATH>")
"""

from tensorflow import keras
from gensim.corpora.dictionary import Dictionary
from tensorflow.python.keras.engine.training import Model # pylint: disable=no-name-in-module, import-error
from nltk.tokenize import word_tokenize, sent_tokenize
from poetic.results import Diagnostics
from poetic.util import Initializer
from poetic import exceptions

from typing import Optional, Union, List
import numpy


class Predictor():
    """
    The :code:`Predictor()` class processes and predicts inputs for poetic scores. It can be used
    as the single interface of the package with other modules built as helpers. 
    
    Args:
        model (tensorflow.keras.Model, optional): 
            A pre-trained keras model. The default model will be loaded if no model is
            supplied. If a custom model is supplied, a custom gensim dictionary is recommended
            for it to work correctly although not strictly enforced.
        dict (gensim.corpora.dictionary.Dictionary, optional): 
            Gensim dictionary for word IDs. If nothing is supplied, the default dictionary
            will be loaded. The default dictionary will be required for the the default
            model to work correctly although it is not strictly enforced.
        force_download_assets (bool, optional):
            Wheher to download assets (the default models) without asking/user input.


    Attributes:
        model (tensorflow.keras.Model): The pre-trained keras model.
        dict (gensim.corpora.dictionary.Dictionary): Gensim dictionary for word IDs.
        force_download_assets (bool): Wheher to download assets without asking.

    """


    def __init__(self, 
                 model: Optional["tensorflow.keras.Model"]=None, 
                 dict: Optional["gensim.corpora.dictionary.Dictionary"]=None, 
                 force_download_assets: Optional[bool]=False) -> None:

        self.model = model if model is not None else Initializer.load_model(force_download=force_download_assets)
        self.dict = dict if dict is not None else Initializer.load_dict()
        self._sentences = None


    def predict(self, input: str) -> "Predictions":
        """
        Predict poetic score from string.

        Parameters:
            input (str): Text content to be predicted.

        Returns:
            Predictions: 
                A Predictions object with predicted scores of the given input.
                
        Raises:
            poetic.exceptions.InputLengthError: Error for processing input length of zero.
        """

        input = self.preprocess(input)
        results = self.model.predict(input)
        results = results.tolist()
        score = Predictions(results, self._sentences)

        return score


    def predict_file(self, path: str) -> "Predictions":
        """
        Predict poetic score from file.

        This method essentially loads the text file into a string
        of text and then calls the predict method.

        Parameters:
            path (str): The path to the text file.

        Returns:
            Predictions: A Predictions object with predicted scores of the given input.
            
        Raises:
            poetic.exceptions.InputLengthError: Error for processing empty file, resulting in input
                length of zero.
        """

        input = self._file_load(path)
        score = self.predict(input)

        return score


    def preprocess(self, input: str) -> numpy.ndarray:
        """
        Preprocess inputs: tokenize, to lower, and padding.

        Parameters:
            input (str):
                Text either in a single string or a list of strings.

        Returns:
            numpy.ndarray: A 2-d numpy array of processed inputs.
            
        Raises:
            poetic.exceptions.InputLengthError: Error for processing input length of zero.
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


    def _file_load(self, path: str) -> str:
        # Open a specified file.
        # Method used for accepting file input.

        file = open(path, "r", encoding='utf-8')
        file = file.read()

        return file


    def tokenize(self, input: str) -> List[List[str]]:
        """
        Tokenize text input into sentences and then words.

        Parameters:
            input (str): A string or list of strings of text.

        Returns:
            list(str): A 2-d list of tokenized words.
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


    def word_id(self, input: List[List[str]]) -> List[List[int]]:
        """
        Convert tokenized words to word IDs using a gensim dictionary.

        Parameters:
            input (list): A 2-d list of tokenized words.

        Returns:
            list: A 2-d list of word ids.
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


    def _check_requirement(self,input: List[List[str]]) -> None:
        if len(input)==0:
            message = "Input length out of bound: must be between 1 and 465"
            raise exceptions.InputLengthError(message)



class Predictions(Diagnostics):
    """Class for prediction results from Predictor class.

    This class inherets from ``Diagnostics`` class of the ``results`` module,
    and it is intended for being internally called by the Predictor class.
    To directly access the Diagnostics class's functionality, use it instead.
    
    Args:
        results (list(list(float))): 
            The prediction results predicted with Keras models.
        sentences (list(str), optional): 
            A list of strings to represent tokenized sentences predicted by the ``Predictor``
            class.

    Attributes:
        predictions (list): Predictions of poetic scores.
        sentences (list): Sentences associated with the predictions.
        diagnostics(dict): A dictionary of diagnostics statistics,
            including sentence count, five number summary, and the predictions themselves.
             
        """

    def __init__(self, results: List[List[float]], sentences: Optional[List[str]]) -> None:
        results = [prediction[0] for prediction in results]
        super().__init__(predictions=results, sentences=sentences)