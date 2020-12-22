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

class TestPredictor():
    # Class to test the Predictor Class

    @classmethod
    def setup_class(cls):
        poetic.util.Info(_test=True)
        
        cls.script_path = os.path.dirname(os.path.realpath(__file__))
        cls.pred = Predictor()
        

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
    def test_input_length_error_check(self, method, param):
        try:
            getattr(self.pred, method)(param)
        except Exception as e:
            assert isinstance(e, poetic.exceptions.InputLengthError)
    
            
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
        
        
    def test_preprocess_custom_length(self, mocker):
        mocker.patch("poetic.predictor.keras.Model.input_shape", (None, 300))
        processed = self.pred.preprocess("This is just a test. Hi.")
        processed = [len(processed), len(processed[0])]
        expected = [2, 300]
        assert processed == expected
        
    
    @pytest.mark.parametrize("input_shape",
                             [(1,2), (1, 2, 3)]
                             )
    def test_unsupported_model_error_handling(self, mocker, input_shape):
        mocker.patch("poetic.predictor.keras.Model.input_shape", input_shape)
        try:
            Predictor()
        except poetic.exceptions.ModelShapeError:
            assert True
        except Exception:
            assert False
        else:
            assert False
            
            
    @classmethod
    def teardown_class(cls):
        info_instance = poetic.util.Info.get_instance()
        info_instance._destructor()
        del info_instance