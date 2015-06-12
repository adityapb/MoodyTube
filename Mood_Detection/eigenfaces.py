#!/usr/bin/python

from PreProcessing import PreProcessing
import cv2
import numpy as np
import sys
import glob
import os
import heapq

class PCA:
	
	def __init__(self, length, *args):
		self.length = length
		self.images = args
		
	def eigenfaces(self, K):
		faces = []
		eig = self.eigenvectors()
		eigenvals = heapq.nlargest(K, eig)
		print eigenvals
		for key in eigenvals:
			faces.append(eig[key])
		for i, face in enumerate(faces):
			faces[i] = np.array(self.reconstruct(face.tolist()))
		return faces
			
	def rowVec(self, image):
		return image.flatten()
		
	def reconstruct(self, vec, length = None):
		if length is None: length = self.length
		res = [[] for x in range(length)]
		for i, val in enumerate(vec):
			res[i/length].append(val)
		return res
		
	def imageMat(self):
		mat = []
		for image in self.images:
			mat.append(self.rowVec(image).tolist())
		return np.array(mat)
		
	def covMat(self):
		mat = self.imageMat()
		print np.dot(mat.T, mat)/float(np.linalg.norm(mat))
		return np.dot(mat.T, mat)/float(np.linalg.norm(mat))
		
	def eigenvectors(self):
		res = {}
		eigenvals, eigenvecs = np.linalg.eigh(self.covMat())
		for i, val in enumerate(eigenvals):
			res[val] = eigenvecs[i]
		return res
		
if __name__ == '__main__':
	if 'test' in sys.argv:
		filenames = []
		for filename in glob.glob(os.getcwd() + '/Data/happy_100_male/*.bmp'):
			print filename
			filenames.append(cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2GRAY))
		p = PCA(100, *filenames)
		print p.eigenfaces(3)
	
