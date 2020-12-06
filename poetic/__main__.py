"""Runs package as a program through main.

The __main__.py is intended for the command line usage
of the package with the command below. Command line arguments
are parsed accordingly with its associated behaviors. For doccumnentation,
please visit: poetic.readthedocs.io or github.com/kevin931/poetic

    $python -m poetic

"""

from poetic import gui, predictor, util, results

def main(*, _test=False, _test_args=None):
    # Initialization and predictor
    args, model, dictionary = util.Initializer.initialize(_test=_test, _test_args=_test_args)
    new_pred = predictor.Predictor(model, dictionary)

    # Check for command-line mode
    if args["Sentence"] is not None or args["File"] is not None:
        # "-s" flag
        if args["Sentence"] is not None:
            score = new_pred.predict(args["Sentence"])
        # "-f" flag
        if args["File"] is not None:
            score = new_pred.predict_file(args["File"])

        score.run_diagnostics()
        # Check for "-o" tag
        if args["Out"] is not None:
            score.to_file(args["Out"])
        else:
            print(score.generate_report())

    # Check for default GUI mode without "-f" and "-s" tag
    launch_GUI = True if args["Sentence"] is None and args["File"] is None else False
    # Start the program with the GUI
    if args["GUI"] or launch_GUI:
        if _test:           
            print("Test GUI launch")
        else:
            gui.GUI(new_pred)
                   


if __name__ == "__main__":
    main()