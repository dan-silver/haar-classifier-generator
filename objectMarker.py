#!/usr/bin/python
 
###############################################################################
# Name		: ObjectMarker.py
# Author	: Python implementation: sqshemet 
# 	 	  Original ObjectMarker.cpp: http://www.cs.utah.edu/~turcsans/DUC_files/HaarTraining/
# Date		: 7/24/12
# Description	: Object marker utility to be used with OpenCV Haar training. 
#		  Tested on Ubuntu Linux 10.04 with OpenCV 2.1.0.
# Usage		: python ObjectMarker.py outputfile inputdirectory
###############################################################################
 
import cv
import sys
import os
 
IMG_SIZE = (300,300)
IMG_CHAN = 3
IMG_DEPTH = cv.IPL_DEPTH_8U
image = cv.CreateImage(IMG_SIZE, IMG_DEPTH, IMG_CHAN)
image2 = cv.CreateImage(IMG_SIZE, IMG_DEPTH, IMG_CHAN) 
roi_x0 = 0
roi_y0 = 0
roi_x1 = 0
roi_y1 = 0
num_of_rec = 0
start_draw = False
window_name = "<Space> to save and load next, <X> to skip, <ESC> to exit."
 
def on_mouse(event, x, y, flag, params):
	global start_draw
	global roi_x0
	global roi_y0
	global roi_x1
	global roi_y1
	if (event == cv.CV_EVENT_LBUTTONDOWN):
		if (not start_draw):
			roi_x0 = x
			roi_y0 = y
			start_draw = True
		else:
			roi_x1 = x
			roi_y1 = y
			start_draw = False
	elif (event == cv.CV_EVENT_MOUSEMOVE and start_draw):
		#Redraw ROI selection
		image2 = cv.CloneImage(image)
		cv.Rectangle(image2, (roi_x0, roi_y0), (x,y), 
			cv.CV_RGB(255,0,255),1)
		cv.ShowImage(window_name, image2)
 
def main():
 
	global image
	iKey = 0
	
	if (len(sys.argv) != 3):
		sys.stderr.write("%s output_info.txt raw/data/directory\n" 
			% sys.argv[0])
		return -1
 
	input_directory = os.path.join(os.getcwd(), sys.argv[2])
	output_file = os.path.join(os.getcwd(), sys.argv[1])
 
	#Get a file listing of all files within the input directory
	try:
		files = os.listdir(input_directory)
	except OSError:
		sys.stderr.write("Failed to open dirctory %s\n" 
			% input_directory)
		return -1
 
	files.sort()
 
	sys.stderr.write("ObjectMarker: Input Directory: %s Output File %s\n" 
			% (input_directory, output_file))
 
	# init GUI
	cv.NamedWindow(window_name, 1)
	cv.SetMouseCallback(window_name, on_mouse, None)
 
	sys.stderr.write("Opening directory...")
	# init output of rectangles to the info file
	os.chdir(input_directory)
	sys.stderr.write("done.\n")
 
	str_prefix = input_directory
 
	try:
		output = open(output_file, "r+")
	except IOError:
		sys.stderr.write("Failed to open file %s.\n" % output_file)
		return -1
 
	for file in files:
		str_postfix = ""
		num_of_rec = 0
		img = str_prefix + file
		sys.stderr.write("Loading image %s...\n" % img)
 
		try: 
			image = cv.LoadImage(img, 1)
		except IOError: 
			sys.stderr.write("Failed to load image %s.\n" % img)
			return -1
 
		#  Work on current image
		cv.ShowImage(window_name, image)
		# Need to figure out waitkey returns.
		# <ESC> = 43		exit program
		# <Space> = 32		add rectangle to current image
		# <x> = 136		skip image
		iKey = cv.WaitKey(0) % 255
		sys.stderr.write("wait key is %d" % iKey)
		# This is ugly, but is actually a simplification of the C++.
		if iKey == 43:
			cv.DestroyWindow(window_name)
			return 0
		elif iKey == 32:
			num_of_rec += 1
			# Currently two draw directions possible:
			# from top left to bottom right or vice versa
			if (roi_x0<roi_x1 and roi_y0<roi_y1):
				str_postfix += " %d %d %d %d\n" % (roi_x0,
					roi_y0, (roi_x1-roi_x0), (roi_y1-roi_y0))
			elif (roi_x0>roi_x1 and roi_y0>roi_y1):
				str_postfix += " %d %d %d %d\n" % (roi_x1, 
					roi_y1, (roi_x0-roi_x1), (roi_y0-roi_y1))
			output.write(img + " " + str(num_of_rec) + str_postfix)
			# output.write("rect.\n")
		elif iKey == 136:
			sys.stderr.write("Skipped %s.\n" % img)
	# output.write("done\n")
	output.close()
if __name__ == '__main__':
	main()