from poetic.util import Info, Initializer
import poetic

import re
import os
import gensim

class TestInfo():
    
    def test_build_type(self):
        status = Info.build_status()
        assert isinstance(status, str)
        
        
    def test_build_status(self):
        status = Info.build_status()
        expected = ["Stable", "Dev", "Beta", "Alpha", "Release Candidate"]
        assert status in expected
        
        
    def test_version_type(self):
        version = Info.version()
        assert isinstance(version, str)
        
        
    def test_version_numbering(self):
        pattern = "^[0-9]*\\.[0-9]*\\.[0-9]*"
        version = Info.version()
        matched = re.match(pattern, version)
        assert matched is not None
        
        
class TestInitializer():
    
    @classmethod
    def setup_class(cls):
        # File paths
        cls.script_path = os.path.dirname(os.path.realpath(__file__))
        
    
    def test_load_dict(self):
        gensim_dict = Initializer.load_dict()
        assert isinstance(gensim_dict, gensim.corpora.dictionary.Dictionary)
    
    
    def test_check_assets_type(self):
        status = Initializer.check_assets()
        assert isinstance(status, dict)
        
        
    def test_check_assets_contents_type(self):
        status = Initializer.check_assets()
        status_all = isinstance(status["all_exist"], bool)  
        status_model = isinstance(status["model"], bool) 
        status_weights = isinstance(status["weights"], bool)
        
        status_bool = status_all and status_model and status_weights
        assert status_bool