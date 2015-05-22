from GetVideo import Music
import cPickle as pickle
import os

def GetData(YOUTUBE_API_KEY):
	mood_music = {'sad' : 'motivational',
					'happy' : 'happy',
					'angry' : 'calm'}
	data = {}
	for mood in mood_music:
		x = Music(YOUTUBE_API_KEY, mood_music[mood])
		data[mood] = x.GetVideoURL()
	data[''] = ''
	with open(str(os.getcwd()) + '/data.db', 'w') as f:
		pickle.dump(data, f)
	return

f = open('id.txt', 'r')
api_key = f.read()
f.close()
GetData(api_key)