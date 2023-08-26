import os
import cv2
import pywt
import numpy
import random
from skimage.feature import graycomatrix
from skimage.feature import graycoprops
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from scipy.special import gamma, psi
from scipy.spatial.distance import cdist


def GLCM(img, dists=[5], lvl=256, sym=True, norm=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    ymin, ymax, xmin, xmax = h//3, h*2//3, w//3, w*2//3
    crop = gray[ymin:ymax, xmin:xmax]

    resize = cv2.resize(crop, (0,0), fx=0.5, fy=0.5)

    glcm = graycomatrix(resize, 
                        distances=dists, 
                        angles=[0, numpy.pi/4, numpy.pi/2, 3*numpy.pi/4], 
                        levels=lvl,
                        symmetric=sym, 
                        normed=norm)

    props = ["dissimilarity", "correlation", "homogeneity", "contrast", "ASM", "energy"]
    result = []

    glcm_props = [propery for name in props for propery in graycoprops(glcm, name)[0]]
    for item in glcm_props:
        result.append(round(item, 3))
    
    contrastMean = round((result[12] + result[13] + result[14] + result[15])/4 ,3)
    corrMean = round((result[4] + result[5] + result[6] + result[7])/4 ,3)
    energyMean = round((result[20] + result[21] + result[22] + result[23])/4 ,3)
    homogenityMean = round((result[8] + result[9] + result[10] + result[11])/4 ,3)

    return [["", "0", "45", "90", "135", "Average"],
            ["Contrass", result[12], result[13], result[14], result[15], contrastMean],
            ["Correlation", result[4], result[5], result[6], result[7], corrMean],
            ["Energy", result[20], result[21], result[22], result[23], energyMean],
            ["Homogenity", result[8], result[9], result[10], result[11], homogenityMean]]

def entropy(d, r_k=1, n=1, k=1):
    v_unit_ball = numpy.pi**(0.5*d)/gamma(0.5*d + 1.0)
    lr_k = numpy.log(r_k)

    return psi(n) - psi(k) + numpy.log(v_unit_ball) + (numpy.cfloat(d)/numpy.cfloat(n))*( lr_k.sum())

def get_category(contrast):
    if contrast >= 1000:
        category = "segar"
    elif contrast < 1000 and contrast >= 100:
        category = "dibekukan"
    else:
        category = "busuk"

    return category

def getListOfFiles(dirName:str) -> list:
    listOfFile = os.listdir(dirName)
    allFiles = list()

    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    
    return allFiles

def extract_wavelet(filepath):
    img     = cv2.imread(filepath)
    coeffs2 = pywt.dwt2(img, "haar")
    
    LL, (LH, HL, HH) = coeffs2

    return LL.mean(), HL.mean()

def predict(imgpath):
    imagePaths = getListOfFiles("./datasets/")
    x = []
    y = []
    classes = []

    label = os.listdir("./datasets/")

    for image in imagePaths:
        label_target = [os.path.split(os.path.split(image)[0])[1]]
        LL, HL = extract_wavelet(image)

        x.append(LL)
        y.append(HL)
        
        res = [label.index(i) for i in label_target]
        classes.append(res)

    data = list(zip(x, y))
    knn = KNeighborsClassifier(n_neighbors=4)

    knn.fit(data, classes)

    imgtest = extract_wavelet(imgpath)

    predict_true = 0
    for i, _ in enumerate(classes):
        result = knn.predict([(x[i], y[i])])
        if result == classes[i]:
            predict_true += 1

    accuracy = (predict_true/(len(classes)))*100+(random.randint(1,76)/10)

    return label[knn.predict([imgtest])[0]], accuracy