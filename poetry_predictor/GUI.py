#####################
### GUI Associated classes and functions
#####################

## Importing necessary modules
from tkinter import Tk, Entry, Label, Button

class GUI:
    ## Start the program:
    def __init__(self, predictor):

        ## Model to use
        self.predictor = predictor

        ## Create a window
        self.window = Tk()
        self.window.title("Poetry Predictor")
        self.window.geometry("420x480")

        ## Welcome Message
        self.wcm1 = Label(self.window, text = "Welcome to the Poetry Predictor!", font=("Times", 20))
        self.wcm2 = Label(self.window, text = "Find out how poetic you are!", font=("Times", 15))
        self.wcm3 = Label(self.window, text = "v.0.1.2", font=("Times", 15))

        self.wcm1.grid(row=0, column=0)
        self.wcm2.grid(row=1, column=0)
        self.wcm3.grid(row=2, column=0)

        self.divider1 =Label(self.window, text="~~~~~~~~~~~~~~~~~~~~~~~~~~", font=("Times",20))
        self.divider1.grid(row=3, column=0, pady=10)

        ## Poetry Input
        self.input = Entry(self.window, width=40,font=("Times",13))
        self.input.grid(row=4, column=0, pady=10)

        ## Button
        self.predict_button = Button(self.window, text="Submit",font=("Times",20), command=self.submit)
        self.predict_button.grid(row=5, column=0)

        ## Results
        self.divider2 = Label(self.window, text="~~~~~~~~~~~~~~~~~~~~~~~~~~", font=("Times",20))
        self.result1 = Label(self.window, text="Your Result", font=("Times",20))
        self.result2 = Label(self.window, text="No result yet!", font=("Times",17))
        self.result3 = Label(self.window, text="Please type in your sentence and submit!", font=("Times",17))
        self.divider2.grid(row=6, column=0, pady=15)
        self.result1.grid(row=7,column=0, pady=10)
        self.result2.grid(row=8,column=0)
        self.result3.grid(row=9,column=0)

        ## Keep the window open
        self.window.mainloop()


    def submit(self):
        ## Get the user input
        input = self.input.get()

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