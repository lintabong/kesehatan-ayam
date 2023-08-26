import os
import tkinter
from dotenv import load_dotenv

from util import config

load_dotenv()


class TitleFrame(tkinter.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.configuration = config.read()
        self.bgMain   = f'#{os.getenv("BACKGROUND_MAIN")}'
        self.title    = os.getenv("TITLE")

        self.config(width=container.winfo_screenwidth(), height=30, background=self.bgMain)
        self.place(x=0, y=10)

        self.title = tkinter.Label(
            self, 
            bg=self.bgMain, 
            text=self.title,
            font=("Arial", 22))

        self.title.place(anchor="c", relx=.5, rely=.5)
