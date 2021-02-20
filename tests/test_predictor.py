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
from poetic.predictor import Predictor
import poetic

from tensorflow import keras
import numpy as np
import os
import pytest
import sys
from io import StringIO

class TestPredictor():
    # Class to test the Predictor Class

    @classmethod
    def setup_class(cls):
        poetic.util.Info(_test=True)
        
        cls.script_path = os.path.dirname(os.path.realpath(__file__))
        cls.model = poetic.util.Initializer.load_model(
            model_path="./tests/data/lexical_model_dummy.json",
            weights_path="./tests/data/lexical_model_dummy.h5"
        )
        cls.pred = Predictor(model=cls.model)
        

    def test_word_id_type(self):
        id = self.pred.word_id([["you"]])
        assert isinstance(id, list)


    @pytest.mark.parametrize("word, expected_id",
                             [("you", 141), 
                              ("this_is_a_test", 0)]
                             )
    def test_word_id(self, word, expected_id):
        word_id = self.pred.word_id([[word]])
        assert word_id[0][0] == expected_id


    def test_file_load(self):
        path = self.script_path + "/data/file_test.txt"
        file = self.pred._file_load(path)
        assert file == "This is just a test."
        
    
    @pytest.mark.parametrize("return_type",
                             [poetic.predictor.Predictions, 
                              poetic.results.Diagnostics]
                             )
    def test_predict_type(self, return_type):
        score = self.pred.predict("This is a test.")
        assert isinstance(score, return_type)


    def test_file_predict(self):
        score = self.pred.predict_file(self.script_path +"/data/file_test.txt")
        score = score.predictions[0]
        assert score >= 0 and score <= 1
        
        
    def test_string_predict(self):
        score = self.pred.predict("This is just a test.")
        score = score.predictions[0]
        assert score >= 0 and score <= 1

      
    @pytest.mark.parametrize("method, param",
                             [("predict", ""),
                              ("_check_requirement", [])]
                             )    
    def test_input_length_error_emmpty_check(self, method, param):
        try:
            getattr(self.pred, method)(param)
        except Exception as e:
            message = "Input length out of bound: must be between 1 and {}".format(self.pred.model.input_shape[1])
            assert str(e) == message
            assert isinstance(e, poetic.exceptions.InputLengthError)
        else:
            assert False
            
            
    def test_tokenize(self):
        tokens = self.pred.tokenize("This is just a test. Hi.")
        expected = [["This", "is", "just", "a", "test", "."], ["Hi", "."]]
        assert tokens == expected
   
    
    @pytest.mark.parametrize("method, return_type",
                             [("tokenize", list), 
                              ("preprocess", np.ndarray)]
                             )   
    def test_tokenize_preprocess_return_type(self, method, return_type):
        tokens = self.pred.tokenize("This is just a test.")
        assert isinstance(tokens, list)
        
        
    def test_preprocess_default_length(self):
        processed = self.pred.preprocess("This is just a test. Hi.")
        processed = [len(processed), len(processed[0])]
        expected = [2, 456]
        assert processed == expected
        
    
    @pytest.mark.parametrize("input_shape",
                             [(1,2), (1, 2, 3)]
                             )
    def test_unsupported_model_error_handling(self, mocker, input_shape):
        model_mock = mocker.MagicMock()
        model_mock.input_shape = input_shape
        mocker.patch("poetic.predictor.Initializer.load_model", return_value = model_mock)
        
        try:
            Predictor()
        except poetic.exceptions.ModelShapeError:
            assert True
        except Exception:
            assert False
        else:
            assert False

            
    @pytest.mark.parametrize("method", ["predict", "preprocess", "tokenize", "word_id"])        
    def test_lexical_input_none_type_error(self, method):
        try:
            getattr(self.pred, method)()
        except Exception as e:
            assert isinstance(e, TypeError)
        else:
            assert False
            
    
    @pytest.mark.parametrize("method, parameter", 
                             [("predict", "This is a test."), 
                              ("preprocess", "This is a test."), 
                              ("tokenize", "This is a test."), 
                              ("word_id", [["this", "is"]])])  
    def test_input_deprecation_warning(self, mocker, method, parameter):

        warn_mocker = mocker.MagicMock()
        mocker.patch("poetic.results.warnings.warn", warn_mocker)
        getattr(self.pred, method)(input=parameter)
        warn_mocker.assert_called()
        
        
    def test_constructor_(self, mocker):
        
        warn_mocker = mocker.MagicMock()
        mocker.patch("poetic.results.warnings.warn", warn_mocker)
        dictionary = poetic.util.Initializer.load_dict()
        Predictor(model=self.model, dict=dictionary)
        warn_mocker.assert_called()
    
    
    @classmethod
    def teardown_class(cls):
        info_instance = poetic.util.Info.get_instance()
        info_instance._destructor()
        del info_instance