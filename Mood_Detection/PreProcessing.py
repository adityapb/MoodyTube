#!/usr/bin/python

import cv2
import numpy as np

class PreProcessing:
	
	def __init__(self):
		pass
		
	def gamma_correction(self, correction, image):
		img = image/255.0
		img = cv2.pow(img, correction)
		return np.uint8(img*255)
		
	def histogram_equalize(self, image):
		return cv2.equalizeHist(image)
		
	def gray(self, image):
		return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
