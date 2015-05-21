from GetVideo import Music
import cPickle as pickle
import os

def GetData():
	mood_music = {'sad' : 'motivational',
					'happy' : 'happy',
					'angry' : 'calm'}
	data = {}
	for mood in mood_music:
		x = Music("AIzaSyDHr5arzR2mOBNLtilBaRgmyWZsieq3sfc", mood)
		data[mood] = x.GetVideoURL()
	with open(str(os.getcwd()) + '/data.db', 'w') as f:
		pickle.dump(data, f)
	return

GetData()