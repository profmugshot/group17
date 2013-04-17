# -*- coding: cp936 -*-
import cv, Image
import sys,os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
import faceRec_lbph as rec
import faceRec_init as fi

min_size = (10,10)
image_scale = 1
haar_scale = 1.2
min_neighbors = 2
haar_flags = 0

# return eyePos[right,left]
def prepare_rec(filename):
    faceCascade = cv.Load("haarcascade_frontalface_alt.xml")
    eyeCascade = cv.Load("haarcascade_eye.xml")
    image = cv.LoadImage(filename)
    # Allocate the temporary images
    gray = cv.CreateImage((image.width, image.height), 8, 1)
    smallImage = cv.CreateImage((cv.Round(image.width / image_scale),
    cv.Round (image.height / image_scale)), 8 ,1)

    # Convert color input image to grayscale
    cv.CvtColor(image, gray, cv.CV_BGR2GRAY)
    # Scale input image for faster processing
    cv.Resize(gray, smallImage, cv.CV_INTER_LINEAR)
    # Equalize the histogram
    cv.EqualizeHist(smallImage, smallImage)
    # Detect the faces
    faces = cv.HaarDetectObjects(smallImage, faceCascade, cv.CreateMemStorage(0),
    haar_scale, min_neighbors, haar_flags, min_size)
    # If faces are found
    if faces:
        stuff={'eyePos':[],'facepos':faces}
        eyePos=[]
        save_file=filename
        for ((x, y, w, h), n) in faces:
            # the input to cv.HaarDetectObjects was resized, so scale the
            # bounding box of each face and convert it to two CvPoints
            pt1 = (int(x * image_scale), int(y * image_scale))
            pt2 = (int((x+w) * image_scale), int((y+h) * image_scale))
            # Estimate the eyes position
            # First, set the image region of interest
            # The last division removes the lower part of the face to lower probability for false recognition
            cv.SetImageROI(image, (pt1[0],
                    pt1[1],
                    pt2[0]-pt1[0],
                    int((pt2[1]-pt1[1]) * 0.6)))
            # print pt1,pt2
            # Detect the eyes
            eyes = cv.HaarDetectObjects(image, eyeCascade,
                    cv.CreateMemStorage(0),
                    haar_scale, min_neighbors,
                    haar_flags, (20,15))
            # If eyes were found
            if eyes:
                # For each eye found
                for eye in eyes:
                    x,y,a,b=eye[0]
                    x+=pt1[0]
                    y+=pt1[1]
                    eyePos.append([x+a/2,y+b/2])
            if len(eyePos)>1:
                eyePos.sort(key=lambda tup:tup[0])
                im = Image.open(filename)
                fi.CropFace(im, eyePos[0], eyePos[1], offset_pct=(0.25,0.25)).save(save_file)
            else:
                cv.ResetImageROI(image)
                cv.SetImageROI(image, (pt1[0],pt1[1],pt2[0]-pt1[0],(pt2[1]-pt1[1])))
                cv.SaveImage(save_file,image)

            # Finally, reset the image region of interest (otherwise this won’t
            # be drawn correctly
            cv.ResetImageROI(image)

        result = rec.rePath(save_file)
        # return image
        return result

if __name__ == "__main__":
    img="test.jpg"
    if len(sys.argv) == 2:
        img=sys.argv[1]
    detectEye(img)