# Package: poetic (poetic-py)
# Author: Kevin Wang
#
# The MIT License (MIT)
#
# Copyright 2020 Kevin Wang
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
""" Module for processing prediction results.

The results module processes the outputs of prediction results
from the Predictor of the predictor module. The functionalities
provided include statistical summaries, io, and diagnostic
reports.

Examples:

    The results module's Diagnostics module can be used as part of
    the prediction workflow. To use its methods with the Predictor
    class: 
    
    .. code-block:: python
    
        pred = poetic.Predictor()
        result = pred.predict("This is an example.")
        result.run_diagnostics() # One-stop function
        result.to_file("<PATH>")
        
    To use without the Predictor class:
    
    .. code-block:: python
    
        pred = [0.1, 0.2, 0.3]
        result = Diagnostics(predictions=pred)
        five_number_summary = result.five_number()
        
    All public methods can be used without the run_diagnostics() method, but
    they depend on the diagnostic attribute, which the run_diagnostic()
    method generates. 


"""


import numpy as np
import csv
from poetic.util import Info

from typing import Optional, List, Sequence, Union, Dict
import warnings


class Diagnostics():
    """ Class for storing and processing prediction results.
    
    ``Diagnostics`` is the default base class of ``Predictions``, which is 
    generated by the ``Predictor`` class. It can also be used as a standalone 
    class for processing any numeric results and strings stored in lists.
    
    Args:
        predictions (list): Predictions of poetic scores.
        sentences (list, optional): Sentences associated with the predictions.

    Attributes:
        predictions (list): Predictions of poetic scores.
        sentences (list): Sentences associated with the predictions.
        diagnostics(dict): A dictionary of diagnostics statistics,
            including sentence count, five number summary, and the predictions themselves. 
    """

    def __init__(self, predictions: List[float], sentences: Optional[List[str]]=None) -> None:
        self.predictions = predictions
        self.sentences = sentences
        self.diagnostics = None


    def __str__(self) -> str:
        """ String representation for ``str()``. 
        
        This string representation returns a summary of of the object. It will truncate
        results if there are more than 15 prediction entries. To get a string representation
        of all the results in a dictionary cast into string, use repr() method.
        
        Returns:
            str: String representation of the object.    
        """
        
        general_message = "Diagnostics object for the following predictions: "
        predictions = str(self.predictions)
        if len(predictions) > 15:
            predictions = predictions[0:14] + "..."
        return general_message + predictions


    def __repr__(self) -> str:
        """ String representation for ``repr()``.
        
        This string representation returns a dictionary cast into a string with three
        attributes of this class: predictions, sentences, and diagnostics. 
        
        Returns:
            str: String representation of the object.
        """
        
        repr_string = {"Predictions": self.predictions, 
                       "Sentences": self.sentences,
                       "Diagnostics": self.diagnostics}
        return str(repr_string)


    def __len__(self) -> int:
        """ Method for ``len()``.

        Returns: 
            int: The length of the predictions attribute
        """
        return len(self.predictions)
    
    
    def __lt__(self, rhs: "Diagnostics") -> bool:
        """ Method for ``<`` operator.
        
        The ``<`` operator relies on the mean predictions of each object 
        for comparison, and it is suited for normal or normal-like data.

        Returns: 
            bool: Whether the mean predictions the left-hand-side is smaller.
        """
        
        return np.mean(self.predictions) < np.mean(rhs.predictions)
    
    
    def __gt__(self, rhs: "Diagnostics") -> bool:
        """ Method for ``>`` operator.
        
        The ``>`` operator relies on the mean predictions of each object 
        for comparison, and it is suited for normal or normal-like data.

        Returns: 
            bool: Whether the mean predictions the left-hand-side is greator.
        """
        
        return np.mean(self.predictions) > np.mean(rhs.predictions)
    
    
    def __le__(self, rhs: "Diagnostics") -> bool:
        """ Method for ``>`` operator.
        
        The ``<=`` operator relies on the mean predictions of each object 
        for comparison, and it is suited for normal or normal-like data.

        Returns: 
            bool: Whether the mean predictions the left-hand-side is smaller
                or equal.
        """
        
        return np.mean(self.predictions) <= np.mean(rhs.predictions)
    
    
    def __ge__(self, rhs: "Diagnostics") -> bool:
        """ Method for ``>`` operator.
        
        The ``>=`` operator relies on the mean predictions of each object 
        for comparison, and it is suited for normal or normal-like data.

        Returns: 
            bool: Whether the mean predictions of the left-hand-side is 
                greator or equal.
        """
        
        return np.mean(self.predictions) >= np.mean(rhs.predictions)


    @classmethod
    def five_number(cls, 
                    numeric_input: Union["numpy.ndarray", List[float]]=None, 
                    **kwargs) -> Dict[str, float]:
        """Five number summary.

        This methods generates five number summary of a given input.
        The five number summary includes minimum, mean, median,
        standard deviation, and maximum. This is a class method.

        Parameters:
            numeric_input (numpy.ndarrau, list): An array like object.

        Returns:
            dict(str, float): A dictionary of five number results.
        """
        
        if "input" in kwargs:
            numeric_input = kwargs["input"]
            
            warning_message = ("The 'input' parameter is deprecated and will be removed"
                               "in the next major release. Use the 'numeric_input' parameter "
                               "instead. No positional args impacted.")
            warnings.warn(warning_message, FutureWarning)
            
        elif numeric_input is None:
            message = ("The numeric_input variable is required. The default NoneType maintains"
                       "backwards compatibility and will be removed in the next major release.")
            raise TypeError(message)

        summary = {}
        summary["Min"] = np.min(numeric_input)
        summary["Mean"] = np.mean(numeric_input)
        summary["Median"] = np.median(numeric_input)
        summary["Stdev"] = np.std(numeric_input)
        summary["Max"] = np.max(numeric_input)

        return(summary)


    def run_diagnostics(self) -> None:
        """Run the diagnostics of the predictions.

        This methods generate diagnostics of the predictions,
        which include sentence count, five number summary, and
        the sentences themselves.

        """

        self.diagnostics = {}
        self.diagnostics["Sentence_count"] = len(self.predictions)
        self.diagnostics["Five_num"] = self.five_number(self.predictions)
        self.diagnostics["Predictions"] = self.predictions


    def to_file(self, path: str) -> None:
        """Saves diagnostics and predictions to a file.

        This methods saves the results to a csv or generates a
        diagnostics report along with the predictions. The supplied
        file path's file extension is used to determine which file
        to save. If a csv is explicitly desired, ``to_csv()`` method can
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
            contents = self.generate_report()

            try:
                f = open(path, "w", encoding='utf-8')
                f.write(contents)
                f.close()

            except Exception as e:
                print(contents)
                print("Warning: Unable to open file at designated path.\n\n")
                raise e


    def to_csv(self, path: str) -> None:
        """Saves predictions and sentences to a csv file.

        This methods saves the results to a csv file. For a
        plain text diagnostics, please use the ``to_file()``
        method.

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


    def generate_report(self) -> str:
        """Generates the diagnostics report in string.

        This methods generates a diagnostics report as a string,
        with Poetic package information, five number summary, and
        all sentences and their poetic sores.

        Returns:
            str: A string with diagnostic report.
        """

        version = Info.version()

        # Program Information
        r = "\nPoetic\n"
        r += "Version: {}\n".format(version)
        r += 'For latest updates: www.github.com/kevin931/Poetic\n\n'
        # General Information
        r += "Diagnostics Report\n\n"
        r += "Model: Lexical Model\n"
        r += "Number of Sentences: {}\n\n".format(self.diagnostics['Sentence_count'])
        # Five Number Summary
        r += "~~~Five Number Summary~~~\n"
        r += "Minimum: {}\n".format(self.diagnostics['Five_num']['Min'])
        r += "Mean: {}\n".format(self.diagnostics['Five_num']['Mean'])
        r += "Median: {}\n".format(self.diagnostics['Five_num']['Median'])
        r += "Maximum: {}\n".format(self.diagnostics['Five_num']['Max'])
        r += "Standard Deviation: {}\n\n".format(self.diagnostics['Five_num']['Stdev'])
        # Score of each sentence
        r = r + "~~~All Scores~~~\n"
        for i in range(0, self.diagnostics["Sentence_count"]):
            r = r + "Sentence #{}: {}\n".format(i+1, self.predictions[i])

        return r