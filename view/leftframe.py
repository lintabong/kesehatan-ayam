import os
import cv2
import numpy
import tkinter
from PIL import ImageTk, Image
from tkinter import filedialog

from util import config


class LeftFrame(tkinter.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.configuration = config.read()

        self.config(
            width=container.winfo_screenwidth(), 
            height=container.winfo_screenheight(), 
            background=self.configuration["bgMain"])
        self.place(x=0, y=0)

        self.boolBrightening = tkinter.BooleanVar()
        self.boolContrassStrect = tkinter.BooleanVar()
        self.boolSmoothing = tkinter.BooleanVar()
        self.boolSharpening = tkinter.BooleanVar()

        self.brightening = tkinter.DoubleVar()
        self.contrastStrect = tkinter.DoubleVar()
        self.smoothing = tkinter.DoubleVar()
        self.sharpening = tkinter.DoubleVar()

        self.loadImageFrame()
        self.resultImageFrame()

    def loadImageFrame(self):
        self.f0 = tkinter.Frame(self, width=350, height=350, background=self.configuration["bgFrame1"])
        self.f0.place(x=400, y=100)

        self.f1 = tkinter.LabelFrame(self.f0, width=330, height=330, background=self.configuration["bgFrame1"], text="  Input Image  ")
        self.f1.place(x=10, y=10)

        image = Image.open("src/blank.png")
        image = image.resize((200, 200))
        image = ImageTk.PhotoImage(image)

        image1 = tkinter.Label(self.f1, image=image)
        image1.image = image
        image1.place(x=10, y=10)

        tkinter.Button(
            self.f1, 
            text="Browse", 
            width=12, 
            command=self.loadImage).place(x=10, y=260)
    
    def loadImage(self):
        file = filedialog.askopenfile(
            mode = "r", 
            filetypes = [("Image file", ["*.png", "*.jpeg", "*jpg", "*.bmp"])]
        )

        if file:
            pathfile = os.path.abspath(file.name)

            pilimg = Image.fromarray(cv2.imread(pathfile))
            pilimg = pilimg.resize((200, 200))
            pilimg = ImageTk.PhotoImage(pilimg)

            image1 = tkinter.Label(self.f1, image=pilimg)            
            image1.image = pilimg
            image1.place(x=10, y=10)

            configuration = config.read()
            configuration["imagePath"] = pathfile
            config.write(configuration)

    def resultImageFrame(self):
        self.f2 = tkinter.Frame(self, width=350, height=350, background=self.configuration["bgFrame1"])
        self.f2.place(x=770, y=100)

        self.f3 = tkinter.LabelFrame(self.f2, width=330, height=330, background=self.configuration["bgFrame1"], text="  Result of Image Enhancement  ")
        self.f3.place(x=10, y=10)

        image = Image.open("src/blank.png")
        image = image.resize((200, 200))
        image = ImageTk.PhotoImage(image)

        image1 = tkinter.Label(self.f3, image=image)
        image1.image = image
        image1.place(x=10, y=10)

        tkinter.Button(
            self.f3, 
            text="Save", 
            width=12).place(x=10, y=260)
        
        self.f4 = tkinter.Frame(self, width=720, height=340, background=self.configuration["bgFrame1"])
        self.f4.place(x=400, y=470)

        self.f5 = tkinter.LabelFrame(self.f4, width=700, height=320, background=self.configuration["bgFrame1"], text="  Image Enhancement Processing  ")
        self.f5.place(x=10, y=10)

        labels     = ["Brightening", "Contrast Strect", "Smoothing", "Sharpening"]
        boolLabels = [self.boolBrightening, self.boolContrassStrect, self.boolSmoothing, self.boolSharpening]
        for i, var in enumerate([self.brightening, self.contrastStrect, self.smoothing, self.sharpening]):
            tkinter.Checkbutton(
                self.f5,
                variable=boolLabels[i],
                onvalue=True,
                offvalue=False
            ).place(x=10,y=38+(55)*i)

            tkinter.Label(
                self.f5,
                text=labels[i]
            ).place(x=50,y=38+(55)*i)

            tkinter.Scale(
                self.f5,
                from_=0,
                to=100,
                orient="horizontal",
                background=self.configuration["bgFrame1"],
                borderwidth=5,
                length=450,
                variable=var
            ).place(x=210,y=10+(55)*i)

        tkinter.Button(
            self.f5, 
            text="Run", 
            width=12,
            command=self.runImageEnhancement).place(x=10, y=250)

    def runImageEnhancement(self):
        configuration = config.read()
        imagePath = configuration["imagePath"]

        img = cv2.imread(imagePath)
        if self.boolBrightening.get():
            img = cv2.convertScaleAbs(img, beta=int(self.brightening.get()))
        
        if self.boolContrassStrect.get():
            img = cv2.convertScaleAbs(img, alpha=int(self.contrastStrect.get()))
        
        if self.boolSmoothing.get():
            img = cv2.blur(img, (int(self.smoothing.get()), int(self.smoothing.get())))

        if self.boolSharpening.get():
            img = cv2.filter2D(img, -1, numpy.array([[0, -1, 0], [-1, int(self.sharpening.get()), -1], [0, -1, 0]]))

        pilimg = Image.fromarray(img)
        pilimg = pilimg.resize((200, 200))
        pilimg = ImageTk.PhotoImage(pilimg)

        image1 = tkinter.Label(self.f3, image=pilimg)            
        image1.image = pilimg
        image1.place(x=10, y=10)

        configuration = config.read()
        configuration["enhancement"]["brightening"]["value"]  = int(self.brightening.get())
        configuration["enhancement"]["brightening"]["status"] = self.boolBrightening.get()
        configuration["enhancement"]["contrass"]["value"]  = int(self.contrastStrect.get())
        configuration["enhancement"]["contrass"]["status"] = self.boolContrassStrect.get()
        configuration["enhancement"]["smoothing"]["value"]  = int(self.smoothing.get())
        configuration["enhancement"]["smoothing"]["status"] = self.boolSmoothing.get()
        configuration["enhancement"]["sharpening"]["value"]  = int(self.sharpening.get())
        configuration["enhancement"]["sharpening"]["status"] = self.boolSharpening.get()
        config.write(configuration)

    def saveImage(self):
        pass