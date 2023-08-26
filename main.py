import os
import ctypes
import tkinter
from dotenv import load_dotenv

from util import config
from view.leftframe import LeftFrame
from view.titleFrame import TitleFrame
from view.rightFrame import RightFrame

ctypes.windll.shcore.SetProcessDpiAwareness(1)
load_dotenv()


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.configuration = config.read()
        self.bgMain        = f'#{os.getenv("BACKGROUND_MAIN")}'

        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()

        self.title("")
        self.geometry(f'{w}x{h}+0+0')
        self.resizable(False, False)
        self.config(background=self.bgMain)

        TitleFrame(self)
        LeftFrame(self)
        RightFrame(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
