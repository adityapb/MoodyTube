#!/usr/bin/python

from YouTubeId import YouTube
import urllib
import json

class Music:
	url = ""
	YOUTUBE_API_KEY = ""

	def __init__(self, api_key, tag):
		self.url = 'http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag=' + tag + '&api_key=e17566c75feedfd740e58e0251cf4eb9&format=json'
		self.YOUTUBE_API_KEY = api_key

	def GetTracks(self):
		page = urllib.urlopen(self.url)
		jObj = json.load(page)
		tracks = []
		for dict in jObj["toptracks"]["track"]:
			tracks.append(dict["name"] + ", " + dict["artist"]["name"])
		return tracks

	def GetVideoURL(self):
		BASE_URL = "https://www.youtube.com/watch?v="
		tracks = self.GetTracks()
		y = YouTube(self.YOUTUBE_API_KEY)
		urls = []
		for track in tracks:
			urls.append(BASE_URL + y.GetID(track))
		return urls
