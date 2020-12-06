from poetic.__main__ import main


class TestMain():
    
    def test_main_return_none(self):
        result = main(_test=True)
        assert result is None