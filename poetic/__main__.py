"""Runs package as main.

The __main__.py is intended for the command line usage
of the package with the command below. Command line arguments
are parsed accordingly with its associated behaviors.

    $python -m poetic

"""

from poetic import gui, predictor, util, results

# Initialization and predictor
args, model, dict = util.Initializer.initialize()
new_pred = predictor.Predictor(model, dict)

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
    newGUI = gui.GUI(new_pred)