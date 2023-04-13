from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

class BallTracker:
	def __init__(self, course, lower_color, upper_color):
		self.course = course
		self.lower_color = lower_color
		self.upper_color = upper_color
		self.points = []
		self.vs = cv2.VideoCapture("D:/Development/alturing/Robot/OpenCV/balls.mp4")
		self.AMOUNT_OF_FRAMES = self.vs.get(cv2.CAP_PROP_FRAME_COUNT)
		print(self.AMOUNT_OF_FRAMES)
		# allow the camera or video file to warm up
		time.sleep(2.0)

	# Resize the frame, blur it, and convert it to the HSV color space
	def __prepare_frame(self, frame):
		frame = imutils.resize(frame, width=600)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

		return hsv

	# Construct a mask for the color, then perform a series of dilations 
	# and erosions to remove any small blobs left in the mask
	def __construct_mask(self, hsv_frame):
		mask = cv2.inRange(hsv_frame, self.lower_color, self.upper_color)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)
		return mask

	# Find contours in the mask and initialize the current (x, y) center of the ball
	def __find_contours(self, mask):
		countours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		countours = imutils.grab_contours(countours)
		return countours

	# Find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
	def __find_center(self, contours):
		center = None
		if len(contours) > 0:
			c = max(contours, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		else:
			print("No contours")
		return center

	def __find_centers(self, contours):
		centers = []
		for c in contours:
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			centers.append(center)
		return centers

	def __set_frame(self, frame_number):
		self.vs.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)

	def __get_frame(self):
		return self.vs.get(cv2.CAP_PROP_POS_FRAMES)

	def __print_balls(self):
		print("There are " + str(len(self.points)) + " balls in the video. They are at:")
		for i in range(len(self.points)):
			x, y = self.points[i - 1]
			print("Ball " + str(i) + "(" + str(x) + ", " + str(y) + ")")

	def loop(self):
		self.__set_frame(10)
		while True:
			# grab the current frame
			ret, frame = self.vs.read()
			# handle the frame from VideoCapture or VideoStream
			#frame = frame[1] if args.get("video", False) else frame
			if ret is None: # end of video
				self.vs.set(cv2.CAP_PROP_POS_FRAMES, 10)

			
			if (frame is None):
				print("No frame")
				self.__set_frame(10)
				continue
			hsv = self.__prepare_frame(frame)
			mask = self.__construct_mask(hsv)
			contours = self.__find_contours(mask)
			#center = self.__find_center(contours)
			centers = self.__find_centers(contours)
			self.points = centers
			#self.points.append(center)

			cv2.imshow("Frame", frame) # show the frame to our screen
			cv2.imshow("Mask", mask) # show the mask to our screen

			key = cv2.waitKey(1) & 0xFF
			if key == ord("q"):
				break
			elif key == ord("p"):
				self.__print_balls()
				time.sleep(2)
			


	
	

def bballTracker(course):
	# define the lower and upper boundaries of the balls color in the HSV color space
	greenLower = (0, 0, 255)
	greenUpper = (180, 255, 255)

	# initialize the list of tracked points
	#pts = deque(maxlen=args["buffer"])
	pts = deque(maxlen = 64)

	# if a video path was not supplied, grab the reference to the webcam otherwise, grab a reference to the video file
	#if not args.get("video", False):
		#vs = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	#else:
		#vs = cv2.VideoCapture(args["video"])

	vs = cv2.VideoCapture("D:/Development/alturing/Robot/OpenCV/balls.mp4")

	# allow the camera or video file to warm up
	time.sleep(2.0)

	while True:
		# grab the current frame
		ret, frame = vs.read()
		# handle the frame from VideoCapture or VideoStream
		#frame = frame[1] if args.get("video", False) else frame
		if ret is None: # end of video
			vs.set(cv2.CAP_PROP_POS_FRAMES, 0)
			#break

		# resize the frame, blur it, and convert it to the HSV color space
		try:
			frame = imutils.resize(frame, width=600)
			blurred = cv2.GaussianBlur(frame, (11, 11), 0)
			hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
		except:
			vs.set(cv2.CAP_PROP_POS_FRAMES, 0)

		# construct a mask for the color "green", then perform a series of dilations and erosions to remove any small blobs left in the mask
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)

		# find contours in the mask and initialize the current (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		center = None
		
		if len(cnts) > 0: # only proceed if at least one contour was found
			# find the largest contour in the mask, then use it to compute the minimum enclosing circle and centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			
			#print(radius)
			#if radius > 1: # only proceed if the radius meets a minimum size
				# draw the circle and centroid on the frame, then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), 10, (0, 255, 255), 10)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
		
		# update the points queue
		pts.appendleft(center)
		
		# loop over the set of tracked points
		for i in range(1, len(pts)):
			# if either of the tracked points are None, ignore them 
			if pts[i - 1] is None or pts[i] is None:
				continue
			
			# otherwise, compute the thickness of the line and draw the connecting lines
			thickness = int(np.sqrt(64 / float(i + 1)) * 2.5)
			cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
		
		# show the frame to our screen
		try:
			cv2.imshow("Frame", frame) 
		except:
			vs.set(cv2.CAP_PROP_POS_FRAMES, 0)
		if (center is not None):
			x, y = center
			if (course.ball_seen_at(x, y)):
				course.print_balls()

		# if the 'q' key is pressed, stop the loop
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
	# if we are not using a video file, stop the camera video stream otherwise, release the camera
	vs.stop()

	# close all windows
	cv2.destroyAllWindows()