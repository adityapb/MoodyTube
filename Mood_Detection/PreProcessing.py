#!/usr/bin/python

import cv2
import numpy as np

def gamma_correction(correction, image):
	img = image/255.0
	img = cv2.pow(img, correction)
	return np.uint8(img*255)
	
def histogram_equalize(image):
	return cv2.equalizeHist(image)
	
def gray(image):
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	
def dog_filter(img):
	return cv2.GaussianBlur(img,img.shape,0)
		
