# Import necessary modules
import numpy as np
import csv

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

    def run_diagnostics(self):
        ## Save diagnostics in a dictionary as instance attribute
        self.diagnostics = {}
        ## Length
        self.diagnostics["Sentence_count"] = len(self.predictions)
        ## Five number summary
        self.diagnostics["Five_num"] = self.five_number(self.predictions)
        ## Append the predictions
        self.diagnostics["Predictions"] = self.predictions

    def to_file(self, path):

        ## Check output file type for csv
        path_len = len(path)
        if (path[(path_len-4):path_len]==".csv"):
            ## Call to_csv method
            self.to_csv(path)
        else:
            ## Generate the general report
            contents = self.generate_report()
            ## Try open or create a new file
            try:
                f = open(path, "w")
                f.write(contents)
                f.close() # Close File

            except:
                print(contents)
                print("Warning: Unable to open file at designated path.\n\n")

    def to_csv(self, path):
        try:
            ## Open the file
            with open(path, "w") as file:
                ## Writer
                writer = csv.writer(file)
                ## Write header
                writer.writerow(["Sentence_num", "Score"])
                ## Loop through each prediction
                for i in range(0, len(self.predictions)):
                    writer.writerow([i+1, self.predictions[i]])
        except:
            print("Warning: Unable to open file at designated path.\n\n")

    ## Generate the contents of the output file
    def generate_report(self):
        ## Program Information
        r = "Poetry Predictor\n"
        r = r + "Version: 0.2.0\n"
        r = r + 'For latest updates: www.github.com/kevin931/PoetryPredictor\n\n'
        ## General Information
        r = "Diagnostics Report\n\n"
        r = r + "Model: Lexical Model\n"
        r = r + f"Number of Sentences: {self.diagnostics['Sentence_count']}\n\n"
        ## Five Number Summary
        r = r + "~~~Five Number Summary~~~\n"
        r = r + f"Minimum: {self.diagnostics['Five_num']['Min']}\n"
        r = r + f"Mean: {self.diagnostics['Five_num']['Mean']}\n"
        r = r + f"Median: {self.diagnostics['Five_num']['Median']}\n"
        r = r + f"Maximum: {self.diagnostics['Five_num']['Max']}\n"
        r = r + f"Standard Deviation: {self.diagnostics['Five_num']['Stdev']}\n\n"

        ## Print out the score of each sentence
        r = r + "~~~All Scores~~~\n"
        for i in range(0, self.diagnostics["Sentence_count"]):
            r = r + f"Sentence #{i+1}: {self.predictions[i]}\n"

        return r