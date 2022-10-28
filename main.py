#!/usr/bin/python

# Create a playlist in the user account with all the highlights of the games of the Week End

import argparse
import os
import datetime

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from sourceCode import *
    
CLIENT_SECRETS_FILE = 'code_secret_client_836432930376-9qe7hdo8pnsdbl92gt13n2gcq0fltkfg.apps.googleusercontent.com.json'

SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
    
# Authorize the request and store authorization credentials.
def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
    


if __name__ == '__main__':
  teams = ['real madrid', 'barca', 'arsenal', 'manchester city', 'liverpool', 'marseille','bayern']
  youtube = get_authenticated_service()
  while(1):
    if searchPlaylist(youtube) == None :
      playlist = create_Playlist(youtube)
    else:
      playlist = searchPlaylist(youtube)
    queries = queryDefinition()
    video = search_highlights(youtube, queries)
    fill_playlist(youtube, playlist, video)
    input()

