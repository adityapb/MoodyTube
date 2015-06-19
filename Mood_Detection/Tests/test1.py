from eigenfaces import PCA
import glob
import sys

'''
Test plotting weights with 3 eigenface reconstruction
'''

if __name__ == "__main__":
	'''
	1 -> dir name
	2 -> number of eigenfaces
	'''
	P = PCA()
	files = []
	for filename in glob.glob(sys.argv[1] + '/*.bmp'):
		files.append(filename)
	P.createFaceVal(files)
	P.calculateWeights(int(sys.argv[2]))
	P.plot()
	
