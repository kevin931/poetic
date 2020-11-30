from poetic.predictor import Predictor
import poetic

from tensorflow import keras
import numpy as np
import os

class TestPredictor():
    # Class to test the Predictor Class

    @classmethod
    def setup_class(cls):
        # File paths
        cls.script_path = os.path.dirname(os.path.realpath(__file__))
        model_dir = cls.script_path + "/data/lexical_model_dummy.json"
        weights_dir = cls.script_path + "/data/lexical_model_dummy.h5"
        # Load model and weights
        json_file = open(model_dir, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = keras.models.model_from_json(loaded_model_json)
        model.load_weights(weights_dir)

        # Initiate Predictor
        cls.pred = Predictor(model=model)


    def test_word_id_type(self):
        id = self.pred.word_id([["you"]])
        assert isinstance(id, list)


    def test_word_id(self):
        id = self.pred.word_id([["you"]])
        assert id[0][0] == 141


    def test_file_load(self):
        path = self.script_path + "/data/file_test.txt"
        file = self.pred._file_load(path)
        assert file == "This is just a test."
        
        
    def test_predict_type(self):
        score = self.pred.predict("This is a test.")
        assert isinstance(score, poetic.predictor.Predictions)
 
        
    def test_predict_type_inheritance(self):
        score = self.pred.predict("This is a test.")
        assert isinstance(score, poetic.results.Diagnostics)


    def test_file_predict(self):
        score = self.pred.predict_file(self.script_path +"/data/file_test.txt")
        score = score.predictions[0]
        assert score >= 0 and score <= 1
        
        
    def test_string_predict(self):
        score = self.pred.predict("This is just a test.")
        score = score.predictions[0]
        assert score >= 0 and score <= 1
      
        
    def test_input_length_check(self):
        try:
            self.pred.predict("")
        except Exception as e:
            assert isinstance(e, poetic.exceptions.InputLengthError)
       
            
    def test_check_requirement(self):
        try:
            self.pred._check_requirement([])
        except Exception as e:
            assert isinstance(e, poetic.exceptions.InputLengthError)
    
            
    def test_tokenize(self):
        tokens = self.pred.tokenize("This is just a test. Hi.")
        expected = [["This", "is", "just", "a", "test", "."], ["Hi", "."]]
        assert tokens == expected
   
        
    def test_tokenize_type(self):
        tokens = self.pred.tokenize("This is just a test.")
        assert isinstance(tokens, list)
        
        
    def test_preprocess_type(self):
        processed = self.pred.preprocess("This is just a test.")
        assert isinstance(processed, np.ndarray)
        
        
    def test_preprocess_length(self):
        processed = self.pred.preprocess("This is just a test. Hi.")
        processed = [len(processed), len(processed[0])]
        expected = [2, 456]
        assert processed == expected