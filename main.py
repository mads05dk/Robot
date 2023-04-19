from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

from Course import Course
from OpenCV.BallTracker import BallTracker, bballTracker

# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video", help="path to the (optional) video file")
#ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
#args = vars(ap.parse_args())

course = Course()
#ballTracker(course)
#LOWER = (0, 0, 150)
#UPPER = (180, 255, 255)
# DTU BALLS
LOWER = (0, 0, 221)
UPPER = (155, 82, 255)
ballTracker = BallTracker(course, LOWER, UPPER)
ballTracker.loop()
#bballTracker(course)