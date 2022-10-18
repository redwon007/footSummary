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

    
CLIENT_SECRETS_FILE = 'code_secret_client_836432930376-9qe7hdo8pnsdbl92gt13n2gcq0fltkfg.apps.googleusercontent.com.json'

SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
    
# Authorize the request and store authorization credentials.
def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
    
def create_Playlist(youtube):
  date = datetime.datetime.now(datetime.timezone.utc)
  body = dict(
    snippet=dict(
      title='resume du week end' ,
      description='tout le meilleur contenu du week end' + date.isoformat()
    ),
    status=dict(
      privacyStatus='private'
    ) 
  ) 

  playlist = youtube.playlists().insert(
    part='snippet,id,status',
    body=body
  ).execute()

  return(playlist)

def searchPlaylist(youtube):
  request = youtube.playlists().list(
      part="snippet,contentDetails",
      maxResults=51, #to change to get all playlist (defalault is 5)
      mine=True
  )
  response = request.execute()

  #namesOfPlaylists = [response['items'][i]['snippet']['title'] for i in range(len(response['items']))]
  for i in range(len(response['items'])):
    if response['items'][i]['snippet']['title'] == 'resume du week end':
      return(response['items'][i])



def search_highlights(youtube, teams):
  videos = []
  date = datetime.datetime.now(datetime.timezone.utc)
  date = date + datetime.timedelta(days=-7)
  default=date.isoformat()
  for team in teams :
    search_response = youtube.search().list(
      q=team,
      part='id,snippet',
      maxResults=1,
      publishedAfter=date.isoformat()
    ).execute()

    videos.append(search_response['items'][0]['id'])

  return(videos)

  


def fill_playlist(youtube, playlist, videos):

  for video in videos:
    body = dict(
      snippet=dict(
        playlistId=playlist['id'],
        resourceId=video
      )
    )
    playlistItems_insert_response = youtube.playlistItems().insert(
      part='id,snippet',
      body=body
        ).execute()


  '''
  
    body=dict(
      snippet=dict(
        playlistId='PLU0gTL-vIMec56150WMYRqqbMdVNXbYtI',
        resourceId=dict(
          kind='youtube#video',
          videoId='C_bihBdAmXk'
        )
      )
    )'''