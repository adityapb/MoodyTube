#!/usr/bin/python

'''Image class has all methods used on training dataset'''

import cv2
import glob
import os
import sys
import numpy as np

class Image:
	
	def __init__(self, cascade = ''):
		self.CASCADE_PATH = cascade
		#self.IMG_PATH = img
		
	def identify(self, *args):
		'''For simplicity args has filenames'''
		Cascade = cv2.CascadeClassifier(self.CASCADE_PATH)
		#os.chdir(self.IMG_PATH)
		crop_img = []
		parameters = {}
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
				parameters[filename] = (x, y, w, h)
		return parameters
		
	def cropImg(self, *args):
		'''args has filenames'''
		crop_img = []
		for filename, (x, y, w, h) in self.identify(*args).items:
			crop_img.append(cv2.imread(str(filename))
		return crop_img
			
	def saveImg(self, PATH, *args):
		'''Here args are images and not filenames'''
		os.chdir(PATH)
		for i, image in enumerate(args):
			print "Saved {0} image".format(i)
			cv2.imwrite(str(i) + '.bmp' , image)
		return
		
	def cornerDetect(self, img, x, y, w, h):
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		gray = np.float32(gray)
		dst = cv2.cornerHarris(gray,2,3,0.04)
		#result is dilated for marking the corners, not important
		dst = cv2.dilate(dst,None)
		# Threshold for an optimal value, it may vary depending on the image.
		#if j,i lies in y:y+h , x:x+w; use those coordinates
		count = 0.
		for i in [x:x+w]:
			for j in [y:y+h]:
				if dst[i][j] > 0.5*dst.max():
					X += i
					Y += j
					count += 1
		return [X/count , Y/count]
		
	
	def rotateImage(self, image, angle):
  		image_center = tuple(np.array(image.shape)/2)
  		rot_mat = cv2.getRotationMatrix2D(image_center,angle,1.0)
  		result = cv2.warpAffine(image, rot_mat, image.shape,flags=cv2.INTER_LINEAR)
  		return result
	
	
	def alignEyes(self, *args):
		pass
	
	def alignImg(self, *args):
		'''Align eyes and mouth in all images
		First rotate the images to align the eyes
		Then change (x,y,w,h) to align all the eyes in the dataset to a fixed point'''
		pass

	def average(self, *args):
		'''Find average of all images in args'''
		pass
		

			
if __name__ == '__main__':
	if 'crop' in sys.argv:
		img = Image(str(os.getcwd()) + '/haarcascades/haarcascade_frontalface_alt.xml')
		BASE_IMG_PATH = str(sys.argv[2])
		images = []
		for filename in glob.glob(BASE_IMG_PATH + '/*.bmp'):
			images.append(filename)
		cropped = img.cropImg(*images)
		img.saveImg(str(os.getcwd()) + '/cropped', *cropped)
	
	if 'align' in sys.argv:
		
	
