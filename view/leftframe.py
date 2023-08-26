import os
import cv2
import numpy
import tkinter
from PIL import ImageTk, Image
from tkinter import filedialog
from dotenv import load_dotenv

from util import config

load_dotenv()


class LeftFrame(tkinter.Frame):
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
        self.place(x=0, y=self.configuration["yFrame"])

        self.boolBrightening    = tkinter.BooleanVar()
        self.boolContrassStrect = tkinter.BooleanVar()
        self.boolSmoothing      = tkinter.BooleanVar()
        self.boolSharpening     = tkinter.BooleanVar()

        self.brightening        = tkinter.DoubleVar()
        self.contrastStrect     = tkinter.DoubleVar()
        self.smoothing          = tkinter.DoubleVar()
        self.sharpening         = tkinter.DoubleVar()

        self.loadImageFrame()
        self.resultImageFrame()
        self.imageEnhancementFrame()
        self.cameraSettingFrame()

    def loadImageFrame(self):
        f0 = tkinter.Frame(self, width=350, height=350, background=self.bgFrame1)
        f0.place(x=10, y=10)

        self.f1 = tkinter.LabelFrame(
            f0, 
            width=330, 
            height=330, 
            background=self.bgFrame1, 
            text="  Input Image  "
        )
        self.f1.place(x=10, y=10)

        image = Image.open("src/blank.png")
        image = image.resize((self.imgSize, self.imgSize))
        image = ImageTk.PhotoImage(image)

        image1 = tkinter.Label(self.f1, image=image)
        image1.image = image
        image1.place(x=10, y=10)

        tkinter.Button(
            self.f1, 
            text="Browse", 
            width=12, 
            command=self.loadImage).place(x=10, y=260)

    def resultImageFrame(self):
        f0 = tkinter.Frame(self, width=350, height=350, background=self.bgFrame1)
        f0.place(x=380, y=10)

        self.f2 = tkinter.LabelFrame(
            f0, 
            width=330, 
            height=330, 
            background=self.bgFrame1, 
            text="  Result of Image Enhancement  "
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
            text="Save", 
            width=12,
            command=self.saveImage).place(x=10, y=260)
        
    def imageEnhancementFrame(self):    
        f0 = tkinter.Frame(self, width=720, height=340, background=self.bgFrame1)
        f0.place(x=10, y=380)

        self.f3 = tkinter.LabelFrame(
            f0, 
            width=700, 
            height=320, 
            background=self.bgFrame1, 
            text="  Image Enhancement Processing  "
        )
        self.f3.place(x=10, y=10)

        labels     = ["brightening", "contrass", "smoothing", "sharpening"]
        boolLabels = [self.boolBrightening, self.boolContrassStrect, self.boolSmoothing, self.boolSharpening]
        for i, var in enumerate([self.brightening, self.contrastStrect, self.smoothing, self.sharpening]):
            tkinter.Checkbutton(
                self.f3,
                variable=boolLabels[i],
                onvalue=True,
                offvalue=False
            ).place(x=10,y=38+(55)*i)

            tkinter.Label(
                self.f3,
                text=labels[i]
            ).place(x=50,y=38+(55)*i)

            scale = tkinter.Scale(
                self.f3,
                from_=0,
                to=100,
                orient="horizontal",
                background=self.configuration["bgFrame1"],
                borderwidth=5,
                length=450,
                variable=var
            )
            scale.set(self.configuration["enhancement"][labels[i]]["value"])
            scale.place(x=210,y=10+(55)*i)

        tkinter.Button(
            self.f3, 
            text="Run", 
            width=12,
            command=self.runImageEnhancement).place(x=10, y=250)
    
    def cameraSettingFrame(self):
        f0 = tkinter.Frame(self, width=720, height=230, background=self.bgFrame1)
        f0.place(x=10, y=740)

        self.f4 = tkinter.LabelFrame(
            f0, 
            width=700, 
            height=210, 
            background=self.bgFrame1, 
            text="  Camera Setting  "
        )
        self.f4.place(x=10, y=10)

        self.inputDistance = tkinter.Entry(self.f4)
        self.inputLighting = tkinter.Entry(self.f4)
        self.inputBodyTemperature = tkinter.Entry(self.f4)
        self.inputHealthCondition = tkinter.Entry(self.f4)

        texts = ["Distance (cm)", "Lighting", "Body Temperature", "Health Condition"]
        for i, var in enumerate([self.inputDistance, self.inputLighting, self.inputBodyTemperature, self.inputHealthCondition]):
            tkinter.Label(self.f4, text=texts[i]).place(x=5, y=10+(40)*i)
            var.place(x=150,y=10+(40)*i)

        tkinter.Button(
            self.f4, 
            text="Save", 
            width=12, 
            height=4,
            command=self.saveCameraSetting).place(x=420, y=10)

    def loadImage(self):
        file = filedialog.askopenfile(
            mode="r", 
            filetypes=[("Image file", ["*.png", "*.jpeg", "*jpg", "*.bmp"])]
        )

        if file:
            imagePath = os.path.abspath(file.name)

            img = cv2.imread(imagePath)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            pilimg = Image.fromarray(img)
            pilimg = pilimg.resize((self.imgSize, self.imgSize))
            pilimg = ImageTk.PhotoImage(pilimg)

            image1 = tkinter.Label(self.f1, image=pilimg)            
            image1.image = pilimg
            image1.place(x=10, y=10)

            image1 = tkinter.Label(self.f2, image=pilimg)            
            image1.image = pilimg
            image1.place(x=10, y=10)

            configuration = config.read()
            configuration["imagePath"] = imagePath
            config.write(configuration)

    def saveImage(self):
        pass
    
    def runImageEnhancement(self):
        configuration = config.read()
        imagePath = configuration["imagePath"]

        img = cv2.imread(imagePath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if self.boolBrightening.get():
            img = cv2.convertScaleAbs(img, beta=int(self.brightening.get()))
        
        if self.boolContrassStrect.get():
            img = cv2.convertScaleAbs(img, alpha=int(self.contrastStrect.get()))
        
        if self.boolSmoothing.get():
            img = cv2.blur(img, (int(self.smoothing.get()), int(self.smoothing.get())))

        if self.boolSharpening.get():
            img = cv2.filter2D(img, -1, numpy.array([[0, -1, 0], [-1, int(self.sharpening.get()), -1], [0, -1, 0]]))

        pilimg = Image.fromarray(img)
        pilimg = pilimg.resize((self.configuration["imageSize"], self.configuration["imageSize"]))
        pilimg = ImageTk.PhotoImage(pilimg)

        image1 = tkinter.Label(self.f2, image=pilimg)            
        image1.image = pilimg
        image1.place(x=10, y=10)

        configuration = config.read()
        configuration["enhancement"]["brightening"]["value"]  = int(self.brightening.get())
        configuration["enhancement"]["contrass"]["value"]     = int(self.contrastStrect.get())
        configuration["enhancement"]["smoothing"]["value"]    = int(self.smoothing.get())
        configuration["enhancement"]["sharpening"]["value"]   = int(self.sharpening.get())
        configuration["enhancement"]["brightening"]["status"] = self.boolBrightening.get()
        configuration["enhancement"]["contrass"]["status"]    = self.boolContrassStrect.get()
        configuration["enhancement"]["smoothing"]["status"]   = self.boolSmoothing.get()
        configuration["enhancement"]["sharpening"]["status"]  = self.boolSharpening.get()
        config.write(configuration)

    def saveCameraSetting(self):
        pass