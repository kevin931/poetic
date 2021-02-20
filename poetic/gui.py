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
"""Module for Poetry Predictor GUI.

This module includes all class and methods for poetic's desktop
GUI revemped with guietta and QT. As an internal interface, this is 
not intended or recommended for importing. To run the GUI, follow
the given examples or refer to the documentation.

Examples:

    Simply run the GUI: 
    
    .. code-block:: shell

        python -m poetic
        
    Make prediction and launch GUI by adding the ``-g`` or ``--GUI`` flag:
    
    .. code-block:: shell

        python -m poetic -s "This is poetic." -o "<PATH>" -g
        
"""

from guietta import Gui, _, ___, III, splash, HSeparator
from guietta import QMessageBox, QFileDialog, QPlainTextEdit
from PySide2 import QtGui
from PySide2 import QtCore

import poetic

import os
from typing import Union
import warnings


class _MainWindow():
    
    def __init__(self):
        self.toolbar = Gui([["Settings"], ["Info"], ["Help"]])
        self.toolbar.Settings = self._run_settings_gui
        self.toolbar.Info = self._run_info_gui
        self.toolbar.Help = self._run_help_gui
        
                
    def _run_info_gui(self, gui:"guietta.Gui", *args) -> None:
        _InfoGUI()
        
        
    def _run_settings_gui(self, gui: "guietta.Gui", *args) -> None:
        _SettingsGUI()
        
        
    def _run_help_gui(self, gui: "guietta.Gui", *args) -> None:
        _HelpGUI()      


class GUI(_MainWindow):
    """
    Launches the main GUI, which is equivalent to launching
    it through the command line.

    Args:
        predictor (poetic.Predictor, optional): A ``poetic.Predictor`` object 
            created through the predictor module. It is automatically initialized
            with the default model if not supplied.
            
    Attributes:
        gui (guietta.Gui): The GUI instance.
        predictor (poetic.Predictor): A ``poetic.Predictor`` object. 
        splash (guietta.spash): A splash sreen for initialization. 
    """
    
    def __init__(self, predictor: "poetic.predictor"=None) -> None:
        
        super().__init__()
        self.predictor = predictor
        self._initialize()
    
        self.gui = Gui(["toolbar", ___],
                       [HSeparator()],
                       [GUIUtil.center("Poetic"), ___],
                       ["Select Mode:", ["Interactive"]],
                       [III, ["File"]])
        
        self.gui.toolbar = self.toolbar
        self.gui.Interactive = self._run_interactive_gui
        self.gui.File = self._run_file_gui
        
        self.gui.fonts([_, _],
                       [_, _],
                       [("Halvetica", 15), _],
                       [("Halvetica", 13), ("Halvetica", 13)],
                       [_, ("Halvetica", 13)])
        
        self.gui.run()
        
        
    def _initialize(self):
        
        splash_text = ("Welcome to Poetic!\n"
                       "v.{}\n\n"
                       " Program loading...\n\n"
                       "MIT License\n"
                       "GitHub: kevin931/poetic").format(poetic.util.Info.version())
        self.splash = splash(splash_text)
        self.predictor = poetic.Predictor() if self.predictor is None else None
        self.splash.close()
        
        
    def _run_interactive_gui(self, gui: "guietta.Gui", *args) -> None:
        _InteractiveGUI(self.predictor)
        
    
    def _run_file_gui(self, gui: "guietta.Gui", *args) -> None:
        _FileGUI(self.predictor)
            

class _InteractiveGUI(_MainWindow):
    """
    This is the GUI window for making prediction interactively. This is automatically
    called by the GUI class when the interactive mode is selected and not intended for
    stand-alone usage.

    Args:
        predictor (poetic.Predictor): A ``Predictor`` object initialized in the GUI class.
        
    Attributes:
        gui (guietta.Gui): The GUI instance.
        predictor (poetic.Predictor): A ``Predictor`` object initialized in the GUI class.
    """
    
    def __init__(self, predictor: "poetic.Predictor"):
        
        super().__init__()
        self.predictor = predictor
        
        self.gui= Gui(["toolbar", ___],
                      [HSeparator()],
                      [(GUIUtil.center("Make a Prediction"), "status"), ___],
                      [(QPlainTextEdit, "lexical"), ["Submit"]])
        
        self.gui.events([_, _],
                        [_, _],
                        [_, _],
                        [_, self._submit_lexical_input])
        
        self.gui.toolbar = self.toolbar
        self.gui.fonts([_, _],
                       [_, _],
                       [("Halvetica", 15), _],
                       [("Halvetica", 13), _])
        self.gui.run()
    
        
    def _submit_lexical_input(self, gui: "guietta.Gui", *args) -> None:
        
        self.gui.execute_in_background(func=self._predict, 
                                       args=self.gui.lexical.toPlainText(),
                                       callback=self._update_results)
        
        self.gui.status = GUIUtil.center("Working on results...")
        self.gui.lexical.setPlainText("")
        
        
    def _predict(self, *args):
        
        lexical_input = ""
        for char in args:
            lexical_input += char
    
        try:
            score =self.predictor.predict(lexical_input)

        except Exception as e:
            return (e)

        else:
            score.run_diagnostics()
            return (score)
        
        
    def _update_results(self, *args):
        GUIUtil.process_prediction_results(args[1])  
        self.gui.status = "Make a Prediction"


