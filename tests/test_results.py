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
from poetic.results import Diagnostics
from poetic.util import Info

import pytest
from math import isclose
import os
from io import StringIO
import sys
import csv
import warnings


class TestDiagnostics():
    
    @classmethod
    def setup_class(cls):
        predictions = [1, 0, 1, 0]
        cls.results = Diagnostics(predictions)
        cls.five_num = cls.results.five_number(cls.results.predictions)
        
        cls.script_path = os.path.dirname(os.path.realpath(__file__))
        
    
    @pytest.mark.parametrize("func, expected",
                             [(repr, "{'Predictions': [1, 0, 1, 0], 'Sentences': None, 'Diagnostics': None}"),
                              (str, "Diagnostics object for the following predictions: [1, 0, 1, 0]"), 
                              (len, 4)]
                             )  
    def test_str_repr_len_return(self, func, expected):
        output = func(self.results)
        assert output == expected
        
        
    def test_str_long_predictions(self):
        pred_long = [0]*15
        results_long = Diagnostics(pred_long)
        output = str(results_long)
        output = output[len(output)-3:]
        assert output == "..."
        
    
    @pytest.mark.parametrize("func, type",
                             [(repr, str), 
                              (str, str),
                              (len, int)]
                             )         
    def test_repr_str_len_return_type(self, func, type):
        output = func(self.results)
        assert isinstance(output, type)
        
        
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
        

    def test_run_diagnostics_generate_report_return_type(self):
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
        
    
    @pytest.mark.parametrize("file_path, method",
                            [("/data/csv_test_temp.csv", "to_csv"),
                            ("/data/txt_test_temp.txt", "to_file"),
                            ("/data/csv_test_via_txt_temp.csv", "to_file")]
                            )    
    def test_to_csv_to_file(self, file_path, method):
        path = self.script_path + file_path
        getattr(self.results, method)(path)     
        assert os.path.exists(path)
        

    @pytest.mark.parametrize("method", ["to_csv", "to_file"])
    def test_to_csv_and_file_error_message(self, method):
        nonexistant_path = "./nonexistant/a.txt"
        screen_stdout = sys.stdout
        string_stdout = StringIO()
        sys.stdout = string_stdout
        
        try:
            getattr(self.results, method)(nonexistant_path)
        except:
            output = string_stdout.getvalue()
        finally:
            sys.stdout = screen_stdout
            
        expected = "Warning: Unable to open file at designated path."
        assert expected in output
        
    
    @pytest.mark.parametrize("method", ["to_csv", "to_file"])    
    def test_to_csv_and_file_exception_handling(self, method):
        nonexistant_path = "./nonexistant/a.txt"
        try:
            getattr(self.results, method)(nonexistant_path)
        except Exception as e:
            assert isinstance(e, Exception)
        else:
            assert False
            
            
    def test_to_csv_sentences(self):
        path = self.script_path + "/data/csv_test_sentence_temp.csv"
        self.results.sentences = ["This", "is", "a", "test"]
        self.results.to_csv(path)
        
        f = open(path, newline="")
        contents = f.read()
        f.close()
        
        for sentence in self.results.sentences:
            if sentence not in contents:
                assert False
            
        assert True
        
                 
    def test_generate_report_type(self):
        report = self.results.generate_report()
        assert isinstance(report, str)
        
        
    def test_generate_report_contents(self):
        report = self.results.generate_report()
        
        contents = []
        contents.append(Info.version())
        contents.append(str(self.results.diagnostics["Sentence_count"]))
        
        five_number_contents = list(self.results.diagnostics["Five_num"].values())
        five_number_contents = [str(item) for item in five_number_contents]
        contents += five_number_contents
        
        predictions = [str(pred) for pred in self.results.predictions]
        contents += predictions
        
        for item in contents:
            if item not in report:
                assert False
                
        assert True

        
    def test_five_number_deprecation_warning(self):
        
        screen_stderr = sys.stderr
        string_stderr = StringIO()
        sys.stderr = string_stderr
        
        Diagnostics.five_number(input = [1, 0, 1, 0])
        output = string_stderr.getvalue()

        sys.stderr = screen_stderr
        
        expected = "The 'input' parameter is deprecated"
        assert expected in output
        
        
    def test_five_number_type_error(self):
        try:
            Diagnostics.five_number()
        except Exception as e:
            isinstance(e, TypeError)
        else:
            assert False
        
        
    def test_five_number_deprecated_input(self):
        result = Diagnostics.five_number(input = [1, 0, 1, 0])
        expected = {"Min": 0, "Mean": 0.5, "Median": 0.5, "Stdev": 0.5, "Max": 1}
        assert result == expected
        
           
    @classmethod   
    def teardown_class(cls):
        os.remove(cls.script_path + "/data/csv_test_temp.csv")
        os.remove(cls.script_path + "/data/txt_test_temp.txt")
        os.remove(cls.script_path + "/data/csv_test_via_txt_temp.csv")
        os.remove(cls.script_path + "/data/csv_test_sentence_temp.csv")