#####################
### GUI Associated classes and functions
#####################

## Importing necessary modules
from tkinter import Tk, Entry, Label, Button, Frame, ttk, filedialog

class GUI():

    ## Constructor
    def __init__(self, predictor=None):
        ## Model to use
        self.predictor = predictor

        ## Open the GUI
        self.root = Tk()
        self.root.title("Poetry Predictor")
        self.root.geometry("410x575")

        self.top_frame = Frame(self.root, height = 100)
        self.top_frame.grid(row=0, sticky = "ew")

        ## Welcome Message
        self.wcm1 = Label(self.top_frame, text = "Welcome to the Poetry Predictor!", font=("Times", 20))
        self.wcm2 = Label(self.top_frame, text = "Find out how poetic you are!", font=("Times", 15))
        self.wcm3 = Label(self.top_frame, text = "v.0.1.2", font=("Times", 15))
        self.wcm1.grid(row=0)
        self.wcm2.grid(row=1)
        self.wcm3.grid(row=2)

        self.divider1 =Label(self.root, text="~~~~~~~~~~~~~~~~~~~~~~~~~~", font=("Times",20))
        self.divider1.grid(row=1,pady=5)

        ## Middle Frame, tabs
        self.tabControl = ttk.Notebook(self.root)

        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text='Interactive Mode')
        self.tabControl.add(self.tab2, text='File Mode')

        self.tabControl.grid(row=2)

        #### Tab 1

        ## Message
        self.sentence_msg = Label(self.tab1, text="Please enter your poetic line.",font=("Times", 15))
        self.sentence_msg.grid(row=0, pady=20)
        ## Text
        self.sentence_input = Entry(self.tab1, width=40,font=("Times",13))
        self.sentence_input.grid(row=1,pady=20)

        ## Button
        self.predict_button = Button(self.tab1, text="Submit",font=("Times",20), command=self.submit_sentence)
        self.predict_button.grid(row=2)

        ## Results
        self.divider2 = Label(self.tab1, text="~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~", font=("Times",17))
        self.result1 = Label(self.tab1, text="Your Result", font=("Times",17))
        self.result2 = Label(self.tab1, text="No result yet!", font=("Times",15))
        self.result3 = Label(self.tab1, text="Please type in your sentence and submit!", font=("Times",15))
        self.divider2.grid(row=3,pady=10)
        self.result1.grid(row=4,pady=5)
        self.result2.grid(row=5)
        self.result3.grid(row=6)

        #### Tab 2

        ## Ask for file path
        self.file_input_msg = Label(self.tab2, text="Please select your file.",font=("Times", 15))
        self.file_input_msg.grid(row=0,column=0, pady=5)
        ## Display selected file
        self.file_input_path = Label(self.tab2, text="File selected: None", font =("Times", 15))
        self.file_input_path.grid(row=2, pady=5)
        ## Select button
        self.file_input_button = Button(self.tab2, text="Select File", font=("Times",15), command=self.submit)
        self.file_input_button.grid(row=1, pady =5)

        self.divider3 =Label(self.tab2, text="~~~~~~~~~~~~~~~~~~~~~~~~~~", font=("Times",20))
        self.divider3.grid(row=3, pady=3)

        ## Ask for save directory
        self.file_output_msg = Label(self.tab2, text="Please select location to save results." ,font=("Times", 15))
        self.file_output_msg.grid(row=4, pady=5)
        ## Echo save directory
        self.file_output_dir = Label(self.tab2, text="Directory Chosen: None" ,font=("Times", 15))
        self.file_output_dir.grid(row=6,pady=1)
        ## Select button
        self.file_input_button2 = Button(self.tab2, text="Select", font=("Times",15), command=self.submit)
        self.file_input_button2.grid(row=5, pady =5)

        self.divider4 =Label(self.tab2, text="~~~~~~~~~~~~~~~~~~~~~~~~~~", font=("Times",20))
        self.divider4.grid(row=7, pady=3)

        ## Run and Status
        self.run_button = Button(self.tab2, text="Run!", font=("Times",15), command=self.submit)
        self.run_button.grid(row=8)

        self.status_message = Label(self.tab2, text = "Status: Not yet run.", font=("Times",15))
        self.status_message.grid(row=9, pady=3)

        # self.root.filename = filedialog.askopenfilename(initialdir=".", title="Select your file.", filetypes=("txt"))

        self.root.mainloop()

    ## Predict with sentence in interactive mode
    def submit_sentence(self):
        ## Get the user input
        input = self.sentence_input.get()

        ## Predict
        try:
            score =self.predictor.predict(input, type="Content")

        except:
            self.result2.config(text = "Nothing entered. Please try again.")
            self.result3.config(text="Please type in your sentence and submit!")

        else:
            ## Process the score for the median
            score.run_diagnostics()
            score = score.diagnostics["Five_num"]["Median"]
            ## Rounding
            score = round(score, 2)
            ## Result
            self.result2.config(text="Your score is "+str(score))

            message = "This is poetic!" if score >=0.5 else "This is not so poetic!"
            self.result3.config(text=message)

    def select_file(self):
        pass


## For developing purposes only
if __name__ == "__main__":
    GUI()