class _FileGUI(_MainWindow):
    """
    This is the GUI window for making prediction with plain text files. This is automatically
    called by the GUI class when the file mode is selected and not intended for stand-alone 
    usage.

    Args:
        predictor (poetic.Predictor): A ``Predictor`` object initialized in the GUI class.
        
    Attributes:
        gui (guietta.Gui): The GUI instance.
        predictor (poetic.Predictor): A ``Predictor`` object initialized in the GUI class.
    """
    
    def __init__(self, predictor: "poetic.Predictor") -> None:
        
        super().__init__()
        self.predictor = predictor
        
        self.gui = Gui(["toolbar"],
                       [HSeparator()],
                       [(GUIUtil.center("File Prediction"), "status")],
                       [["Select File"]])
        
        self.gui.toolbar = self.toolbar
        self.gui.SelectFile = self._submit_file_input
        self.gui.fonts([_],
                       [_],
                       [("helvetica", 15)],
                       [("helvetica", 13)])
        
        self.gui.run()
        
        
    def _submit_file_input(self, gui: "guietta.Gui", *args) -> None:
        
        file_path = QFileDialog.getOpenFileName(None, "Select file")
        self.gui.execute_in_background(func=self._predict, 
                                       args=file_path,
                                       callback=self._update_results)
        self.gui.status = GUIUtil.center("Working on results...")
        
        
    def _predict(self, *args):
        
        file_path = args[0]
    
        try:
            score =self.predictor.predict_file(path=file_path)

        except Exception as e:
            return (e)

        else:
            score.run_diagnostics()
            return (score)
        
        
    def _update_results(self, *args):
        GUIUtil.process_prediction_results(args[1])
        self.gui.status = GUIUtil.center("Status: No results yet!")


class _InfoGUI():
    
    def __init__(self):
        self.gui = Gui([GUIUtil.center("Package Information"), ___, ___, ___],
                       [(QPlainTextEdit, "info"), ___, ___, ___],
                       [["GitHub"], ["PyPI"], ["conda"], ["Documentation"]])
        
        self.gui.info.setReadOnly(True)
        self.gui.info.setPlainText(self._package_info())
        
        self.gui.GitHub = self._open_github
        self.gui.PyPI = self._open_pypi
        self.gui.conda = self._open_conda
        self.gui.Documentation = self._open_documentation
        
        self.gui.fonts([("Halvetica", 15), _, _, _])
        self.gui.run()
        
        
    def _package_info(self)->str:

        info = ("Package Name: poetic\n"
                "Version: {}\n"
                "Build: {}\n\n"
                "GitHub: kevin931/poetic\n"
                "PyPI: poetic-py\n"
                "conda: kevin931/poetic-py\n\n"
                "Documentation: www.poetic.readthedocs.io\n\n"
                "The MIT License (MIT)\n"
                "Copyright 2020 Kevin Wang\n\n"
                "Permission is hereby granted, free of charge, to any person obtaining a\n"
                'copy of this software and associated documentation files (the "Software"),\n'
                "to deal in the Software without restriction, including without limitation\n"
                "the rights to use, copy, modify, merge, publish, distribute, sublicense,\n"
                "and/or sell copies of the Software, and to permit persons to whom the\n"
                "Software is furnished to do so, subject to the following conditions:\n\n"

                "The above copyright notice and this permission notice shall be included\n"
                "in all copies or substantial portions of the Software.\n\n"

                'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS\n'
                "OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
                "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
                "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
                "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING\n"
                "FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER\n"
                "DEALINGS IN THE SOFTWARE.\n"
                ).format(poetic.util.Info.version(),
                         poetic.util.Info.build_status())
        return info
    
    def _open_link(self, link:str) -> None:
        self.gui.execute_in_main_thread(QtGui.QDesktopServices.openUrl, 
                                        QtCore.QUrl(link))
        
        
    def _open_github(self, gui: "guietta.Gui", *args) -> None: 
        self._open_link("https://github.com/kevin931/poetic")
        
        
    def _open_pypi(self, gui: "guietta.Gui", *args) -> None: 
        self._open_link("https://pypi.org/project/poetic-py/")
        
        
    def _open_conda(self, gui: "guietta.Gui", *args) -> None: 
        self._open_link("https://anaconda.org/kevin931/poetic-py")
        
    def _open_documentation(self, gui: "guietta.Gui", *args) -> None: 
        self._open_link("https://poetic.readthedocs.io/")


