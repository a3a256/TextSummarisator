from tkinter import *
from tkinter.scrolledtext import ScrolledText
from transformers import pipeline
import torch


class UI:
    def __init__(self, ui):
        self.ui = ui
        self.first = 0
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.summarizer = pipeline("summarization", model="text_summarization", device=device)
        self.is_start = False

    def test(self, txt):
        if not self.is_start:
            textfield = ScrolledText(self.ui, wrap=WORD)
            textfield.grid(row=3, column=0)
        else:
            textfield.delete("1.0", END)

        res = self.summarizer(txt, max_length=1000, min_length=30, do_sample=False)[0]["summary_text"]
        textfield.insert(END, res)

    def go(self):
        lb = Label(master=self.ui, text="Enter the text to summarise")
        lb.grid(row=0, column=0)
        textfield = ScrolledText(self.ui, wrap=WORD)
        textfield.grid(row=1, column=0)
        btn = Button(master=self.ui, text='Review', command=lambda: self.test(textfield.get("1.0", END)))
        btn.grid(row=2, column=0)
        self.ui.mainloop()



if __name__ == "__main__":
    wn = Tk()
    ui = UI(wn)
    ui.go()