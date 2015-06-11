#!/usr/bin/python

from PreProcessing import PreProcessing
import cv2
import numpy as np
import sys
import glob
import os
import heapq

class PCA:
	
	def __init__(self, *args):
		self.images = args
		
	def eigenfaces(self, K):
		faces = []
		eig = self.eigenvectors()
		eigenvals = heapq.nlargest(K, eig)
		for key in eigenvals:
			faces.append(eig[key])
		return faces
			
	def rowVec(self, image):
		'''image is grayscale image'''
		result = np.array([])
		for row in image:
			#print row
			result = np.concatenate([result, row])
		return result
		
	def imageMat(self):
		mat = []
		for image in self.images:
			mat.append(self.rowVec(image).tolist())
		return np.array(mat)
		
	def covMat(self):
		return np.cov(self.imageMat().T)
		
	def eigenvectors(self):
		res = {}
		eigenvals, eigenvecs = np.linalg.eig(self.covMat())
		for i, val in enumerate(eigenvals):
			res[val] = eigenvecs[i]
		return res
		
if __name__ == '__main__':
	if 'test' in sys.argv:
		filenames = []
		for filename in glob.glob(os.getcwd() + '/male/*.bmp'):
			print filename
			filenames.append(cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2GRAY))
		p = PCA(*filenames)
		print p.eigenfaces(3)
	
