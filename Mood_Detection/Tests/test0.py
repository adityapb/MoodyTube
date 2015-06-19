from eigenfaces import PCA
import glob
import sys

'''
Test for finding matched image
'''

if __name__ == "__main__":
	'''
	1 -> image name
	2 -> dir name
	3 -> number of eigenfaces
	4 -> threshold value
	'''
	P = PCA()
	files = []
	for filename in glob.glob(sys.argv[2] + '/*.bmp'):
		files.append(filename)
	P.createFaceVal(files)
	P.calculateWeights(int(sys.argv[3]))
	dist, result = P.findmatchingimage(sys.argv[1], int(sys.argv[3]), int(sys.argv[4]))
	print result
	
