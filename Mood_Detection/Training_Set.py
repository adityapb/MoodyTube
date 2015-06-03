#!/usr/bin/python

'''Faces will be detected such that the centre of the nose is at the centre of the face
Consider image alignment by eye detection using Shi-Tomasi corner detection algorithm'''


from Image import Image
import cv2
import glob
import math
import sys
import os
import warnings
import numpy as np


class Training:
	
	def __init__(self, nose_cascade = None, face_cascade = None, eye_cascade = None):
		#if nose_cascade or face_cascade is None: warnings.warn('Some of the cascades are still None')
		self.nose = Image(nose_cascade)
		self.face = Image(face_cascade)
		self.eye = Image(eye_cascade)
		
	def alignImage(self, PATH, image):
		for filename, image in self.eye.alignEyes(image).iteritems():
			self.save(PATH, **{filename : image})
			return image
		
	def IdError(self, image):
		'''Use primitive way of saving the image'''
		#image = self.alignedImage(image)
		for filename, list_of_parameters in self.face.identify(image).iteritems():
			if len(list_of_parameters) is not 1: raise Exception('Identification error for face')
			for (x, y, w, h) in list_of_parameters:
				return cv2.imread(image)[y:y+h , x:x+w]
		
	def nose_center(self, image):
		for filename, list_of_parameters in self.nose.identify(image).iteritems():
			if len(list_of_parameters) is not 1:
				#self.IdError(image)
				return None
			for (x, y, w, h) in list_of_parameters:
				return (x + (w/2.) , y + (h/2.))
				
	def faceIdentify(self, image):
		for filename, list_of_parameters in self.face.identify(image).iteritems():
			if len(list_of_parameters) is not 1:
				#self.IdError(image)
				return None
			for (x, y, w, h) in list_of_parameters:
				return (w, h)
				
	def alignFace(self, image):
		'''(nose_x, nose_y) = self.nose_center(image)
		(height, length) = self.faceIdentify(image)'''
		#image = self.alignedImage(image)
		center = self.nose_center(image)
		dimensions = self.faceIdentify(image)
		try:
			return (center[0] - (dimensions[0]/2.),
					center[1] - (dimensions[1]/2.), 
					dimensions[0], 
					dimensions[1])
		except:
			return None
				
	def crop(self, image):
		x = self.alignFace(image)
		try:
			return self.face.getImg(image)[x[1]:x[1]+x[3] , x[0]:x[0]+x[2]]
		except:
			return self.IdError(image)
		
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
	t = Training(sys.argv[1], sys.argv[2], sys.argv[3])
	images = {}
	for filename in glob.glob(BASE_PATH + '/male/*.bmp'):
		t.alignImage(BASE_PATH, filename)
	#t.save(BASE_PATH + '/cropped', *images)
	
	for filename in glob.glob(BASE_PATH + '/male/*.bmp'):
		images[filename] = t.crop(filename)
	t.save(BASE_PATH, **images)
	
