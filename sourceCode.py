#!/usr/bin/python

# Create a playlist in the user account with all the highlights of the games of the Week End

import argparse
import os, glob
import datetime
import pytz

from pathlib import Path
import json

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

  playlist = None

  ###search all my playlist
  playlists = youtube.playlists().list(
      part="snippet,contentDetails",
      maxResults=51, #to change to get all playlist (defalault is 5)
      mine=True
  ).execute()


  ###search the playlist named 'resume du week end' the name of the playlist by convention
  #namesOfPlaylists = [playlists['items'][i]['snippet']['title'] for i in range(len(playlists['items']))]
  for i in range(len(playlists['items'])):
    if playlists['items'][i]['snippet']['title'] == 'resume du week end':
      playlist = playlists['items'][i]
      
      ###delete all videos in the playlist
      videosInThePlaylist = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=51, #to change to get all playlist (defalault is 5)
        playlistId=playlist['id']
      ).execute()

      #print(videosInThePlaylist)
      for i in range(len(videosInThePlaylist['items'])):

        youtube.playlistItems().delete(
            id=videosInThePlaylist['items'][i]['id']
        ).execute()

  return(playlist)

def queryDefinition():
  utc=pytz.UTC

  premier_league_file = 'calendars/Premier_League.json'
  ligue_1_file = 'calendars/Ligue_1.json'

  path = 'calendars'

  queries = []

  for filename in glob.glob(os.path.join(path, '*.json')):
    with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode

      league = Path(filename).stem
      print(league)
      filename = json.load(f)

      
      
      queries_League = []
      for i, match in enumerate(filename):
        
        date_match = datetime.datetime.strptime(match['DateUtc'][:-1], '%Y-%m-%d %H:%M:%S')
        date_match = utc.localize(date_match)

        date_now = datetime.datetime.now(datetime.timezone.utc)
        date_week_before = date_now + datetime.timedelta(days=-7)
          
        if date_week_before <= date_match <= date_now :

          query = 'resume ' + match['HomeTeam'] + ' ' + match['AwayTeam']
        
          queries_League.append(query)
          
      dict = {}
      dict[league] = queries_League

      queries.append(dict)
  return(queries)

  


def search_highlights(youtube, queries):
  videos = []
  date = datetime.datetime.now(datetime.timezone.utc)
  date = date + datetime.timedelta(days=-7)
  default=date.isoformat()
  for query in queries :
    '''search_response = youtube.search().list(
      q=query,
      part='id,snippet',
      maxResults=1,
      publishedAfter=date.isoformat()
    ).execute()'''

    videos.append(search_response['items'][0]['id'])

  return(videos)

  


def fill_playlist(youtube, playlist, videos):

  for video in videos:
    print(video)
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