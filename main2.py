import os
import os
import cv2
import numpy
import ctypes
import tkinter
from tkinter import filedialog
from PIL import ImageTk, Image
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from util import config
from util import image_processing

ctypes.windll.shcore.SetProcessDpiAwareness(1)

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()

        w = 1430
        h = 850

        self.title("")
        self.geometry(f'{w}x{h}+0+0')
        self.resizable(False, False)

        # initial variable
        self.imagePath = None
        self.imageSize = 270

        self.boolBrightness = tkinter.BooleanVar()
        self.boolContrast = tkinter.BooleanVar()

        self.brightness = tkinter.DoubleVar()
        self.contrast = tkinter.DoubleVar()

        self.classifier = tkinter.IntVar()

        self.classifierList = [
            "SVM", 
            "KNN", 
            "CNN", 
            "Random Forest", 
            "Decision Tree", 
            "Naive Bayes"
        ]

        # initial frame
        self.browseImageFrame()
        self.imageClassificationFrame()

        self.imageSettingFrame()
        self.methodSettingFrame()
        self.performanceMeasurementFrame()
        self.predictionResultFrame()

        self.histogramFrame()

    def browseImageFrame(self):
        self.f0 = tkinter.Frame(self, width=350, height=350, background='#4287f5')
        self.f0.place(x=20, y=40)

        image = Image.open("src/blank.png")
        image = image.resize((self.imageSize, self.imageSize))
        image = ImageTk.PhotoImage(image)

        image1 = tkinter.Label(self.f0, image=image)
        image1.image = image
        image1.place(x=40, y=20)

        tkinter.Button(
            self.f0, 
            text="Load Image", 
            width=12,
            command=self.loadImage).place(x=110, y=310)

    def imageClassificationFrame(self):
        self.f1 = tkinter.Frame(self, width=350, height=350, background='#4287f5')
        self.f1.place(x=390, y=40)

        image = Image.open("src/blank.png")
        image = image.resize((self.imageSize, self.imageSize))
        image = ImageTk.PhotoImage(image)

        image1 = tkinter.Label(self.f1, image=image)
        image1.image = image
        image1.place(x=40, y=20)

        tkinter.Button(
            self.f1, 
            text="Run", 
            width=12,
            command=self.runPredict).place(x=40, y=310)
        
        tkinter.Button(
            self.f1, 
            text="Save", 
            width=12,
            command=self.saveImageAfterPredict).place(x=210, y=310)

    def imageSettingFrame(self):
        self.f2 = tkinter.Frame(self, width=350, height=200, background='#4287f5')
        self.f2.place(x=20, y=420)

        tkinter.Scale(
            self.f2,
            from_=0,
            to=100,
            orient="horizontal",
            borderwidth=5,
            length=200,
            variable=self.brightness).place(x=120,y=10)

        tkinter.Scale(
            self.f2,
            from_=0,
            to=100,
            orient="horizontal",
            borderwidth=5,
            length=200,
            variable=self.contrast).place(x=120,y=80)

        tkinter.Button(
            self.f2, 
            text="Process", 
            width=12,
            command=self.setValue).place(x=100, y=150)

    def methodSettingFrame(self):
        self.f3 = tkinter.Frame(self, width=350, height=250, background='#4287f5')
        self.f3.place(x=390, y=420)

        for i, var in enumerate(self.classifierList):
            tkinter.Radiobutton(
                self.f3,
                text=var,
                value=i,
                variable=self.classifier
            ).place(x=10, y=10+(30)*i)

        self.classifier.set(0)

    def histogramFrame(self):
        self.f4 = tkinter.Frame(self, width=650, height=350, background='#4287f5')
        self.f4.place(x=760, y=40)

    def performanceMeasurementFrame(self):
        self.f5 = tkinter.Frame(self, width=650, height=200, background='#4287f5')
        self.f5.place(x=760, y=420)

        labels = ["Accuracy", "Precission", "Recall"]
        for i in range(len(labels)):
            tkinter.Label(
                self.f5,
                text=labels[i]
            ).place(x=50, y=38*(i+1))

        self.inputAccuracy = tkinter.Entry(self.f5)
        self.inputPrecission = tkinter.Entry(self.f5)
        self.inputRecall = tkinter.Entry(self.f5)

        self.inputAccuracy.place(x=150,y=38)
        self.inputPrecission.place(x=150,y=76)
        self.inputRecall.place(x=150,y=114)

    def predictionResultFrame(self):
        self.f6 = tkinter.Frame(self, width=650, height=200, background='#4287f5')
        self.f6.place(x=760, y=640)

        labels = ["Sickness", "Dead", "Normal"]
        for i in range(len(labels)):
            tkinter.Label(
                self.f6,
                text=labels[i]
            ).place(x=50, y=38*(i+1))

        self.inputAccuracy = tkinter.Entry(self.f6)
        self.inputPrecission = tkinter.Entry(self.f6)
        self.inputRecall = tkinter.Entry(self.f6)

        self.inputAccuracy.place(x=150,y=38)
        self.inputPrecission.place(x=150,y=76)
        self.inputRecall.place(x=150,y=114)

    # function
    def loadImage(self):
        file = filedialog.askopenfile(
            mode="r", 
            filetypes=[("Image file", ["*.png", "*.jpeg", "*jpg", "*.bmp"])]
        )

        if file:
            self.imagePath = os.path.abspath(file.name)

            img = cv2.imread(self.imagePath)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            pilimg = Image.fromarray(img)
            pilimg = pilimg.resize((self.imageSize, self.imageSize))
            pilimg = ImageTk.PhotoImage(pilimg)

            image1 = tkinter.Label(self.f0, image=pilimg)            
            image1.image = pilimg
            image1.place(x=40, y=20)

    def setValue(self):
        brightness = int(self.brightness.get())
        contrast = int(self.contrast.get())

        img = cv2.imread(self.imagePath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = cv2.addWeighted(img, contrast, img, 0, brightness)

        pilimg = Image.fromarray(img)
        pilimg = pilimg.resize((self.imageSize, self.imageSize))
        pilimg = ImageTk.PhotoImage(pilimg)

        image1 = tkinter.Label(self.f0, image=pilimg)            
        image1.image = pilimg
        image1.place(x=40, y=20)

        vals = cv2.imread(self.imagePath).mean(axis=2).flatten()

        fig = Figure(figsize=(6.2, 3.2), dpi=80)
        fig.add_subplot(111).hist(vals, 255)
        
        canvas = FigureCanvasTkAgg(fig, master=self.f4)  
        canvas.draw()
        canvas.get_tk_widget().place(x=10, y=10)

    def runPredict(self):
        print(self.classifier.get())

    def saveImageAfterPredict(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()
