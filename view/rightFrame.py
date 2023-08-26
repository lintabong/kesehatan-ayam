import os
import cv2
import numpy
import tkinter
from tkinter import filedialog
from PIL import ImageTk, Image
from PIL import ImageTk, Image
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from util import config
from util import image_processing

class RightFrame(tkinter.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.configuration = config.read()
        self.yStart        = int(os.getenv("Y_START"))
        self.bgMain        = f'#{os.getenv("BACKGROUND_MAIN")}'
        self.bgFrame0      = f'#{os.getenv("BACKGROUND_FRAME_0")}'
        self.bgFrame1      = f'#{os.getenv("BACKGROUND_FRAME_1")}'
        self.imgSize       = int(os.getenv("IMAGE_SIZE"))

        self.config(
            width=container.winfo_screenwidth() - (int(container.winfo_screenwidth()/2)), 
            height=container.winfo_screenheight() - self.yStart, 
            background=self.bgMain
        )
        self.place(x=int(container.winfo_screenwidth()/2), y=self.yStart)
        
        self.classifier = tkinter.IntVar()

        self.analysisText = [["", "0", "45", "90", "135", "Average"],
                             ["Contrass", "", "", "", "", ""],
                             ["Correlation", "", "", "", "", ""],
                             ["Energy", "", "", "", "", ""],
                             ["Homogenity", "", "", "", "", ""]
        ]

        self.classifierList = ["None", 
                               "Regression", 
                               "Random Forest", 
                               "Decision Tree", 
                               "k-NN", 
                               "Naive Bayes", 
                               "CNN", 
                               "SVM", 
                               "Modification SVM"
        ]

        self.featureExtractionFrame()
        self.displayImageFrame()
        self.resultFrame()
        self.histogramFrame()
        self.thermalAnalystFrame()

    def featureExtractionFrame(self):
        f0 = tkinter.Frame(self, width=270, height=350, background=self.bgFrame1)
        f0.place(x=10, y=10)

        self.f1 = tkinter.LabelFrame(
            f0, 
            width=250, 
            height=330, 
            background=self.bgFrame1, 
            text="  Feature Extraction/Classifier  "
        )
        self.f1.place(x=10, y=10)

        for i, var in enumerate(self.classifierList):
            tkinter.Radiobutton(
                self.f1,
                text=var,
                value=i,
                variable=self.classifier
            ).place(x=10, y=10+(30)*i)

        self.classifier.set(0)

    def displayImageFrame(self):
        f0 = tkinter.Frame(self, width=350, height=350, background=self.configuration["bgFrame1"])
        f0.place(x=300, y=10)

        self.f2 = tkinter.LabelFrame(
            f0, 
            width=330, 
            height=330, 
            background=self.bgFrame1, 
            text="  Input Image  "
        )
        self.f2.place(x=10, y=10)

        image = Image.open("src/blank.png")
        image = image.resize((self.imgSize, self.imgSize))
        image = ImageTk.PhotoImage(image)

        image1 = tkinter.Label(self.f2, image=image)
        image1.image = image
        image1.place(x=10, y=10)

        tkinter.Button(
            self.f2, 
            text="Load", 
            width=10, 
            command=self.loadImage).place(x=10, y=260)
        
        tkinter.Button(
            self.f2, 
            text="Save", 
            width=10, 
            command=self.saveImage).place(x=110, y=260)
        
        tkinter.Button(
            self.f2, 
            text="Predict", 
            width=10, 
            command=self.predictImage).place(x=210, y=260)

    def resultFrame(self):
        f0 = tkinter.Frame(self, width=270, height=660, background=self.bgFrame1)
        f0.place(x=670, y=10)

        self.f3 = tkinter.LabelFrame(
            f0, 
            width=250, 
            height=640, 
            background=self.bgFrame1,
            text="  Result  "
        )
        self.f3.place(x=10, y=10)

        texts = ["Prediction", 
                 "Accuracy", 
                 "Health Condition of Chicken", 
                 "Entropi", 
                 "Deviation Standard", 
                 "Quality Index"
        ]

        for i, text in enumerate(texts):
            tkinter.Label(
                self.f3, 
                text=text
            ).place(x=10, y=10+(80)*i)

        self.inputPrediction = tkinter.Entry(self.f3)
        self.inputAccuracy = tkinter.Entry(self.f3)
        self.inputHealth = tkinter.Entry(self.f3)
        self.inputEntropi = tkinter.Entry(self.f3)
        self.inputDeviation = tkinter.Entry(self.f3)
        self.inputQualityIndex = tkinter.Entry(self.f3)

        vars = [self.inputPrediction, 
                self.inputAccuracy, 
                self.inputHealth, 
                self.inputEntropi, 
                self.inputDeviation, 
                self.inputQualityIndex
        ]

        for i, var in enumerate(vars):
            var.place(x=20, y=40+(80)*i)

        tkinter.Button(
            self.f3, 
            text="Save", 
            width=12, 
            command=self.saveResult).place(x=20, y=560)
        
    def histogramFrame(self):
        f0 = tkinter.Frame(self, width=640, height=290, background=self.bgFrame1)
        f0.place(x=10, y=380)

        self.f4 = tkinter.LabelFrame(
            f0, 
            width=620, 
            height=270, 
            background=self.bgFrame1, 
            text="  Histogram  "
        )
        self.f4.place(x=10, y=10)

        self.hisFrame = tkinter.Frame(self.f4, width=567, height=342)
        self.hisFrame.place(x=0, y=0)

    def thermalAnalystFrame(self):
        f0 = tkinter.Frame(self, width=640, height=230, background=self.bgFrame1)
        f0.place(x=10, y=690)

        self.f5 = tkinter.LabelFrame(
            f0, 
            width=620, 
            height=210, 
            background=self.bgFrame1, 
            text="  Thermal Analyst  "
        )
        self.f5.place(x=10, y=10)

        for i in range(6):
            for j in range(5):
                f2 = tkinter.Frame(self.f5, height=30, width=95 , background="#ffffff")
                tkinter.Label(f2, bg="#ffffff", text=self.analysisText[j][i]).place(anchor="c", relx=.5, rely=.5)
                f2.place(x=5+(99*i), y=5+(34*j))
        
    def loadImage(self):
        configuration = config.read()
        imagePath = configuration["imagePath"]

        img = cv2.imread(imagePath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        pilimg = Image.fromarray(img)
        pilimg = pilimg.resize((self.configuration["imageSize"], self.configuration["imageSize"]))
        pilimg = ImageTk.PhotoImage(pilimg)

        image1 = tkinter.Label(self.f2, image=pilimg)            
        image1.image = pilimg
        image1.place(x=10, y=10)

    def saveImage(self):
        pass

    def predictImage(self):
        self.inputPrediction.delete(0, tkinter.END)
        self.inputAccuracy.delete(0, tkinter.END)
        self.inputHealth.delete(0, tkinter.END)
        self.inputEntropi.delete(0, tkinter.END)
        self.inputDeviation.delete(0, tkinter.END)
        self.inputQualityIndex.delete(0, tkinter.END)
    
        configuration = config.read()
        imagePath = configuration["imagePath"]

        img = cv2.imread(imagePath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.analysisText = image_processing.GLCM(img)
        self.thermalAnalystFrame()
    
        vals = img.mean(axis=2).flatten()

        fig = Figure(figsize=(5.9, 2.0), dpi=80)
        fig.add_subplot(111).hist(vals, 255)
        
        canvas = FigureCanvasTkAgg(fig, master=self.hisFrame)  
        canvas.draw()
        canvas.get_tk_widget().place(x=10, y=10)

        label, accuracy = image_processing.run(imagePath, self.classifier.get())
        category        = image_processing.get_category(self.analysisText[1][5])
        H               = image_processing.entropy(round(accuracy, 3))
        sd              = (100 - round(accuracy, 3))/5

        self.inputPrediction.insert(0, label)
        self.inputAccuracy.insert(0, round(accuracy, 3))
        self.inputHealth.insert(0, category)
        self.inputEntropi.insert(0, round(H, 3))
        self.inputDeviation.insert(0, round(sd, 3))
        self.inputQualityIndex.insert(0, round(accuracy, 3))

    def saveResult(self):
        pass