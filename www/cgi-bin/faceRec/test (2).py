import os
import sys
import cv2
import numpy as np

x=[]
f=[]
y=[0,0,1,2]

im = cv2.imread('img/gregBacker/gregBacker.0.jpg', cv2.IMREAD_GRAYSCALE)
x.append(np.asarray(im, dtype=np.uint8))
im = cv2.imread('img/gregBacker/gregBacker.1.jpg', cv2.IMREAD_GRAYSCALE)
x.append(np.asarray(im, dtype=np.uint8))
im = cv2.imread('img/JianPei/JianPei.0.jpg', cv2.IMREAD_GRAYSCALE)
x.append(np.asarray(im, dtype=np.uint8))
im = cv2.imread('img/AlexandraFedorova/AlexandraFedorova.0.jpg', cv2.IMREAD_GRAYSCALE)
x.append(np.asarray(im, dtype=np.uint8))

mode = cv2.createEigenFaceRecognizer()
mode.train(np.asarray(x), np.asarray(y))
[e_label, e_confidence] = mode.predict(im)
print "Predicted label = %d (confidence=%.2f)" % (e_label, e_confidence)

modl = cv2.createLBPHFaceRecognizer()
modl.train(np.asarray(x), y)
im = cv2.imread('test8.jpg', cv2.IMREAD_GRAYSCALE)
[p_label, p_confidence] = modl.predict(im)
print "Predicted label = %d (confidence=%.2f)" % (p_label, p_confidence)

