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
from poetic import gui, util, exceptions, predictor

from tensorflow import keras

from io import StringIO
import sys
import pytest

class TestGUI():
    
    @classmethod
    def setup_class(cls):
        util.Info(_test=True)
        
        json_file = open("./tests/data/lexical_model_dummy.json", 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        
        model = keras.models.model_from_json(loaded_model_json)
        model.load_weights("./tests/data/lexical_model_dummy.h5")
        
        cls.new_predictor = predictor.Predictor(model=model)

    
    def test_gui_constructor_with_mock(self, mocker):
        mock_main = mocker.MagicMock()
        mocker.patch("poetic.gui.Tk.mainloop", mock_main)
        gui.GUI()
        mock_main.assert_called()
            
            
    def test_sumbit_file(self, mocker):
        mocker.patch("poetic.gui.Tk.mainloop")
        mock_submit = mocker.MagicMock()
        mocker.patch("poetic.gui.futures.ThreadPoolExecutor.submit", mock_submit)
        gui.GUI()._submit_file()
        mock_submit.assert_called()
        
        
    def test_submit_sentence_input_length_error(self, mocker):
        screen_stdout = sys.stdout
        string_stdout = StringIO()
        sys.stdout = string_stdout
        
        mocker.patch("poetic.gui.Tk.mainloop")
        mocker.patch("poetic.gui.Entry.get", return_value="")
        gui.GUI(predictor=self.new_predictor)._submit_sentence()

        expected = "Input length out of bound: must be between 1 and 465"
        
        output = string_stdout.getvalue()
        sys.stdout = screen_stdout
        assert expected in output
        
        
    def test_submit_sentence_raise_general_error(self, mocker):
        mocker.patch("poetic.gui.Tk.mainloop")
        mocker.patch("poetic.gui.Entry.get", return_value={})
        
        try:
            gui.GUI(predictor=self.new_predictor)._submit_sentence()
        except Exception as e:
            assert isinstance(e, TypeError)
    
    
    def test_submit_sentence(self, mocker):
        mocker.patch("poetic.gui.Tk.mainloop")
        mocker.patch("poetic.gui.Entry.get", return_value="This is a test")
        gui.GUI(predictor=self.new_predictor)._submit_sentence()

        
    @pytest.mark.parametrize("mock_object, method",
                            [("poetic.gui.filedialog.askdirectory", "_select_directory"),
                            ("poetic.gui.filedialog.askopenfilename", "_select_file")]
                            )      
    def test_select_directory_and_file(self, mocker, mock_object, method):
        ask_mock = mocker.MagicMock()
        ask_mock.return_value = "./tests/"
        label_mock = mocker.MagicMock()
        mocker.patch("poetic.gui.Tk.mainloop")
        mocker.patch(mock_object, ask_mock)
        mocker.patch("poetic.gui.Label.config", label_mock)
        
        gui_window = gui.GUI()
        getattr(gui_window, method)()
        
        ask_mock.assert_called()
        label_mock.assert_called()

        
    @pytest.mark.parametrize("file_type", [1, 2])    
    def test_run_file(self, mocker, file_type):
        predict_results = self.new_predictor.predict_file("./tests/data/file_test.txt")
        
        to_file_mock = mocker.MagicMock()
        mocker.patch("poetic.gui.Tk.mainloop")
        mocker.patch("poetic.gui.IntVar.get", return_value=file_type)
        mocker.patch("poetic.predictor.Predictor.predict_file", return_value = predict_results)
        mocker.patch("poetic.gui.Tk.after")
        mocker.patch("poetic.results.Diagnostics.to_file", to_file_mock)
        
        new_gui = gui.GUI(predictor=self.new_predictor)
        new_gui.filepath = "./tests/data/file_test.txt"
        new_gui.savedir = "./"
        new_gui._run_file()
        
        to_file_mock.assert_called()
        
        
    @pytest.mark.parametrize("file_type", [1, 2])
    def test_run_file_file_exist(self, mocker, file_type):
        predict_results = self.new_predictor.predict_file("./tests/data/file_test.txt")
        
        to_file_mock = mocker.MagicMock()
        mocker.patch("poetic.gui.Tk.mainloop")
        mocker.patch("poetic.gui.IntVar.get", return_value=file_type)
        mocker.patch("poetic.predictor.Predictor.predict_file", return_value = predict_results)
        mocker.patch("poetic.gui.Tk.after")
        mocker.patch("poetic.results.Diagnostics.to_file", to_file_mock)
        mocker.patch("os.path.exists", return_value=True)
        
        new_gui = gui.GUI(predictor=self.new_predictor)
        new_gui.filepath = "./tests/data/file_test.txt"
        new_gui.savedir = "./"
        new_gui._run_file()
        
        assert not to_file_mock.called
        
        
    def test_update_status(self, mocker):
               
        update_mock = mocker.MagicMock()
        mocker.patch("poetic.gui.Tk.mainloop")
        mocker.patch("poetic.gui.Label.config", update_mock)

        gui.GUI()._update_status("Test")
        update_mock.assert_called()
            
    
    @classmethod
    def teardown_class(cls):
        info_instance = util.Info.get_instance()
        info_instance._destructor()
        del info_instance