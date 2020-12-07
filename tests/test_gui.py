from poetic import gui

class TestGUI():
    
    def test_gui_constructor(self):
        try:
            gui.GUI(_test=True)
        except:
            assert False
        else:
            assert True
        