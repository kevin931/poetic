from poetic.util import Info, Initializer
import poetic

import re

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
        
        
        