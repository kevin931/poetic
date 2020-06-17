# Import necessary module
from Lib import *

def main():

    ## Initialize and load the program
    args, model, dict = Initialize.Initializer.initialize()

    # print(args)

    ## Initialize the predictor
    predictor = Predictor.Predictor(model, dict)

    ## Check for "-s" tag
    if args["Sentence"] is not None:
        ## Prediction
        score = predictor.predict(args["Sentence"])
        ## Diagnostics
        score = Diagnostics.Diagnostics.five_number(score)
        ## Extracting the median
        score = str(round(score["Median"], 2))
        print("\n\nYour score is " + score + "\n\n")

    ## Start the program with the GUI
    if args["GUI"] or args["Sentence"] is None:
        newGUI = GUI.GUI(predictor)

if __name__ == "__main__":
    main()

predictor.predict("I am a good man. Hi there")