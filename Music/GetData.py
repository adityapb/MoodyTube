from GetVideo import Music
import cPickle as pickle
import os

def GetData(YOUTUBE_API_KEY):
	mood_music = {'sad' : 'motivational',
					'happy' : 'happy',
					'angry' : 'calm'}
	data = {}
	for mood in mood_music:
		x = Music(YOUTUBE_API_KEY, mood)
		data[mood] = x.GetVideoURL()
	with open(str(os.getcwd()) + '/data.db', 'w') as f:
		pickle.dump(data, f)
	return

f = open('id.txt', 'r')
api_key = f.read()
GetData(api_key)