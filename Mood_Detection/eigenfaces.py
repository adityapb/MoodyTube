#!/usr/bin/python

from numpy import max
from numpy import zeros
from numpy import average
from numpy import dot
from numpy import asfarray
from numpy import sort
from numpy import trace
from numpy import argmin
from numpy import mean
from numpy import array
from numpy.linalg import *
import imageops
from os.path import isdir,join,normpath
from os import listdir,mkdir,getcwd,remove
from shutil import rmtree
import cPickle as pickle
from math import sqrt
import cv2
import sys
import glob
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class ImageError(Exception):
    pass

class DirError(Exception):
    pass 

class FaceVal():
	def __init__(self,imglist,wd,ht,adjfaces,fspace,avgvals,evals):
		self.imglist=imglist
		self.wd=wd
		self.ht=ht
		self.adjfaces=adjfaces
		self.eigenfaces=fspace
		self.avgvals=avgvals
		self.evals=evals
        
class PCA():
	def validateDirectory(self,imgfilenameslist):                
		if (len(imgfilenameslist)==0):
			print "folder empty!"
			raise DirError("folder empty!")
		imgfilelist=[]
		for z in imgfilenameslist:
			img=imageops.XImage(z)
			imgfilelist.append(img)        
		sampleimg=imgfilelist[0]
		imgwdth=sampleimg._width
		imght=sampleimg._height        
        #check if all images have same dimensions
		for x in imgfilelist:
			newwdth=x._width
			newht=x._height
			if((newwdth!=imgwdth) or (newht!=imght)):
				raise DirError("select folder with all images of equal dimensions !")
		return imgfilelist

	def createFaceVal(self, imglist):
		imgfilelist=self.validateDirectory(imglist)
		img=imgfilelist[0]
		imgwdth=img._width
		imght=img._height
		numpixels=imgwdth * imght
		numimgs=len(imgfilelist)               
        #trying to create a 2d array ,each row holds pixvalues of a single image
		facemat=zeros((numimgs,numpixels))               
		for i in range(numimgs):
			pixarray=asfarray(imgfilelist[i]._pixellist)
			pixarraymax=max(pixarray)
			pixarrayn=pixarray/pixarraymax                        
			facemat[i,:]=pixarrayn           
        
        #create average values ,one for each column(ie pixel)        
		avgvals=average(facemat,axis=0)        
        #make average faceimage in currentdir just for fun viewing..
		#if isdir('/average.png'): remove('average.png')
		self.average_image = imageops.make_image(avgvals,"average.png",(imgwdth,imght))              
        #substract avg val from each orig val to get adjusted faces(phi of T&P)
		adjfaces=facemat-avgvals        
		adjfaces_tr=adjfaces.transpose()
		L=dot(adjfaces , adjfaces_tr)
		evals1,evects1=eigh(L)        
		reversedevalueorder=evals1.argsort()[::-1]
		evects=evects1[:,reversedevalueorder]               
		evals=sort(evals1)[::-1]                
        #rows in u are eigenfaces        
		u=dot(adjfaces_tr,evects)
		u=u.transpose()               
        #NORMALISE rows of u
		for i in range(numimgs):
			ui=u[i]
			ui.shape=(imght,imgwdth)
			norm=trace(dot(ui.transpose(), ui))            
			u[i]=u[i]/norm        
        
		self.bundle=FaceVal(imglist,imgwdth,imght,adjfaces,u,avgvals,evals)
		#self.save(u,avgvals)
		self.createEigenimages(u)# eigenface images
		
	def createEigenimages(self,eigenspace):                
		egndir='../eigenfaces'        
		if isdir(egndir):                
			rmtree(egndir,True)               
		mkdir(egndir)
		numimgs=len(self.bundle.imglist)
		faces = []
		for x in range(numimgs):
			imgname=egndir+"/eigenface"+str(x)+".png"            
			faces.append(imageops.make_image(eigenspace[x],imgname,(self.bundle.wd,self.bundle.ht)))
		return faces
		
	def calculateWeights(self,selectedfacesnum,eigenfaces = None,adjfaces = None):
		'''Each row of wts is weight for corresponding adjface'''
		setWeights0, setWeights1 = False, False
		if eigenfaces is None:
			eigenfaces = self.bundle.eigenfaces
			setWeights0 = True
		if adjfaces is None:
			adjfaces = self.bundle.adjfaces
			setWeights1 = True
		usub=eigenfaces[:selectedfacesnum,:]        
		wts=dot(usub,adjfaces.transpose()).transpose()                         
		if setWeights0 is True and setWeights1 is True: self.weights = wts
		return wts
		
	def createWeightHash(self):
		weights = {}
		for i,filename in enumerate(self.bundle.imglist):
			weights[filename] = self.weights[i]
		return weights
		
	def inputWeight(self,imagename,selectedfacesnum,avgvals=None,eigenfaces=None):
		if avgvals is None: avgvals = self.bundle.avgvals
		if eigenfaces is None: eigenfaces = self.bundle.eigenfaces
		selectimg=self.validateselectedimage(imagename)
		inputfacepixels=selectimg._pixellist
		inputface=asfarray(inputfacepixels)
		pixlistmax=max(inputface)
		inputfacen=inputface/pixlistmax        
		inputface=inputfacen-avgvals
		usub=eigenfaces[:selectedfacesnum,:]
		return dot(usub,inputface.transpose()).transpose()
	
	def findmood(self,imagename,selectedfacesnum,weights=None,avgvals=None,eigenfaces=None):
		input_wk=self.inputWeight(imagename,selectedfacesnum,avgvals,eigenfaces)
		dist_sad, dist_happy, c_sad, c_happy = 0,0,0.,0.
		if weights is None: weights = self.createWeightHash()
		for filename in weights:
			if "sad" in filename:
				dist_sad += sqrt(((weights[filename]-input_wk)**2).sum())
				c_sad += 1
			if "happy" in filename:
				dist_happy += sqrt(((weights[filename]-input_wk)**2).sum())
				c_happy += 1
		result=""
		print dist_sad, dist_happy
		if dist_sad/c_sad > dist_happy/c_happy: result = "happy"
		else: result = "sad"
		return result
		
	def data(self):
		weights = self.createWeightHash()
		X,Y = [],[]
		for key in weights:
			if "happy" in key: Y.append("happy")
			else: Y.append("sad")
			X.append(weights[key])
		return X,Y
		
	def savedata(self):
		X,Y = self.data()
		pickle.dump([array(X), array(Y)], open("data_svm.db","w"))
		
	def validateselectedimage(self,imgname):                     
		selectimg=imageops.XImage(imgname)
		return selectimg
			
	def plot(self,selectedfacesnum,imagename=None):
		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		w = self.createWeightHash()
		if imagename is not None:
			res = self.inputWeight(imagename,selectedfacesnum)
			ax.scatter(res[0],res[1],res[2],c='#00FF00')
		for key in w:
			val = w[key]
			#print key
			if "sad" in key:
				ax.scatter(val[0], val[1], val[2], c = '#000000')
			if "happy" in key:
				ax.scatter(val[0], val[1], val[2])
			if "angry" in key:
				ax.scatter(val[0], val[1], val[2], c='#FF0000')
		fig.savefig('plot.png')
		plt.show()
		
	def saveVals(self,selectedfacesnum):
		'''save self.bundle.eigenfaces and self.bundle.avgvals and self.weights'''
		BASE_PATH = os.path.dirname(os.path.realpath(sys.argv[0]))
		pickle.dump(self.bundle.eigenfaces[:selectedfacesnum,:], open(BASE_PATH+'/eigendata/eigenfaces.db','w'))
		pickle.dump(self.bundle.avgvals, open(BASE_PATH+'/eigendata/average.db','w'))
		pickle.dump(self.weights, open(BASE_PATH+'/eigendata/weights.db','w'))
		return
        
if __name__ == '__main__':
	P = PCA()
	files = []
	for filename in glob.glob(sys.argv[1] + '/*.bmp'):
		files.append(filename)
	P.createFaceVal(files)
	P.calculateWeights(3)
	#P.savedata()
	#P.saveVals(14)
	P.plot(3,'test.bmp')
		
