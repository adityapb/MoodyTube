from GetVideo import Music
import cPickle as pickle
import os
import sys

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

if __name__ == '__main__':
	GetData(str(sys.argv[1]))
