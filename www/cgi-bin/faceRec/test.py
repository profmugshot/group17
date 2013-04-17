import os
import sys
import cv2
import cv
import numpy as np
import fnmatch

FACE_PATH = "P:\WORK\_faces"
HAAR_CASCADE_PATH = "P:\WORK\Packages-Python\OpenCV\data\haarcascades\haarcascade_frontalface_default.xml"

def initFace(path):
    faces = []
    # detected = cv.HaarDetectObjects(image, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
    arr_face = [f for f in listdir("C:\Intel\Logs") if fnmatch.fnmatch(f, "log")]

    return

CAMERA_INDEX = 0

def detect_faces(image):
    faces = []
    detected = cv.HaarDetectObjects(image, cascade, storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
    if detected:
        for (x,y,w,h),n in detected:
            faces.append((x,y,w,h))
    return faces

if __name__ == "__main__":
    cv.NamedWindow("Video", cv.CV_WINDOW_AUTOSIZE)

    capture = cv.CaptureFromCAM(CAMERA_INDEX)
    storage = cv.CreateMemStorage()
    cascade = cv.Load(HAAR_CASCADE_PATH)
    faces = []

    i = 0
    c = -1
    while (c == -1):
        image = cv.QueryFrame(capture)

        # Only run the Detection algorithm every 5 frames to improve performance
        if i%5==0:
            faces = detect_faces(image)

        for (x,y,w,h) in faces:
            cv.Rectangle(image, (x,y), (x+w,y+h), 255)

        cv.ShowImage("Video", image)
        i += 1
        c = cv.WaitKey(10)
