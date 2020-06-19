# Import necessary modules
import numpy as np

class Diagnostics():

    ## Constructor
    def __init__(self, predictions):
        self.predictions = predictions

    ## Five number summary
    @classmethod
    def five_number(cls, input):
        # Summary Dictionary
        summary = {}
        # Five number summary
        summary["Min"] = np.min(input)
        summary["Mean"] = np.mean(input)
        summary["Median"] = np.median(input)
        summary["Stdev"] = np.std(input)
        summary["Max"] = np.max(input)

        return(summary)

