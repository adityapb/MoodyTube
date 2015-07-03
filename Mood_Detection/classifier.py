import cPickle as pickle
from sklearn import svm

class SVM():
	
	def __init__(self,data_file):
		data = pickle.load(open(data_file,"r"))
		self.X = data[0]
		self.Y = data[1]
		
	def train(self):
		clf = svm.SVC(kernel='linear', C=2)
		clf.fit(self.X,self.Y)
		return clf
		
	def saveClassifier(self):
		pickle.dump(self.train(), open("classifier.db","w"))
		
class Predictor():
	
	def __init__(self, data_file):
		self.classifier = pickle.load(open(data_file,"r"))
		
	def predict(self, inpt):
		return self.classifier.predict(inpt)
		
if __name__ == "__main__":
	s = SVM("data_svm.db")
	s.saveClassifier()
	#p = Predictor('classifier.db')
	#inpt = pickle.load(open('testval.db','r'))
	#print p.predict(inpt)
	
