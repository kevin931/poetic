from poetic import gui
from _tkinter import TclError

class TestGUI():
    
    def test_gui_constructor(self):
        try:
            gui.GUI(_test=True)
        except TclError:
            assert True
        except:
            assert False
        else:
            assert True
        