class _SettingsGUI():
    
    def __init__(self):
        pass
    

class _HelpGUI():
    
    def __init__(self):
        pass

            
class _ResultsGUI():
    """
    This is the GUI window for showing and saving prediction results. This is automatically
    called by when users successfully make a prediction using either the interactive or file
    mode. This class is not intended as a stand-alone interface.

    Args:
        results (poetic.Diagnostics): A ``poetic.Diagnostics`` object with prediction results.
        
    Attributes:
        gui (guietta.Gui): The GUI instance.
        results (poetic.Diagnostics): A ``poetic.Diagnostics`` object with prediction results.
    """
    
    def __init__(self, results: "poetic.results.Diagnostics") -> None:
        
        self.results = results
        five_number = [str(round(value, 2)) for value in results.diagnostics["Five_num"].values()]
        
        self.gui = Gui([GUIUtil.center("Prediction Results Summary")],
                       [HSeparator()],
                       ["Number of Sentences: " + str(len(results))],
                       ["Min. Score: " + five_number[0]],
                       ["Mean Score: " + five_number[1]],
                       ["Median Score: " + five_number[2]],
                       ["Stdev. Score: " + five_number[3]],
                       ["Max. Score: " + five_number[4]],
                       [HSeparator()],
                       [["Save csv"]],
                       [["Save txt"]])
        self.gui.Savecsv = self._save_csv
        self.gui.Savetxt = self._save_txt
        self.gui.fonts([("Halvetica", 15)])
        self.gui.run()
        
        
    def _save_csv(self, gui: "guietta.Gui", *args) -> None: 
        save_path = GUIUtil.get_save_path(file_type=".csv")
        self.results.to_file(path=save_path)
    
    
    def _save_txt(self, gui: "guietta.Gui", *args) -> None:
        save_path = GUIUtil.get_save_path(file_type=".txt")
        self.results.to_file(path=save_path)
        
   
class GUIUtil():
    """
    The ``util`` class provides utility functions for all GUI classes in the ``gui`` modules. 
    All methods are and will will be static methods. Although this class and its methods are not
    protected by underscores, they are not intended for stand-alone usage.
    
    """
    
    @staticmethod
    def center(text: str) -> str:
        return "<center>" + text + "</center"
    
    @staticmethod
    def process_prediction_results(predictor_return: Union["poetic.Diagnostics", "Exception", "poetic.exceptions.InputLengthError"]) -> None:
        """Process prediction results and errors.
        
        This method processes prediction results from either ``_FileGUI`` or 
        ``_InteractiveGUI`` class's prediction methods. When errors are passed in, 
        a warning message box is invoked. Otherwise, a GUI is called with ``_ResultsGUI``
        to display the results.

        Parameters:
            predictor_return (Union["poetic.Diagnostics", "Exception"): Object returned by prediction methods in the GUIs.
        
        """
            
        if isinstance(predictor_return, Exception):
            QMessageBox.warning(None,
                                "An error has occurred",
                                str(predictor_return))
            
        else:
            _ResultsGUI(results=predictor_return)
            
            
    @staticmethod   
    def get_save_path(file_type: str) -> str:
        """Find a path to save prediction results.
        
        This method returns a unique, new file path that can be used to write a new file with
        the given file extension. All paths will have the format of "results.*"; in the case of
        the file already existing, it will try and add increasing numbers to the file name with
        the format of "results(*).*". It will not provide a path with existing files to prevent
        accidental overwriting.

        Parameters:
            file_type (str): A file extension.

        Returns:
            str: A file path in the selected directory for results.
        """
        
        save_dir = QFileDialog.getExistingDirectory(None, "Select save directory")
        save_path = save_dir + "/results" + file_type
        
        duplicate_index = 2
        while True:
            if os.path.exists(save_path):
                save_path = save_dir + "/results({})".format(duplicate_index) + file_type
                continue  
            else:
                break
            
        return save_path
        
        
if __name__ == "__main__":
    GUI()