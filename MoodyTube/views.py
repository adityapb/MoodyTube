from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
import os
import cPickle as pickle

from django.contrib.auth.models import User
from django.contrib.auth import logout
from MoodyTube.forms import *
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required

def main_page(request):
	return render_to_response('main_page.html', RequestContext(request))

@login_required
def PlayMusic(request):
	t = get_template('mood.html')
	mood = request.GET.get('q', '')
	with open(str(os.getcwd()) + '/Data/data.db', 'rb') as f:
		data = pickle.load(f)
	playlists = data[str(mood)]
	c = {'playlist' : playlists,
		 'query' : mood,}
	return render_to_response('mood.html', c, context_instance = RequestContext(request))

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/login')

def register_page(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password1'],
				email = form.cleaned_data['email']
			)
			return HttpResponseRedirect('/login/')
	else:
		form = RegistrationForm()
	variables = RequestContext(request,{ 'form' : form })
	return render_to_response(
		'registration/register.html',
		variables
	)