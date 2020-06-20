# Import necessary modules
import numpy as np

class Diagnostics():

    ## Constructor
    def __init__(self, predictions, diagnostics=None):
        self.predictions = predictions
        self.diagnostics = diagnostics

    ## String representation
    def __str__(self):
        general_message = "Diagnostics object for the following predictions: "
        predictions = str(self.predictions)
        if len(predictions) > 15:
            predictions = predictions[0:14] + "..."
        return general_message + predictions

    ## String Representation
    def __repr__(self):
        repr = {"Predictions": self.predictions, "Diagnostics": self.diagnostics}
        return str(repr)

    ## len method: return the length of the predictions attribute.
    def __len__(self):
        return len(self.predictions)

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

    def get_diagnostics(self):
        ## Save diagnostics in a dictionary as instance attribute
        self.diagnostics = {}
        ## Length
        self.diagnostics["Sentence_count"] = len(self.predictions)
        ## Five number summary
        self.diagnostics["Five_num"] = cls.five_number(self.predictions)
        ## Append the predictions
        self.diagnostics["Predictions"] = self.predictions

        return self.diagnostics
