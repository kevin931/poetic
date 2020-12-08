"""Runs package as a program through main.

The __main__.py is intended for the command line usage
of the package with the command below. Command line arguments
are parsed accordingly with its associated behaviors. For doccumnentation,
please visit: poetic.readthedocs.io or github.com/kevin931/poetic

    $python -m poetic

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
        gui.GUI(new_pred, _test=_test)
        
        if _test:           
            print("Test GUI launch")
                   

if __name__ == "__main__":
    main()