#!/usr/bin/python

from Image import Image_X
from eigenfaces import PCA
from classifier import Predictor
import glob
import cv2
import sys
import numpy as np
import math
import cPickle as pickle
import PreProcessing as pr
from matplotlib import pyplot as plt

class Mood_Detect():
	
	def __init__(self, nose_cascade = None, face_cascade = None, eye_cascade = None, sample = None, data_dir = None):
		self.nose = Image_X(nose_cascade)
		self.face = Image_X(face_cascade)
		self.eye = Image_X(eye_cascade)
		self.nose_casc = nose_cascade
		self.face_casc = face_cascade
		self.eye_casc = eye_cascade
		val = self.GetDimensions(cv2.imread(sample))
		self.dimensions = val['dimensions']
		self.dist = val['distance']
		self.dir = data_dir
		
	def GetImages(self, port):
		'''
		When two eyes and face are detected, capture the image
		'''
		cam_port = port
		cam = cv2.VideoCapture(port)
		images = []
		while True:
			if len(images) is 20:
				del(cam)
				return images
			ret, image = cam.read()
			face = self.identify(self.face_casc, image)
			if len(face) is 1:
				for x in face:
					if len(self.identify(self.eye_casc, image[x[1]:x[1]+x[3], x[0]:x[0]+x[2]])) is 2:
						images.append(self.process(self.crop(image)))
						
	def GetRealtimeInput(self,port):
		cam = cv2.VideoCapture(port)
		while True:
			ret, image = cam.read()
			face = self.identify(self.face_casc, image)
			if len(face) is 1:
				for x in face:
					if len(self.identify(self.eye_casc, image[x[1]:x[1]+x[3], x[0]:x[0]+x[2]])) is 2:
						return self.process(self.crop(image))
						
	def process(self, image):
		image = pr.gamma_correction(0.2,image)
		image = pr.dog_filter(image)
		image = pr.histogram_equalize(image)
		return image
						
	def GetDimensions(self, img):
		val = self.GetCentre(img)
		centre = val['centre']
		#return (up, down, left, right)
		try:
			return {'dimensions' : (img.shape[1] - centre[1], centre[1], centre[0], img.shape[0] - centre[0]),
					'distance' : val['dist']}
		except:
			return None

	def GetCentre(self, img):
		#print img
		eye = self.GetEyes_haar(img)
		return {'centre' : ((eye[0][0]+eye[1][0])/2., eye[0][1]), 'dist' : abs(eye[0][0]-eye[1][0])}
		
	def IdError(self, img):
		face = self.identify(self.face_casc, img)
		if len(face) is not 1: raise Exception('Error in detection')
		for (x, y, w, h) in face:
			return img[y:y+h , x:x+w]
		
	def identify(self, cascade, image):
		Cascade = cv2.CascadeClassifier(cascade)
		try:
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		except:
			gray = image
		result = []
		objects = Cascade.detectMultiScale(
		    gray,
		    scaleFactor=1.1,
		    minNeighbors=5,
		    minSize=(30, 30),
		    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
		)
		print "Found {0} objects!".format(len(objects))
		for parameters in objects:
			result.append(parameters)
		return result
		
	def GetAngle(self, corners):
		tangent = (corners[0][1] - corners[1][1])/float(corners[0][0] - corners[1][0])
		angle = math.degrees(math.atan(tangent))
		return angle
		
	def Resize(self, img):
		#print img
		dist = self.GetCentre(img)['dist']
		print dist
		scaleFactor = self.dist/float(dist)
		print scaleFactor
		return cv2.resize(img, (0,0), fx = scaleFactor, fy = scaleFactor)
		
	def GetEyes(self, img):
		'''Use Shi-Tomasi corner detection'''
		try:
			gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		except:
			gray = img
		result = []
		eyes = self.identify(self.eye_casc, img)
		if len(eyes) is 2:
			for (x, y, w, h) in eyes:
				corners = cv2.goodFeaturesToTrack(gray[y:y+h , x:x+w],1,0.01,10)
				corners = np.int0(corners)
				for i in corners:
					u,v = i.ravel()
					result.append((u+x, v+y))
		return result
		
	def GetEyes_haar(self, img):
		#print img
		try:
			gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		except:
			gray = img
		result = []
		for (x, y, w, h) in self.identify(self.eye_casc, img):
			result.append((x+w/2.,y+h/2.))
		return result
		
	def AlignEyes(self, img):
		return self.eye.rotateImage(img, self.GetAngle(self.GetEyes_haar(img)))
			
	def alignFace(self, img):
		'''
		x -> left
		y -> down
		w -> right + left
		h -> up + down
		'''
		image = self.Resize(self.AlignEyes(img))
		#print image
		centre = self.GetCentre(image)['centre']
		dim = self.dimensions
		try:
			return image,  (centre[0] - dim[2],
							centre[1] - dim[1],
							dim[2] + dim[3],
							dim[0] + dim[1])
		except:
			return image, None

	def crop(self, image):
		image, x = self.alignFace(image)
		return image[x[1]:x[1]+x[3] , x[0]:x[0]+x[2]]
			
	'''def detect(self,img,face_no):
		p = PCA()
		p.findmood(img,face_no,)'''
		
	def detect(self,num,classifier):
		p = PCA()
		imagename = self.GetRealtimeInput(0)
		cv2.imshow('you', imagename)
		cv2.waitKey(0)
		cv2.imwrite('test.bmp',imagename)
		facenum = num
		avgvals = pickle.load(open(self.dir+'/average.db','r'))
		eigenfaces = pickle.load(open(self.dir+'/eigenfaces.db','r'))
		weights = p.inputWeight(imagename,facenum,avgvals,eigenfaces)
		s = Predictor(classifier)
		return s.predict(weights)
			
if __name__ == '__main__':
	m = Mood_Detect(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
	print m.detect(14,'classifier.db')
		
