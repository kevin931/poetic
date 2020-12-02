""" Module for processing prediction results.

This module processes the outputs of prediction results
from the Predictor of the predictor module. The functionalities
provided include statistical summaries, io, and diagnostic
reports.

Classes:
    Disgnostics (predictions, sentences, diagnostics):
        Class for storing and handling prediction results.

"""


import numpy as np
import csv
from poetic.util import Info

class Diagnostics():
    """ Class for storing and processing prediction results.

    Attributes:
        predictions (list):
            Predictions of poetic scores.
        sentences (list, optional):
            Sentences associated with the predictions.

    Methods:
        five_number(input):
            Generate the five-number summary of the given input.
        run_diagnostics()
            Run the diagnostics of the predictions.
        to_file(path)
            Genererate and save a summary text file for predictions.
        to_csv(path)
            Save predictions and sentences to a csv file.
        generate_report()
            Generate diagnostics report for predictions as a string.
    """

    def __init__(self, predictions, sentences=None):
        """
        Parameters:
            predictions (list):
                Predictions of poetic scores.
            sentences (list, optional):
                Sentences associated with the predictions.
        """

        self.predictions = predictions
        self.sentences = sentences
        self.diagnostics = None

    # String representation
    def __str__(self):
        general_message = "Diagnostics object for the following predictions: "
        predictions = str(self.predictions)
        if len(predictions) > 15:
            predictions = predictions[0:14] + "..."
        return general_message + predictions

    # String Representation
    def __repr__(self):
        repr = {"Predictions": self.predictions, 
                "Sentences": self.sentences,
                "Diagnostics": self.diagnostics}
        return str(repr)

    def __len__(self):
        """ Method for len().

        Returns: The length of the predictions attribute
        """
        return len(self.predictions)


    @classmethod
    def five_number(cls, input):
        """Five number summary.

        This methods generates five number summary of a given input.
        The five number summary includes minimum, mean, median,
        standard deviation, and maximum. This is a class method.

        Parameters:
            input (array_like): An array like object.

        Returns:
            summary (dict): A dictionary of five number results.
        """

        summary = {}
        summary["Min"] = np.min(input)
        summary["Mean"] = np.mean(input)
        summary["Median"] = np.median(input)
        summary["Stdev"] = np.std(input)
        summary["Max"] = np.max(input)

        return(summary)

    def run_diagnostics(self):
        """Run the diagnostics of the predictions.

        This methods generate diagnostics of the predictions,
        which include sentence count, five number summary, and
        the sentences themselves.

        """

        self.diagnostics = {}
        self.diagnostics["Sentence_count"] = len(self.predictions)
        self.diagnostics["Five_num"] = self.five_number(self.predictions)
        self.diagnostics["Predictions"] = self.predictions

    def to_file(self, path):
        """Saves diagnostics and predictions to a file.

        This methods saves the results to a csv or generates a
        diagnostics report along with the predictions. The supplied
        file path's file extension is used to determine which file
        to save. If a csv is explicitly desired, to_csv() method can
        be used. For all file extensions other than csv, a plain text
        report will be generated.

        Parameters:
            path (str): An string representing the file path.

        """

        # Check for csv
        path_len = len(path)
        if (path[(path_len-4):path_len]==".csv"):
            self.to_csv(path)
        else:
            # Plain Text report
            contents = self.generate_report()

            try:
                f = open(path, "w", encoding='utf-8')
                f.write(contents)
                f.close() # Close File

            except:
                print(contents)
                print("Warning: Unable to open file at designated path.\n\n")


    def to_csv(self, path):
        """Saves predictions and sentences to a csv file.

        This methods saves the results to a csv file. For a
        plain text diagnostics, please use the to_file() method.

        Parameters:
            path (str): An string representing the file path.

        """
        try:
            with open(path, "w", encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Sentence_num","Sentence", "Score"])
                # Loop through each prediction
                for i in range(0, len(self.predictions)):
                    if self.sentences is not None:
                        row = [i+1, self.sentences[i], self.predictions[i]]
                    else:
                        row = [i+1, "NA", self.predictions[i]]
                    # Write results
                    writer.writerow(row)

        except Exception as e:
            print("Warning: Unable to open file at designated path.\n\n")
            raise e



    def generate_report(self):
        """Generates the diagnostics report in string.

        This methods generates a diagnostics report as a string,
        with Poetic package information, five number summary, and
        all sentences and their poetic sores.

        Returns:
            r (str): A string with diagnostic report.
        """

        version = Info.version()

        # Program Information
        r = "\nPoetic\n"
        r += f"Version: {version}\n"
        r += 'For latest updates: www.github.com/kevin931/Poetic\n\n'
        # General Information
        r += "Diagnostics Report\n\n"
        r += "Model: Lexical Model\n"
        r += f"Number of Sentences: {self.diagnostics['Sentence_count']}\n\n"
        # Five Number Summary
        r += "~~~Five Number Summary~~~\n"
        r += f"Minimum: {self.diagnostics['Five_num']['Min']}\n"
        r += f"Mean: {self.diagnostics['Five_num']['Mean']}\n"
        r += f"Median: {self.diagnostics['Five_num']['Median']}\n"
        r += f"Maximum: {self.diagnostics['Five_num']['Max']}\n"
        r += f"Standard Deviation: {self.diagnostics['Five_num']['Stdev']}\n\n"
        # Score of each sentence
        r = r + "~~~All Scores~~~\n"
        for i in range(0, self.diagnostics["Sentence_count"]):
            r = r + f"Sentence #{i+1}: {self.predictions[i]}\n"

        return r