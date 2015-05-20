#!/usr/bin/python

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

class YouTube:
  DEVELOPER_KEY = ""
  YOUTUBE_API_SERVICE_NAME = ""
  YOUTUBE_API_VERSION = ""

  def __init__(self, key):
    self.DEVELOPER_KEY = key
    self.YOUTUBE_API_SERVICE_NAME = "youtube"
    self.YOUTUBE_API_VERSION = "v3"

  def youtube_search(self, options):
    youtube = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
      developerKey=self.DEVELOPER_KEY)

    search_response = youtube.search().list(
      q=options.q,
      part="id,snippet",
      maxResults=options.max_results
    ).execute()

    for search_result in search_response.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        return search_result["id"]["videoId"]
    return -1

  def GetID(self, search_str):
    argparser.add_argument("--q", help="Search term", default=search_str)
    argparser.add_argument("--max-results", help="Max results", default=1)
    args = argparser.parse_args()

    try:
      return self.youtube_search(args)
    except:
      return -1