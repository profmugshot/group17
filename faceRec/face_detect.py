#!/usr/bin/python
 
# face_detect.py
 
# Face Detection using OpenCV. Based on sample code from:
# http://python.pastebin.com/m76db1d6b
 
# Usage: python face_detect.py <image_file>
 
import sys, os
import cv2 as cv

def detectObjects(image):
    """Converts an image to grayscale and prints the locations of any 
         faces found"""
    grayscale = cv.cvCreateImage((image.width, image.height), 8, 1)
    cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)
 
    storage = cv.CreateMemStorage(0)
    cv.ClearMemStorage(storage)
    cvE.qualizeHist(grayscale, grayscale)
    cascade = cv.LoadHaarClassifierCascade(
        '/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml',
        cvSize(1,1))
    faces = cv.HaarDetectObjects(grayscale, cascade, storage, 1.2, 2,
                                                         cv.CV_HAAR_DO_CANNY_PRUNING)
 
    if faces:
        for f in faces:
            print("[(%d,%d) -> (%d,%d)]" % (f.x, f.y, f.x+f.width, f.y+f.height))
 
def main():
    image = cv.imread("E:/Documents/Dropbox/CMPT 456/Proj/faceRec/images/JianPei.0.jpg");
    detectObjects(image)
 
if __name__ == "__main__":
    main()
