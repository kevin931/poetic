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
"""Runs package as a program through main.

The __main__.py is intended for the command line usage
of the package with the command below. Command line arguments
are parsed accordingly with its associated behaviors. For doccumnentation,
please visit: poetic.readthedocs.io or github.com/kevin931/poetic.

Examples:

    Run the GUI:
    
    .. code-block:: bash
    
        python -m poetic
        
    String Input:
    
    .. code-block:: bash
    
        python -m poetic -s "This is poetic."
        
    File Input:
    
    .. code-block:: bash
    
        python -m poetic -f "<PATH>"
        
    Results Output
    
    .. code-block:: bash
    
        python -m poetic -s "This is poetic." -o "<PATH>"
    


"""

from poetic import gui, predictor, util, results
from typing import List, Union, Optional

def main(*, _test: bool=False, _test_args: Optional[Union[List[str], str]]=None) -> None:
    
    args, model, dictionary = util.Initializer.initialize(_test=_test, _test_args=_test_args)
    new_pred = predictor.Predictor(model, dictionary)

   
    if args["Sentence"] is not None or args["File"] is not None:

        if args["Sentence"] is not None:
            score = new_pred.predict(args["Sentence"])

        if args["File"] is not None:
            score = new_pred.predict_file(args["File"])

        score.run_diagnostics()

        if args["Out"] is not None:
            score.to_file(args["Out"])
        else:
            print(score.generate_report())


    launch_GUI = True if args["Sentence"] is None and args["File"] is None else False

    if args["GUI"] or launch_GUI:
        if _test:           
            print("Test GUI launch")
        gui.GUI(new_pred, _test=_test)
                   

if __name__ == "__main__":
    main()