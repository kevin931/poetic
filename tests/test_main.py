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
from poetic.__main__ import main
from poetic.util import Info

import pytest
from io import StringIO
import sys
import os

class TestMain():
    
    @classmethod
    def setup_class(cls):
        Info(_test=True)   
        cls.script_path = os.path.dirname(os.path.realpath(__file__))
        os.mkdir(cls.script_path + "/data/temp")

    
    def test_main_return_none(self, mocker):
        mocker.patch("poetic.gui.Tk.mainloop")
        result = main(_test_args="") #pylint: disable=assignment-from-no-return
        assert result is None
        
    
    @pytest.mark.parametrize("arguments,expected",
                             [(["-s", "This is just a test"], "Diagnostics Report"),
                             (["-f", "./tests/data/file_test.txt"], "Diagnostics Report"),
                             (["-f", "./tests/data/file_test.txt", "--GUI"], "Test GUI launch"),
                             (["-s", "This is just a test", "--GUI"], "Test GUI launch"),
                             (["--GUI"], "Test GUI launch"),
                             ("", "Test GUI launch")]
                             )
    def test_main_cli_parameters_sentence_file_gui(self, mocker, arguments, expected):
        screen_stdout = sys.stdout
        string_stdout = StringIO()
        sys.stdout = string_stdout
        
        mocker.patch("poetic.gui.Tk.mainloop")
        main(_test_args=arguments)
            
        output = string_stdout.getvalue()
        sys.stdout = screen_stdout
        
        assert expected in output
        
    
    @pytest.mark.parametrize("arguments",
                            [["-s", "This is just a test", "-o", "./tests/data/temp/test_s.txt"],
                            ["-f", "./tests/data/file_test.txt", "-o", "./tests/data/temp/test_s_f.txt"]]
                            )    
    def test_main_cli_parameters_save_file(self, mocker, arguments):
        mocker.patch("poetic.gui.Tk.mainloop")
        main(_test_args=arguments)
        assert os.path.exists(arguments[3])
        
    
    @classmethod
    def teardown_class(cls):
        info_instance = Info.get_instance()
        info_instance._destructor()
        del info_instance
        
        files = os.listdir(cls.script_path + "/data/temp/")
        for file in files:
            os.remove(cls.script_path + "/data/temp/" + file)
        os.rmdir("./tests/data/temp")