import os
import sys
import cv2
import numpy as np

lables={}

if __name__ == "__main__":

    model = cv2.createLBPHFaceRecognizer()
    # Read
    # Learn the model. Remember our function returns Python lists,
    # so we use np.asarray to turn them into NumPy lists to make
    # the OpenCV wrapper happy:
    model.load("lbph.yml")
    #
    # model.predict is going to return the predicted label and
    # the associated confidence:
    pre=cv2.imread("img/JianPei/JianPei.0.jpg", cv2.IMREAD_GRAYSCALE)
    [p_label, p_confidence] = model.predict(pre)
    # Print it:
    print "Predicted label = %d (confidence=%.2f)" % (p_label, p_confidence)
    print "Predicted: %s; Actual: " % (p_label)
    # Cool! Finally we'll plot the Eigenfaces, because that's
    # what most people read in the papers are keen to see.
    #
    # Just like in C++ you have access to all model internal
    # data, because the cv::FaceRecognizer is a cv::Algorithm.
    #
    # You can see the available parameters with getParams():
