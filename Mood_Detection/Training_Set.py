#!/usr/bin/python

'''Faces will be detected such that the centre of the nose is at the centre of the face
WITHOUT ALIGNING IMAGES by eye detection'''

from Image import Image
import cv2
import numpy as np


class Training():
	
	def __init__(self, nose_cascade = None, face_cascade = None):
		self.nose = Image(nose_cascade)
		self.face = Image(face_cascade)
		
	def nose_center(self, image):
		for filename, list_of_parameters in self.nose.identify(image):
			if len(parameters != 1): raise Exception('Identification error')
			for (x, y, w, h) in list_of_parameters:
				return (x + w/2. , y + h/2.)
				
	def faceIdentify(self, image):
		for filename, list_of_parameters in self.face.identify(image):
			if len(parameters != 1): raise Exception('Identification error')
			for (x, y, w, h) in list_of_parameters:
				return (w, h)
				
	def alignFace(self, image):
		'''(nose_x, nose_y) = self.nose_center(image)
		(height, length) = self.faceIdentify(image)'''
		center = self.nose_center(image)
		dimensions = self.faceIdentify(image)
		return (center[0] - dimensions[0]/2.,
				center[1] - dimensions[1]/2., 
				center[0] + dimensions[0]/2., 
				center[1] + dimensions[1]/2.)
				
	def crop(self, image):
		for (x, y, w, h) in alignFace(image):
			return self.face.getImg(image)[y:y+h , x:x+w]
