from poetic.results import Diagnostics

import pytest
from math import isclose
import os


class TestDiagnostics():
    
    @classmethod
    def setup_class(cls):
        predictions = [1, 0, 1, 0]
        cls.results = Diagnostics(predictions)
        cls.five_num = cls.results.five_number(cls.results.predictions)
        
        cls.script_path = os.path.dirname(os.path.realpath(__file__))
        
    
    def test_str_type(self):
        output = str(self.results)
        assert isinstance(output, str)
        
    
    def test_str_return(self):
        output = str(self.results)
        expected = "Diagnostics object for the following predictions: [1, 0, 1, 0]"
        assert output == expected
        
        
    def test_repr_type(self):
        output = repr(self.results)
        assert isinstance(output, str)
        
    
    def test_repr_return(self):
        output = repr(self.results)
        expected = "{'Predictions': [1, 0, 1, 0], 'Sentences': None, 'Diagnostics': None}"
        assert output == expected
        
        
    def test_len_type(self):
        length = len(self.results)
        assert isinstance(length, int)
        
        
    def test_len_return(self):
        length = len(self.results)
        assert length == 4
        
        
    def test_five_number_type(self):
        assert isinstance(self.five_num, dict)
        
        
    @pytest.mark.parametrize("key, expected",
                             [("Min", 0),
                             ("Mean", 0.5),
                             ("Median", 0.5),
                             ("Stdev", 0.5),
                             ("Max", 1)]
                             )
    def test_five_number(self, key, expected):
        result = self.five_num[key]
        assert isclose(result, expected)
        
        
    def test_run_diagnostics_type(self):
        self.results.run_diagnostics()
        assert isinstance(self.results.diagnostics, dict)
        
        
    def test_diagnostics_keys(self):
        stats = self.results.diagnostics
        keys = list(stats.keys())
        expected = ["Sentence_count", "Five_num", "Predictions"]
        assert keys == expected
        
    
    @pytest.mark.parametrize("key, expected",
                            [("Sentence_count", 4),
                            ("Predictions", [1,0,1,0])]
                            )
    def test_diagnostics(self, key, expected):
        stats = self.results.diagnostics
        assert stats[key] == expected
        
        
    def test_to_csv(self):
        path = self.script_path + "/data/csv_test_temp.csv"
        self.results.to_csv(path)       
        assert os.path.exists(path)
        
        
    def test_to_file(self):
        path = self.script_path + "/data/txt_test_temp.txt"
        self.results.to_csv(path)       
        assert os.path.exists(path)
        
        
    def test_to_file_csv_parse(self):
        path = self.script_path + "/data/csv_test_via_txt_temp.txt"
        self.results.to_csv(path)       
        assert os.path.exists(path)
        
             
    def test_generate_report_type(self):
        report = self.results.generate_report()
        assert isinstance(report, str)
        
    
    @classmethod   
    def teardown_class(cls):
        os.remove(cls.script_path + "/data/csv_test_temp.csv")
        os.remove(cls.script_path + "/data/txt_test_temp.txt")
        os.remove(cls.script_path + "/data/csv_test_via_txt_temp.txt")