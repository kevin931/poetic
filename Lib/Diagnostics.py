# Import necessary modules
import numpy as np

class Diagnostics():
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

