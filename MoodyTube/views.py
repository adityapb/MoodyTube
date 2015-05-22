from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import os
import cPickle as pickle

def PlayMusic(request):
	#print mood
	t = get_template('mood.html')
	mood = request.GET.get('q', '')
	with open(str(os.getcwd()) + '/Data/data.db', 'rb') as f:
		data = pickle.load(f)
	playlists = data[str(mood)]
	c = {'playlist' : playlists,
		 'query' : mood}
	html = t.render(Context(c))
	return HttpResponse(html)