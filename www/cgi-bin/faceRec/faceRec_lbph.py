import os
import sys
import cv2
import numpy as np
import URLopen as uo
import faceRec_init as fi

def readLabel(csvPath):
    names = [line.strip().split(';') for line in open(csvPath)]
    labels = {l[0]:l[1] for l in names}
    return labels

def rePath(imgpath,xml="",csv='csv.txt'):
    model = cv2.createLBPHFaceRecognizer()
    model.load(xml+"face-lbph.yml")
    try:
        im = cv2.imread(imgpath, cv2.IMREAD_GRAYSCALE)
    except IOError, (errno, strerror):
        print "I/O error({0}): {1}".format(errno, strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
    [p_label, p_confidence] = model.predict(im)
    return [p_label,readLabel(csv)[str(p_label)],p_confidence]

def reImg(img,xml=""):
    model = cv2.createLBPHFaceRecognizer()
    model.load(xml+"face-lbph.yml")
    [p_label, p_confidence] = model.predict(img)
    return p_label

if __name__ == "__main__":
    model = cv2.createLBPHFaceRecognizer()
    model.load("face-lbph.yml")
    im = cv2.imread('test7.jpg', cv2.IMREAD_GRAYSCALE)
    labels=readLabel('csv.txt')
    [p_label, p_confidence] = model.predict(im)
    # Print it:
    print "Predicted label = %d:%s (confidence=%.2f)" % (p_label,labels[str(p_label)], p_confidence)
