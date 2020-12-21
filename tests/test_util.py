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
from poetic.util import Info, Initializer, _Arguments
import poetic

import re
import os
import pytest
from io import StringIO
import sys
import http

import gensim
from tensorflow import keras

class TestInfo():
    
    @classmethod
    def setup_class(cls):
        Info(_test=True)
        
    
    def test_info_singleton(self):
        try:
            Info(_test=True)
        except Exception as e:
            assert isinstance(e, poetic.exceptions.SingletonError)
        else:
            assert False
            
            
    def test_info_singleton_error_message(self):
        try:
            Info(_test=True)
        except poetic.exceptions.SingletonError as e:
            message = str(e)
        else:
            assert False
            
        expected = "Info is a singleton class. Use Info.get_instance() instead."
        assert message == expected
            
            
    def test_info_test_parameter(self):
        assert Info.get_instance()._test() is True
    
    
    @pytest.mark.parametrize("method, return_type",
                             [("get_instance", Info),
                             ("build_status", str),
                             ("version", str)]
                             )
    def test_method_return_type(self, method, return_type):
        return_object = getattr(Info, method)()
        assert isinstance(return_object, return_type)
        
        
    def test_build_status(self):
        status = Info.build_status()
        expected = ["Stable", "Dev", "Beta", "Alpha", "Release Candidate"]
        assert status in expected
        
        
    def test_version_numbering(self):
        pattern = "^[0-9]*\\.[0-9]*\\.[0-9]*"
        version = Info.version()
        matched = re.match(pattern, version)
        assert matched is not None
        
    
    @classmethod
    def teardown_class(cls):
        info_instance = Info.get_instance()
        info_instance._destructor()
        del info_instance
        
        
class TestInitializer():
    
    @classmethod
    def setup_class(cls):
        Info.get_instance(_test=True)
        # File paths
        cls.script_path = os.path.dirname(os.path.realpath(__file__))
        cls.initialize_return =  Initializer.initialize(_test_args="")
        cls.assets_status = Initializer.check_assets()
        
        
    def test_initialize_return_tuple_type(self):
        assert isinstance(self.initialize_return, tuple)
        
        
    def test_initialize_return_tuple_length(self):
        assert len(self.initialize_return) == 3
        
        
    @pytest.mark.parametrize("index, return_type",
                             [(0, dict),
                             (1, keras.Model),
                             (2, gensim.corpora.dictionary.Dictionary)]
                             )   
    def test_initialize_return_tuple_contents_type(self, index, return_type):    
        assert isinstance(self.initialize_return[index], return_type)
        
    
    @pytest.mark.parametrize("method, return_type",
                             [("load_dict", gensim.corpora.dictionary.Dictionary),
                             ("load_model", keras.Model),
                             ("check_assets", dict)]
                             )    
    def test_dict_model_assets_return_type(self, method, return_type):
        load_return = getattr(Initializer, method)()
        assert isinstance(load_return, return_type)
        
        
    def test_check_assets_contents_type(self):
        status_all = isinstance(self.assets_status["all_exist"], bool)  
        status_model = isinstance(self.assets_status["model"], bool) 
        status_weights = isinstance(self.assets_status["weights"], bool)
        
        status_bool = status_all and status_model and status_weights
        assert status_bool
        
        
    def test_download_assets_all_exist(self):
        self.assets_status["all_exist"] = True
        
        screen_stdout = sys.stdout
        string_stdout = StringIO()
        sys.stdout = string_stdout
        
        Initializer.download_assets(self.assets_status)
            
        output = string_stdout.getvalue()
        sys.stdout = screen_stdout     
        assert output == ""

      
    def test_download_assets_all_exist_return_none(self):
        self.assets_status["all_exist"] = True
        result = Initializer.download_assets(self.assets_status)       
        assert result is None
        
        
    def test_download_assets_check_assets_return_none(self):
        result = Initializer.download_assets()
        assert result is None
        
        
    def test_download_assets_input_n_return_none(self, mocker):
        self.assets_status["all_exist"] = False
        mocker.patch("builtins.input", return_value="n")
        result = Initializer.download_assets(assets_status=self.assets_status)
        assert result is None
        
    
    @pytest.mark.parametrize("input_value, expected, force",
                             [("Y", "Download in progress...", False),
                             ("y", "Download in progress...", False),
                             ("n", "You have declined to download the assets.", False),
                             ("N", "You have declined to download the assets.", False),
                             (None, "Download in progress...", True)]
                             )     
    def test_download_assets_force_and_input_printout(self, mocker, input_value, expected, force):
        self.assets_status["all_exist"] = False
        
        screen_stdout = sys.stdout
        string_stdout = StringIO()
        sys.stdout = string_stdout
        
        mocker.patch("builtins.input", return_value=input_value)
        Initializer.download_assets(assets_status=self.assets_status, force_download=force)
        
        output = string_stdout.getvalue()
        sys.stdout = screen_stdout
        
        assert expected in output
        
        
    def test_download_assets_url_download_extract_mock(self, mocker):
        contents_mock = mocker.MagicMock()
        contents_mock.read.return_value = b"This is a test."
        
        zip_mock = mocker.MagicMock()
        zip_mock.extractall.return_value = None
        
        mocker.patch("poetic.util.urlopen", return_value = contents_mock)
        mocker.patch("poetic.util.ZipFile", return_value = zip_mock)
        mocker.patch("poetic.util.Info._test", return_value = False)
        
        self.assets_status["all_exist"] = False
        
        Initializer.download_assets(assets_status=self.assets_status, force_download=True)
        
        contents_mock.read.assert_called()
        zip_mock.extractall.assert_called()
            
            
    @classmethod
    def teardown_class(cls):
        info_instance = Info.get_instance()
        info_instance._destructor()
        del info_instance
   
        
class Test_Arguments():
    
    @classmethod
    def setup_class(cls):
        cls.parser = _Arguments()
        
    
    def test_version_type(self):
        version = self.parser.version()
        assert isinstance(version, str)
    
    
    def test_version(self):
        pattern = "Poetic [0-9]*\\.[0-9]*\\.[0-9]*"
        version = self.parser.version()
        matched = re.match(pattern, version)
        assert matched is not None
    
    
    def test_parse_type(self):
        test_args = []
        arguments = self.parser.parse(test_args)
        assert isinstance(arguments, dict)
    
    
    def test_parse_flags(self):
        test_args = []
        arguments = self.parser.parse(test_args)
        arguments_keys = list(arguments.keys())
        expected = ["GUI", "Sentence", "File", "Out"]
        assert arguments_keys == expected
        
        
    @pytest.mark.parametrize("input",
                             [["-s", ".", "-f", "."],
                             ["--Sentence", ".", "--File", "."]]
                             )
    def test_unsupported_config_error(self, input):
        try:
            self.parser.parse(input)
        except Exception as e:
            assert isinstance(e, poetic.exceptions.UnsupportedConfigError)
            
            
    @pytest.mark.parametrize("input,key",
                             [(["-s", "."], "Sentence"),
                             (["--Sentence", "."], "Sentence"),
                             (["--GUI"], "GUI"),
                             (["-g"], "GUI"),
                             (["--File", "."], "File"),
                             (["-f", "."], "File"),
                             (["--Out", "."], "Out"),
                             (["-o", "."], "Out")]
                             )        
    def test_config_single_flag(self, input, key):
        arguments = self.parser.parse(input)
        assert arguments[key] is not None
        