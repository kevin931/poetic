from poetic.predictor import Predictor
import poetic
from tensorflow import keras
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

    def test_predict_type(self):
        score = self.pred.predict("This is a test.")
        assert isinstance(score, poetic.predictor.Predictions)

    def test_file_load(self):
        path = self.script_path + "/data/file_test.txt"
        file = self.pred._file_load(path)
        assert file == "This is just a test."

    def test_file_predict(self):
        score = self.pred.predict_file(self.script_path +"/data/file_test.txt")
        score = score.predictions[0]
        assert score >= 0 and score <= 1
        
    def test_string_predict(self):
        score = self.pred.predict("This is just a test.")
        score = score.predictions[0]
        assert score >= 0 and score <= 1