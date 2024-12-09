from tkinter import *
from tkinter.scrolledtext import ScrolledText
from transformers import pipeline
import torch
from huggingface_hub import login


class UI:
    def __init__(self, ui):
        self.ui = ui
        self.first = 0
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.summarizer = None
        self.is_start = False

    def test(self, txt):
        if not self.is_start:
            self.summarizer = pipeline("summarization", model="text_summarization", device=self.device)
            textfield = ScrolledText(self.ui, wrap=WORD)
            textfield.grid(row=3, column=0)
        else:
            textfield.delete("1.0", END)

        res = self.summarizer(txt, max_length=1000, min_length=30, do_sample=False)[0]["summary_text"]
        textfield.insert(END, res)


    def active_ui(self):
        lb = Label(master=self.ui, text="Enter text to review:")
        lb.grid(row=0, column=0)
        textfield = ScrolledText(self.ui, wrap=WORD)
        textfield.grid(row=1, column=0)
        btn = Button(master=self.ui, text='Review', command=lambda: self.test(textfield.get("1.0", END)))
        btn.grid(row=2, column=0)


    def entering_hf_token(self):
        hf_lb = Label(master=self.ui, text="Enter your Huggingface token:")
        hf_lb.grid(row=0, column=0)

        hf_ent = Entry(master=self.ui)
        hf_ent.grid(row=1, column=0)

        btn = None

        def entered_hf_token():
            token = hf_ent.get()
            login(token=token, add_to_git_credential=False)
            if btn is not None:
                btn.destroy()
            hf_ent.destroy()
            hf_lb.destroy()
            self.active_ui()

        btn = Button(master=self.ui, text="Enter", command=entered_hf_token)
        btn.grid(row=2, column=0)

    def go(self):
        lb = Label(master=self.ui, text="Do you have Huggingface token?")
        lb.grid(row=0, column=0)
        def no_hf_token():
            no_button.destroy()
            yes_button.destroy()
            lb.config(text="Please register on Huggingface and generate token")

        def yes_hf_token():
            yes_button.destroy()
            no_button.destroy()
            lb.destroy()
            self.entering_hf_token()
        yes_button = Button(master=self.ui, text="Yes", command=yes_hf_token)
        yes_button.grid(row=1, column=0)
        no_button = Button(master=self.ui, text="No", command=no_hf_token)
        no_button.grid(row=2, column=0)
        # textfield = ScrolledText(self.ui, wrap=WORD)
        # textfield.grid(row=1, column=0)
        # btn = Button(master=self.ui, text='Review', command=lambda: self.test(textfield.get("1.0", END)))
        # btn.grid(row=2, column=0)
        self.ui.mainloop()



if __name__ == "__main__":
    wn = Tk()
    ui = UI(wn)
    ui.go()