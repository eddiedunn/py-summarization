import os
import json

import google.oauth2.credentials
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import Request

# load variables from .env
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']


def get_credentials():
    creds = None

    # The file token.json stores the user's refresh token, client_id and client_secret, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        with open('token.json', 'r') as token:
            token_info = json.load(token)
            creds = google.oauth2.credentials.Credentials.from_authorized_user_info(token_info, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(prompt='consent', open_browser=True)

            # Save the client_secret, client_id, and refresh_token for the next run
            with open('token.json', 'w') as token:
                token_info = {
                    'refresh_token': creds.refresh_token,
                    'client_id': creds.client_id,
                    'client_secret': creds.client_secret,
                }
                json.dump(token_info, token)
    return creds

def download_transcript(video_id):
    # Build the YouTube Data API client
    youtube = build('youtube', 'v3', 
        credentials=get_credentials()
    )

    # Get the video caption tracks
    captions = youtube.captions().list(part='snippet', videoId=video_id).execute()

    for caption in captions['items']:
        # Download the transcript
        transcript = youtube.captions().download(id=caption['id'], tfmt='vtt').execute()

        # Save the transcript to a file
        with open(f"{video_id}_{caption['language']}.vtt", 'w', encoding='utf-8') as f:
            f.write(transcript['body'])



video_id = 'Re4LFUOCJ0A'
download_transcript(video_id)