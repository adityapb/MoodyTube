#!/usr/bin/python

from Image import Image
import cv2

class Mood_Detect():
	
	def __init__(self, nose_cascade = None, face_cascade = None, eye_cascade = None):
		self.nose = Image(nose_cascade)
		self.face = Image(face_cascade)
		self.eye = Image(eye_cascade)
		
	def GetImage(self, port):
		cam_port = port
		cam = cv2.VideoCapture(port)
		ret, image = cam.read()
		del(cam)
		return image
		
	def IdError(self, img):
		face = self.identify(self.face, img)
		if len(face) in not 1: raise Exception('Error in detection')
		for (x, y, w, h) in face:
			return img[y:y+h , x:x+w]
		
	def identify(self, cascade, img):
		Cascade = cv2.CascadeClassifier(cascade)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		objects = []
		objects = Cascade.detectMultiScale(
		    gray,
		    scaleFactor=1.1,
		    minNeighbors=5,
		    minSize=(30, 30),
		    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
		)
		print "Found {0} objects!".format(len(objects))
		for (x, y, w, h) in objects:
			objects.append((x, y, w, h))
		return objects
		
	def GetAngle(self, corners):
		tangent = (corners[0][1] - corners[1][1])/float(corners[0][0] - corners[1][0])
		angle = math.degrees(math.atan(tangent))
		return angle
		
	def AlignEyes(self, img):
		'''Use Shi-Tomasi corner detection'''
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		result = []
		for (p, q, r, s) in self.identify(self.face, img):
			eyes = self.identify(self.eye, img[q:q+s , p:p+r])
			if len(eyes) is 2:
				for (x, y, w, h) in eyes:
					corners = cv2.goodFeaturesToTrack(gray[y:y+h , x:x+w],1,0.01,10)
					corners = np.int0(corners)
					for i in corners:
						u,v = i.ravel()
						result.append((u+x+p, v+y+q))
		else:
			return img
		angle = self.GetAngle(corners)
		return self.eye.rotateImage(img, angle)
		
	def GetNose(self, img):
		nose = self.identify(self.nose, img)
		if len(nose) is not 1:
			return None
		for (x, y, w, h) in nose:
			return (x + (w/2.) , y + (h/2.))
			
	def GetFace(self, img):
		face = self.identify(self.face, img)
		if len(face) is not 1:
			return None
		for (x, y, w, h) in face:
			return (w, h)
			
	def AlignImage(self, img):
		center = self.GetNose(img)
		dimensions = self.GetFace(img)
		try:
			return (center[0] - (dimensions[0]/2.),
					center[1] - (dimensions[1]/2.), 
					dimensions[0], 
					dimensions[1])
		except:
			return None
			
	def crop(self, img):
		x = self.AlignImage(img)
		try:
			return img[x[1]:x[1]+x[3] , x[0]:x[0]+x[2]]
		except:
			return self.IdError(img)
			
			
