## Import necessary module
from Lib import *

def main():

    ## Initialize and load model
    new_program = Initialize.Initialize()
    model = new_program.load_model()
    dict = new_program.load_dict()
    ## Initialize the predictor
    predictor = Predictor.Predictor(model, dict)
    ## Start the program with the GUI
    newGUI = GUI.GUI(predictor)


if __name__ == "__main__":
    main()