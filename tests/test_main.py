from poetic.__main__ import main

import pytest
from io import StringIO
import sys
import os

class TestMain():
    
    @classmethod
    def setup_class(cls):
        cls.script_path = os.path.dirname(os.path.realpath(__file__))
        os.mkdir(cls.script_path + "/data/temp")

    
    def test_main_return_none(self):
        result = main(_test=True, _test_args="") #pylint: disable=assignment-from-no-return
        assert result is None
        
    
    @pytest.mark.parametrize("arguments,expected",
                             [(["-s", "This is just a test"], "Diagnostics Report"),
                             (["-f", "./tests/data/file_test.txt"], "Diagnostics Report"),
                             (["-f", "./tests/data/file_test.txt", "--GUI"], "Test GUI launch"),
                             (["-s", "This is just a test", "--GUI"], "Test GUI launch"),
                             (["--GUI"], "Test GUI launch"),
                             ("", "Test GUI launch")]
                             )
    def test_main_cli_parameters_sentence_file_gui(self, arguments, expected):
        screen_stdout = sys.stdout
        string_stdout = StringIO()
        sys.stdout = string_stdout
        
        main(_test=True, _test_args=arguments)
            
        output = string_stdout.getvalue()
        sys.stdout = screen_stdout
        
        assert expected in output
        
    
    @pytest.mark.parametrize("arguments,",
                            [(["-s", "This is just a test", "-o", "./tests/data/temp/test_s.txt"], ),
                            (["-f", "./tests/data/file_test.txt", "-o", "./tests/data/temp/test_s_f.txt"], )]
                            )    
    def test_main_cli_parameters_save_file(self, arguments):
        arguments, = arguments
        main(_test=True, _test_args=arguments)
        assert os.path.exists(arguments[3])
        
    
    @classmethod
    def teardown_class(cls):
        files = os.listdir(cls.script_path + "/data/temp/")
        for file in files:
            os.remove(cls.script_path + "/data/temp/" + file)
        os.rmdir("./tests/data/temp")