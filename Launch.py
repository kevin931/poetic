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
import warnings

## Warning message for deprecation
warning_message = "Launching method deprecated.\n"
warning_message += "Use 'python -m poetry_predictor' instead.\n"
warning_message += "Launcher is no longer updated after v.0.2.0 "
warning_message += "and will be removed at in the future."

warnings.warn(warning_message, FutureWarning)

# Import necessary module
from poetic import gui, predictor, util, results

def main():

    ## Initialize and load the program
    args, model, dictionary = util.Initializer.initialize()


    ## Initialize the predictor
    new_pred = predictor.Predictor(model, dictionary)

    ## Check for command-line mode
    if args["Sentence"] is not None or args["File"] is not None:

        ## Check for "-s" tag
        if args["Sentence"] is not None:
            ## Prediction
            score = new_pred.predict(args["Sentence"])

        ## Check for "-f" tag
        if args["File"] is not None:
            ## Prediction
            score = new_pred.predict_file(args["File"])

        ## Run diagnostics
        score.run_diagnostics()

        ## Check for "-o" tag
        if args["Out"] is not None:
            score.to_file(args["Out"])
        else:
            print(score.generate_report())

    ## Check whether for default GUI mode without "-f" and "-s" tag
    launch_GUI = True if args["Sentence"] is None and args["File"] is None else False

    ## Start the program with the GUI
    if args["GUI"] or launch_GUI:
        gui.GUI(new_pred)

if __name__ == "__main__":
    main()