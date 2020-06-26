# Import necessary module
from poetry_predictor import gui, predictor, preprocess, results

def main():

    ## Initialize and load the program
    args, model, dict = preprocess.Initializer.initialize()


    ## Initialize the predictor
    new_pred = predictor.Predictor(model, dict)

    ## Check for command-line mode
    if args["Sentence"] is not None or args["File"] is not None:

        ## Check for "-s" tag
        if args["Sentence"] is not None:
            ## Prediction
            score = new_pred.predict(args["Sentence"], type="Content")

        ## Check for "-f" tag
        if args["File"] is not None:
            ## Prediction
            score = new_pred.predict(args["File"], type="Path")

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

if __name__ == "__main__":
    main()