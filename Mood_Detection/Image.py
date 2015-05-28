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
		'''args has images'''
		Cascade = cv2.CascadeClassifier(self.CASCADE_PATH)
		#os.chdir(self.IMG_PATH)
		crop_img = []
		parameters = {}
		for image in args:
			#image = cv2.imread(str(filename))
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
				if image not in parameters: parameters[image] = [(x, y, w, h)]
				else: parameters[image].append((x, y, w, h))
		return parameters
		
	def cropImg(self, *args):
		'''args has images'''
		crop_img = []
		for image, (x, y, w, h) in self.identify(*args).items:
			crop_img.append(image[y:y+h , x:x+w])
		return crop_img
			
	def saveImg(self, PATH, *args):
		os.chdir(PATH)
		for i, image in enumerate(args):
			print "Saved {0} image".format(i)
			cv2.imwrite(str(i) + '.bmp' , image)
		return
		
	def cornerDetect(self, img):
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		gray = np.float32(gray)
		dst = cv2.cornerHarris(gray,2,3,0.04)
		#(x, y, w, h) = identify(img)
		#result is dilated for marking the corners, not important
		dst = cv2.dilate(dst,None)
		# Threshold for an optimal value, it may vary depending on the image.
		#if j,i lies in y:y+h , x:x+w; use those coordinates
		corners= []
		for (x, y, w, h) in identify(img):
			count = 0.
			for i in range(x,x+w):
				for j in range(y,y+h):
					if dst[i][j] > 0.5*dst.max():
						X += i
						Y += j
						count += 1
			corners.append([X/count , Y/count])
		return corners
		
	
	def rotateImage(self, image, angle):
  		image_center = tuple(np.array(image.shape)/2)
  		rot_mat = cv2.getRotationMatrix2D((image_center[0], image_center[1]),angle,1.0)
  		result = cv2.warpAffine(image, rot_mat, (image.shape[0], image.shape[1]),flags=cv2.INTER_LINEAR)
  		cv2.resize(result, tuple(reversed(image.shape[:2])))
  		return result
	
	
	def alignEyes(self, *args):
		'''args has images'''
		
	
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
			images.append(cv2.imread(filename))
		cropped = img.cropImg(*images)
		img.saveImg(str(os.getcwd()) + '/cropped', *cropped)
		
	if 'rotate' in sys.argv:
		x = Image()
		img = x.rotateImage(cv2.imread(str(os.getcwd()) + '/male/EMBmale20happy.bmp'), 90)
		cv2.imshow('rotated', img)
		cv2.waitKey(0)
	
	if 'align' in sys.argv:
		pass
	
