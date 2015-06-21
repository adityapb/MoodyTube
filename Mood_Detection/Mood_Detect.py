#!/usr/bin/python

from Image import Image
import cv2
import sys
import numpy as np
import math

class Mood_Detect():
	
	def __init__(self, nose_cascade = None, face_cascade = None, eye_cascade = None, sample = None):
		self.nose = Image(nose_cascade)
		self.face = Image(face_cascade)
		self.eye = Image(eye_cascade)
		self.nose_casc = nose_cascade
		self.face_casc = face_cascade
		self.eye_casc = eye_cascade
		val = self.GetDimensions(sample)
		self.dimensions = val['dimensions']
		self.dist = val['distance']
		
	def GetImage(self, port):
		'''
		When two eyes and face are detected, capture the image
		'''
		cam_port = port
		cam = cv2.VideoCapture(port)
		while True:
			ret, image = cam.read()
			face = self.identify(self.face_casc, image)
			if len(face) is 1:
				for x in face:
					if len(self.identify(self.eye_casc, image[x[1]:x[1]+x[3], x[0]:x[0]+x[2]])) is 2:
						del(cam)
						return self.AlignEyes(image)
						
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
		eye = self.GetEyes(img)
		try:
			return {'centre' : ((eye[0][0]+eye[1][0])/2., eye[0][1]), 'dist' : abs(eye[0][0]-eye[1][0])}
		except:
			return None
		
	def IdError(self, img):
		face = self.identify(self.face, img)
		if len(face) is not 1: raise Exception('Error in detection')
		for (x, y, w, h) in face:
			return img[y:y+h , x:x+w]
		
	def identify(self, cascade, image):
		Cascade = cv2.CascadeClassifier(cascade)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
		
	def GetEyes(self, img):
		'''Use Shi-Tomasi corner detection'''
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		result = []
		for (p, q, r, s) in self.identify(self.face_casc, img):
			eyes = self.identify(self.eye_casc, img[q:q+s , p:p+r])
			if len(eyes) is 2:
				for (x, y, w, h) in eyes:
					corners = cv2.goodFeaturesToTrack(gray[y:y+h , x:x+w],1,0.01,10)
					corners = np.int0(corners)
					for i in corners:
						u,v = i.ravel()
						result.append((u+x+p, v+y+q))
		return result
		
	def AlignEyes(self, img):
		return self.eye.rotateImage(img, self.GetAngle(self.GetEyes(img)))
			
	def alignFace(self, image):
		'''
		x -> left
		y -> down
		w -> right + left
		h -> up + down
		'''
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
			return image[x[1]:x[1]+x[3] , x[0]:x[0]+x[2]]
		except:
			self.IdError(image)
			return None
			
if __name__ == '__main__':
	p = Mood_Detect(sys.argv[1], sys.argv[2], sys.argv[3])
	cv2.imshow('face', p.GetImage(0))
	cv2.waitKey(0)
			
			
