from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

# Utitlity class for analysing and manipulating frames
# Used in order to find the center and radius of balls in a given frame

class FrameAnalyser:
    # Resize the frame, blur it, and convert it to the HSV color space
    @staticmethod
	def __prepare_frame(frame):
		frame = imutils.resize(frame, width=600)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

		return hsv

	# Construct a mask for the color, then perform a series of dilations 
	# and erosions to remove any small blobs left in the mask
    @staticmethod
	def __construct_mask(hsv_frame):
		mask = cv2.inRange(hsv_frame, lower_color, upper_color)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		return mask

	# Find contours in the mask and initialize the current (x, y) center of the ball
    @staticmethod
	def __find_contours(mask):
		countours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		countours = imutils.grab_contours(countours)
		return countours

    @staticmethod
	def __find_centers(contours):
		centers = []
		for c in contours:
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			centers.append(center)
		return centers

    @staticmethod
    def find_balls(frame):
        hsv = FrameAnalyser.__prepare_frame(frame)
        mask = FrameAnalyser.__construct_mask(hsv)
        contours = FrameAnalyser.__find_contours(mask)
        centers = FrameAnalyser.__find_centers(contours)
        return centers