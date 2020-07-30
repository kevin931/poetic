# Import necessary module
from poetic import gui, predictor, util, results

## Initialize and load the program
args, model, dict = util.Initializer.initialize()

## Initialize the predictor
new_pred = predictor.Predictor(model, dict)

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
    newGUI = gui.GUI(new_pred)