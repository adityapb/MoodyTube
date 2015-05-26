#!/usr/bin/python

'''Image class has all methods used on training dataset'''

import cv2
import glob
import os
import sys

class Image:
	
	def __init__(self, cascade = ''):
		self.CASCADE_PATH = cascade
		#self.IMG_PATH = img
		
	def cropImg(self, *args):
		Cascade = cv2.CascadeClassifier(self.CASCADE_PATH)
		#os.chdir(self.IMG_PATH)
		crop_img = []
		for filename in args:
			image = cv2.imread(str(filename))
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			objects = Cascade.detectMultiScale(
			    gray,
			    scaleFactor=1.1,
			    minNeighbors=5,
			    minSize=(30, 30),
			    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
			)
			print "Found {0} objects!".format(len(objects))
			for (x, y, w, h) in objects:
				crop_img.append(image[y:y+h , x:x+w])
		return crop_img
			
	def saveImg(self, PATH, *args):
		os.chdir(PATH)
		for i, image in enumerate(args):
			print "Saved {0} image".format(i)
			cv2.imwrite(str(i) + '.bmp' , image)
		return

	def alignImg(self, *args):
		'''Align eyes and mouth in all images'''
		pass

	def average(self, *args):
		'''Find average of all images in args'''
		pass

			
if __name__ == '__main__':
	img = Image(str(os.getcwd()) + '/haarcascades/haarcascade_frontalface_alt.xml')
	BASE_IMG_PATH = str(sys.argv[1])
	images = []
	for filename in glob.glob(BASE_IMG_PATH + '/*.bmp'):
		images.append(filename)
	cropped = img.cropImg(*images)
	img.saveImg(str(os.getcwd()) + '/cropped', *cropped)
	
