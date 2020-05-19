from Lib import poetry_predictor as pp

def main():

    ## Initialize and load model
    new_program = pp.Initialize()
    model = new_program.load_model()
    dict = new_program.load_dict()

    newGUI = pp.GUI(model, dict)


if __name__ == "__main__":
    main()