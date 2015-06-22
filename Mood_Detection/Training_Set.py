#!/usr/bin/python

'''
Faces will be detected such that the centre of the nose is at the centre of the face
Consider image alignment by eye detection using Shi-Tomasi corner detection algorithm

1. Align the image
2. Find the distance between the centre of the eyes and upper bound of the sample image
3. Resize the image so that the distance between the eyes is equal to that of the sample
4. The centre of the eyes should match the centre of the sample
'''


from Image import Image_X
from PreProcessing import PreProcessing
import cv2
import glob
import math
import sys
import os
import warnings
import numpy as np


class Training:

	def __init__(self, nose_cascade = None, face_cascade = None, eye_cascade = None, sample = None):
		#if nose_cascade or face_cascade is None: warnings.warn('Some of the cascades are still None')
		self.nose = Image_X(nose_cascade)
		self.face = Image_X(face_cascade)
		self.eye = Image_X(eye_cascade)
		val = self.GetDimensions(sample)
		self.dimensions = val['dimensions']
		self.dist = val['distance']

	def alignImage(self, PATH, image):
		try:
			for filename, image in self.eye.alignEyes(image).iteritems():
				self.save(PATH, **{filename : image})
				return image
		except:
			try:
				self.IdError(image)
			except:
				pass

	def GetDimensions(self, filename):
		img = cv2.imread(filename)
		val = self.GetCentre(filename)
		centre = val['centre']
		#return (up, down, left, right)
		try:
			return {'dimensions' : (img.shape[1] - centre[1], centre[1], centre[0], img.shape[0] - centre[0]),
					'distance' : val['dist']}
		except:
			return None

	def GetCentre(self, filename):
		img = cv2.imread(filename)
		eye = self.eye.ShiTomasiCornerDetect(filename)
		try:
			return {'centre' : ((eye[0][0]+eye[1][0])/2., eye[0][1]), 'dist' : abs(eye[0][0]-eye[1][0])}
		except:
			return None

	def IdError(self, image):
		'''Delete the image'''
		try:
			os.remove(image)
		except:
			pass

	def Resize(self, filename):
		try:
			dist = self.GetCentre(filename)['dist']
		except:
			self.IdError(filename)
			return
		scaleFactor = self.dist/float(dist)
		return cv2.resize(cv2.imread(filename), (0,0), fx = scaleFactor, fy = scaleFactor)

	def faceIdentify(self, image):
		for filename, list_of_parameters in self.face.identify(image).iteritems():
			if len(list_of_parameters) is not 1:
				#self.IdError(image)
				return None
			for (x, y, w, h) in list_of_parameters:
				return (w, h)

	def alignFace(self, image):
		'''
		x -> left
		y -> down
		w -> right + left
		h -> up + down
		'''
		#image = self.alignedImage(image)
		try:
			centre = self.GetCentre(image)['centre']
			dim = self.dimensions
		except:
			self.IdError(image)
		try:
			return (centre[0] - dim[2],
					centre[1] - dim[1],
					dim[2] + dim[3],
					dim[0] + dim[1])
		except:
			return None

	def crop(self, image):
		x = self.alignFace(image)
		try:
			return self.face.getImg(image)[x[1]:x[1]+x[3] , x[0]:x[0]+x[2]]
		except:
			self.IdError(image)
			return None

	def save(self, PATH, **kwargs):
		os.chdir(PATH)
		for filename, image in kwargs.iteritems():
			if image is not None:
				print "Saved {0} image".format(filename)
				cv2.imwrite(filename , image)
			else:
				print "Not saved {0}".format(filename)
		return

if __name__ == '__main__':
	BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
	t = Training(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	images = {}
	for filename in glob.glob(BASE_PATH + '/sad/*.JPG'):
		t.alignImage(BASE_PATH, filename)
	#t.save(BASE_PATH + '/cropped', *images)
	print "Done aligning..."
	for filename in glob.glob(BASE_PATH + '/sad/*.JPG'):
		image = t.Resize(filename)
		t.save(BASE_PATH, **{filename : image})
	for filename in glob.glob(BASE_PATH + '/sad/*.JPG'):
		image = t.crop(filename)
		images[filename] = image
		'''p = PreProcessing()
		image = p.gray(image)
		image = p.histogram_equalize(image)
		images[filename] = p.gamma_correction(0.5,image)'''
	t.save(BASE_PATH, **images)
