from poetic.__main__ import main


class TestMain():
    
    def test_main_return_none(self):
        result = main(_test=True) #pylint: disable=assignment-from-no-return
        assert result is None