## Import necessary module
from tkinter import *
import numpy as np
from tensorflow import keras
import gensim as gs
from nltk.tokenize import word_tokenize

def main():

    ## Initialize and load model
    new_program = Initialize()
    model = new_program.load_model()
    dict = new_program.load_dict()

    newGUI = GUI(model, dict)


class GUI:
    ## Start the program:
    def __init__(self, model, dict):

        ## Model to use
        self.model = model
        self.dict = dict

        ## Create a window
        self.window = Tk()
        self.window.title("Poetry Predictor")
        self.window.geometry("420x480")

        ## Welcome Message
        self.wcm1 = Label(self.window, text = "Welcome to the Poetry Predictor!", font=("Times", 20))
        self.wcm2 = Label(self.window, text = "Find out how poetic you are!", font=("Times", 15))
        self.wcm3 = Label(self.window, text = "v.0.1.0", font=("Times", 15))

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
        new_predictor = Predictor(input, self.model, self.dict)
        input = new_predictor.proprocess()
        score = new_predictor.predict(input)

        self.result2.config(text="Your score is "+str(score))

        message = "This is poetic!" if score >=0.5 else "This is not so poetic!"
        self.result3.config(text=message)


class Initialize():

    def load_dict(self):
        word_dictionary = gs.corpora.Dictionary.load_from_text(fname="../Models/word_dictionary_complete.txt")
        return word_dictionary

    def load_model(self):
        json_file = open('../Models/sent_model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        sent_model = keras.models.model_from_json(loaded_model_json)
        # load weights into new model
        sent_model.load_weights("../Models/sent_model.h5")

        return sent_model


class Predictor():

    ## Constructor
    def __init__(self, input, model, dict):
        self.input = input
        self.model = model
        self.dict = dict

    def predict(self, input):
        result = self.model.predict(input)
        result = result.tolist()
        score = result[0][0]

        return score

    ## Preprocess the input
    def proprocess(self):
        ## Tokenize and to lower
        sent_token = self.input.lower()
        sent_token = word_tokenize(input)

        ## Word to index
        id_sent = []
        for words in sent_token:
            try:
                self.dict.token2id.get(words) > 0
                id_sent.append(self.dict.token2id.get(words))
            except:
                id_sent.append(0)

        ## Padding
        sent_test = [id_sent]
        sent_test = keras.preprocessing.sequence.pad_sequences(sent_test, maxlen=456)

        return sent_test


if __name__ == "__main__":
    main()