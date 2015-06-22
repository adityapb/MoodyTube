#!/usr/bin/python

'''Image_X class has all methods used on training dataset'''

import cv2
import glob
import os
import sys
import numpy as np
import math
from PIL import Image
from matplotlib import pyplot as plt

class Image_X:

	def __init__(self, cascade = None):
		self.CASCADE_PATH = cascade
		#self.IMG_PATH = img

	def getImg(self, filename):
		return cv2.imread(filename)

	def identify(self, *args):
		Cascade = cv2.CascadeClassifier(self.CASCADE_PATH)
		#os.chdir(self.IMG_PATH)
		parameters = {}
		for i, filename in enumerate(args):
			#image = cv2.imread(str(filename))
			image = self.getImg(filename)
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
				if filename not in parameters: parameters[filename] = [(x, y, w, h)]
				else: parameters[filename].append((x, y, w, h))
		#print len(parameters)
		return parameters

	def cropImg(self, *args):
		crop_img = []
		for filename, list_of_parameters in self.identify(*args).iteritems():
			for (x, y, w, h) in list_of_parameters:
				crop_img.append(self.getImg(filename)[y:y+h , x:x+w])
		return crop_img

	def saveImg(self, PATH, *args):
		os.chdir(PATH)
		for i, image in enumerate(args):
			print "Saved {0} image".format(i)
			cv2.imwrite(str(i) + '.bmp' , image)
		return

	def ShiTomasiCornerDetect(self, filename):
		img = self.getImg(filename)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		result = []
		for filename, list_of_parameters in self.identify(filename).iteritems():
			if len(list_of_parameters) is not 2: return None
			for (x, y, w, h) in list_of_parameters:
				corners = cv2.goodFeaturesToTrack(gray[y:y+h , x:x+w],1,0.01,10)
				corners = np.int0(corners)
				for i in corners:
					u,v = i.ravel()
					result.append((u+x, v+y))
		return result

	def testCornerDetect(self, filename):
		img = self.getImg(filename)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		result = []
		for filename, list_of_parameters in self.identify(filename).iteritems():
			for (x, y, w, h) in list_of_parameters:
				corners = cv2.goodFeaturesToTrack(gray[y:y+h , x:x+w],1,0.01,10)
				corners = np.int0(corners)
				for i in corners:
					u,v = i.ravel()
					cv2.circle(img,(u+x,v+y),3,255,-1)
		plt.imshow(img),plt.show()
		return

	def testAlignment(self, filename):
		corners = self.ShiTomasiCornerDetect(filename)
		tangent = (corners[0][1] - corners[1][1])/float(corners[0][0] - corners[1][0])
		angle = math.degrees(math.atan(tangent))
		plt.imshow(self.rotateImage(self.getImg(filename), angle)),plt.show()
		return


	def rotateImage(self, image, angle):
  		image = Image.fromarray(cv2.cvtColor(image,cv2.COLOR_BGR2GRAY))
		return np.array(image.rotate(angle))

	def alignEyes(self, *args):
		'''args has images'''
		aligned = {}
		for filename in args:
			image = self.getImg(filename)
			corners = self.ShiTomasiCornerDetect(filename)
			if corners is None:
				os.remove(filename)
				return None
			if len(corners) is 2:
				if (corners[0][0] - corners[1][0]) is not 0:
					tangent = (corners[0][1] - corners[1][1])/float(corners[0][0] - corners[1][0])
					angle = math.degrees(math.atan(tangent))
					aligned[filename] = self.rotateImage(image, angle)
			else: return None
		return aligned


if __name__ == '__main__':

	if 'test' in sys.argv:
		eye = Image_X(str(os.getcwd()) + '/haarcascades/haarcascade_eye.xml')
		eye.testCornerDetect(str(os.getcwd()) + '/1.jpg')

	if 'testalign' in sys.argv:
		eye = Image_X(str(os.getcwd()) + '/haarcascades/haarcascade_eye.xml')
		eye.testAlignment(str(os.getcwd()) + '/1.jpg')
