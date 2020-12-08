"""Module for Poetry Predictor GUI.

This module includes the class and methods for poetic's desktop
Tkinter GUI. As an internal interface, this is not intended or
recommended for being used as an import. To run the GUI, execute
on the command line the following command:

.. code-block:: python

    python -m poetic
"""

from tkinter import Tk, Entry, Label, Button, Frame, ttk
from tkinter import filedialog, Radiobutton, IntVar
import re
import os
from concurrent import futures
from poetic.util import Info

# Set up a threadpool
thread_pool = futures.ThreadPoolExecutor(max_workers=1)


class GUI():
    """
    Launches the GUI, which is equivalent to launching
    it through the command line.

    Attributes:
        predictor (Predictor, optional): A Predictor object created
            through the predictor module. If not supplying a Predictor
            object, the GUI will have no predicting functionality.
    """

    def __init__(self, predictor=None, *, _test=False) -> None:
        self.predictor = predictor
        # GUI parameters
        self.root = Tk()
        self.root.title("Poetry Predictor")
        self.root.geometry("610x775")
        self.root.grid_columnconfigure(0, weight=1)

        self.top_frame = Frame(self.root)
        self.top_frame.grid(row=0)

        # Welcome Message
        version = "v."+Info.version()
        self.wcm1 = Label(self.top_frame, text = "Welcome to the Poetry Predictor!", font=("Times", 20))
        self.wcm2 = Label(self.top_frame, text = "Find out how poetic you are!", font=("Times", 15))
        self.wcm3 = Label(self.top_frame, text = version, font=("Times", 15))
        self.wcm1.grid(row=0)
        self.wcm2.grid(row=1)
        self.wcm3.grid(row=2)

        self.divider1 =Label(self.root, text="~~~~~~~~~~~~~~~~~~~~~~~~~~", font=("Times",20))
        self.divider1.grid(row=1,pady=5)

        # Middle Frame, tabs
        self.tabControl = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Interactive Mode')
        self.tabControl.add(self.tab2, text='File Mode')
        self.tabControl.grid(row=2)

        #### Tab 1
        # Message
        self.sentence_msg = Label(self.tab1, text="Please enter your poetic line.",font=("Times", 15))
        self.sentence_msg.grid(row=0, pady=20)
        # Text
        self.sentence_input = Entry(self.tab1, width=40,font=("Times",13))
        self.sentence_input.grid(row=1,pady=20)
        # Button
        self.predict_button = Button(self.tab1, text="Submit",font=("Times",20), command=self._submit_sentence)
        self.predict_button.grid(row=2)
        # Results
        self.divider2 = Label(self.tab1, text="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", font=("Times",17))
        self.result1 = Label(self.tab1, text="Your Result", font=("Times",17))
        self.result2 = Label(self.tab1, text="No result yet!", font=("Times",15))
        self.result3 = Label(self.tab1, text="Please type in your sentence and submit!", font=("Times",15))
        self.divider2.grid(row=3,pady=10)
        self.result1.grid(row=4,pady=5)
        self.result2.grid(row=5)
        self.result3.grid(row=6)

        #### Tab 2 ######
        # Ask for file path
        self.file_input_msg = Label(self.tab2, text="Please select your file.",font=("Times", 15))
        self.file_input_msg.grid(row=0,column=0, pady=5)
        # Display selected file
        self.file_input_path = Label(self.tab2, text="File selected: None", font =("Times", 15))
        self.file_input_path.grid(row=2, pady=5)
        # Select button
        self.file_input_button = Button(self.tab2, text="Select File", font=("Times",15), command=self._select_file)
        self.file_input_button.grid(row=1, pady =5)

        self.divider3 =Label(self.tab2, text="~~~~~~~~~~~~~~~~~~~~~~~~~~", font=("Times",20))
        self.divider3.grid(row=3, pady=3)

        ## Ask for save directory
        self.file_output_msg = Label(self.tab2, text="Please select location to save results." ,font=("Times", 15))
        self.file_output_msg.grid(row=4, pady=5)
        # Echo save directory
        self.file_output_dir = Label(self.tab2, text="Directory Chosen: None" ,font=("Times", 15))
        self.file_output_dir.grid(row=6,pady=1)
        # Select button
        self.directory_input_button = Button(self.tab2, text="Select", font=("Times",15), command=self._select_directory)
        self.directory_input_button.grid(row=5, pady =5)

        self.divider4 =Label(self.tab2, text="~~~~~~~~~~~~~~~~~~~~~~~~~~", font=("Times",20))
        self.divider4.grid(row=7, pady=3)

        # Output mode
        self.radiolabel = Label(self.tab2, text="Select Output File Type", font=("Times",15))
        self.radiolabel.grid(row=8, pady=5)
        # Radio Buttons: Output select
        self.output_variable = IntVar()
        self.radio1 = Radiobutton(self.tab2,
            text="Summary Text File",
            variable=self.output_variable,
            value=1)
        self.radio2 = Radiobutton(self.tab2,
            text = "CSV File",
            variable=self.output_variable,
            value=2)

        self.radio1.grid(row=9)
        self.radio2.grid(row=10)

        self.divider5 =Label(self.tab2, text="~~~~~~~~~~~~~~~~~~~~~~~~~~", font=("Times",20))
        self.divider5.grid(row=11, pady=3)

        # Run and Status
        self.run_button = Button(self.tab2, text="Run!", font=("Times",15), command=self._submit_file)
        self.run_button.grid(row=12)
        self.status_message = Label(self.tab2, text = "Status: Not yet run.", font=("Times",15))
        self.status_message.grid(row=13, pady=3)

        if not _test:
            self.root.mainloop() # End


    def _submit_sentence(self) -> None:
        # Predict with sentence in interactive mode

        input = self.sentence_input.get()
        try:
            score =self.predictor.predict(input)
        # Input Length Error
        except self.predictor._InputLengthError as e:
            print(e)
            self.result2.config(text = "Nothing entered. Please try again.")
            self.result3.config(text="Please type in your sentence and submit!")

        # All other exceptions
        except Exception as e:
            self.result2.config(text = "An error has occurred. Please try again.")
            self.result3.config(text="Please type in your sentence and submit!")
            raise e

        else:
            # Process outputs
            score.run_diagnostics()
            score = score.diagnostics["Five_num"]["Median"]
            score = round(score, 2)
            # Display results
            self.result2.config(text="Your score is "+str(score))
            message = "This is poetic!" if score >=0.5 else "This is not so poetic!"
            self.result3.config(text=message)


    def _select_file(self) -> None:
        # Method that selects file.

        self.filepath = filedialog.askopenfilename(initialdir=".", title="Select your file.")
        file_name = re.split("/", self.filepath)[-1] # Get file name
        self.file_input_path.config(text=file_name,
                                    font =("Times", 15))


    def _select_directory(self) -> None:
        # Ask for save directory
        self.savedir = filedialog.askdirectory(initialdir=".", title="Select your save directory.")
        dir_name = re.split("/", self.savedir)[-1]
        self.file_output_dir.config(text=dir_name, font =("Times", 15))


    def _submit_file(self) -> None:
        thread_pool.submit(self._run_file)


    def _run_file(self) -> None:
        # Method for submitting the file to run.

        # Update status
        self.root.after(0, self._update_status, "Running")
        # Run the results
        results = self.predictor.predict_file(self.filepath)
        results.run_diagnostics()
        # Save filepath
        file_name = re.split("/",self.filepath)[-1]
        file_name = file_name.split(".")[0]
        file_path = self.savedir+"/"+file_name+"_results"
        # Check file type
        file_type = self.output_variable.get()
        if file_type == 1:
            file_path += ".txt"
        elif file_type ==2:
            file_path += ".csv"

        # Check if the file already exists to prevent overwriting
        if os.path.exists(file_path):
            error_msg = "Error: "+file_name+" already exists."
            self.root.after(0, self._update_status, error_msg)
        else:
            # Save results and update status
            results.to_file(file_path)
            self.root.after(0, self._update_status, "Done!")


    def _update_status(self, status) -> None:
        # Method for updating the status
        self.status_message.config(text="Status: "+status, font=("Times",15))


# For UI developing purposes only
if __name__ == "__main__":
    GUI()