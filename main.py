import ctypes
import tkinter

ctypes.windll.shcore.SetProcessDpiAwareness(1)

from util import config
from view.leftframe import LeftFrame


class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        configuration = config.read()

        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()

        self.title("GUI Deteksi Daging")
        self.geometry(f'{w}x{h}+0+0')
        self.resizable(False, False)
        self.config(background=configuration["bgMain"])
        # self.overrideredirect(1)

        LeftFrame(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()
