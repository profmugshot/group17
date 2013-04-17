#!/usr/bin/python
import sys
import cv2.cv as cv
import cv2
from optparse import OptionParser

# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned
# for accurate yet slow object detection. For a faster operation on real video
# images the settings are:
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING,
# min_size=<minimum possible face size

min_size = (10, 10)
image_scale = 1
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0
# load harr cascades
cascade = cv.Load("haarcascade_frontalface_default.xml")
nested = cv.Load("haarcascade_eye.xml")

def detect_and_draw(img, cascade):
    # allocate temporary images
    gray = cv.CreateImage((img.width,img.height), 8, 1)
    small_img = cv.CreateImage((cv.Round(img.width / image_scale),
                   cv.Round (img.height / image_scale)), 8, 1)

    # convert color input image to grayscale
    cv.CvtColor(img, gray, cv.CV_BGR2GRAY)

    # scale input image for faster processing
    cv.Resize(gray, small_img, cv.CV_INTER_LINEAR)

    cv.EqualizeHist(small_img, small_img)

    if(cascade):
        t = cv.GetTickCount()
        faces = cv.HaarDetectObjects(small_img, cascade, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, min_size)
        t = cv.GetTickCount() - t
        print "detection time = %gms" % (t/(cv.GetTickFrequency()*1000.))
        print "foudn %s faces"%len(faces)
        print faces
        if faces:
            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                print x,y,w,h
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                cv.Rectangle(img, pt1, pt2, cv.RGB(255, 0, 0), 1, 8, 0)

                # Estimate the eyes position
                # First, set the image region of interest
                # The last division removes the lower part of the face to lower probability for false recognition
                cv.SetImageROI(img,
                (pt1[0],
                pt1[1],pt2[0]-pt1[0],
                int((pt2[1]-pt1[1])*0.6) ) )
                # Detect the eyes
                eyes = cv.HaarDetectObjects(img, nested, cv.CreateMemStorage(0),
                                     haar_scale, min_neighbors, haar_flags, (10,10))
                # If eyes were found
                if eyes:
                    # For each eye found
                    print "found %s eyes: %s"%(len(eyes),eyes)
                    for eye in eyes:
                        x,y,a,b=eye[0]
                        x+=pt1[0]
                        y+=pt1[1]
                        eyePos=([x+a/2,y+b/2])
                        print eyePos
                        # Draw a rectangle around the eye
                        cv.Rectangle(img,
                        (eye[0][0], eye[0][1]),
                        (eye[0][0]+eye[0][2], eye[0][1]+eye[0][3]),
                        cv.RGB(0, 255, 0), 1, 8, 0)
                cv.ResetImageROI(img)

    cv.ShowImage("result", img)

if __name__ == '__main__':
    input_name = '1'

    if len(sys.argv) == 2:
        input_name=sys.argv[1]
    else:
        print "No input given, fallback to camera"


    if input_name.isdigit():
        capture = cv.CreateCameraCapture(int(input_name))
    else:
        capture = None
    cv.NamedWindow("result", 1)

    if capture:
        frame_copy = None
        while True:
            frame = cv.QueryFrame(capture)
            if not frame:
                cv.WaitKey(0)
                break
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width,frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, frame_copy)
            else:
                cv.Flip(frame, frame_copy, 0)

            detect_and_draw(frame_copy, cascade)

            if cv.WaitKey(10) >= 0:
                break
    else:
        image = cv.LoadImage(input_name, 1)
        detect_and_draw(image, cascade)
        cv.WaitKey(0)

    cv.DestroyWindow("result")
