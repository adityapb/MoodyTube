#!/usr/bin/python

'''Faces will be detected such that the centre of the nose is at the centre of the face
WITHOUT ALIGNING IMAGES by eye detection'''

from Image import Image
import cv2
import glob
import math
import sys
import os
import warnings
import numpy as np


class Training:
	
	def __init__(self, nose_cascade = None, face_cascade = None):
		#if nose_cascade or face_cascade is None: warnings.warn('One of the cascades is still None')
		self.nose = Image(nose_cascade)
		self.face = Image(face_cascade)
		
	def IdError(self, image):
		pass
		
	def nose_center(self, image):
		for filename, list_of_parameters in self.nose.identify(image).iteritems():
			if len(list_of_parameters) != 1:
				self.IdError(image)
				return None
			for (x, y, w, h) in list_of_parameters:
				return (x + (w/2.) , y + (h/2.))
				
	def faceIdentify(self, image):
		for filename, list_of_parameters in self.face.identify(image).iteritems():
			if len(list_of_parameters) != 1:
				self.IdError(image)
				return None
			for (x, y, w, h) in list_of_parameters:
				return (w, h)
				
	def alignFace(self, image):
		'''(nose_x, nose_y) = self.nose_center(image)
		(height, length) = self.faceIdentify(image)'''
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
			return None
		
	def save(self, PATH, *args):
		os.chdir(PATH)
		for i, image in enumerate(args):
			try:
				print "Saved {0} image".format(i)
				cv2.imwrite(str(i) + '.bmp' , image)
			except:
				print "Not saved {0}".format(i)
		return
			
if __name__ == '__main__':
	BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
	t = Training(sys.argv[1], sys.argv[2])
	images = []
	for filename in glob.glob(BASE_PATH + '/male/*.bmp'):
		images.append(t.crop(filename))
	t.save(BASE_PATH + '/cropped', *images)
	
