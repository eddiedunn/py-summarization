from urllib.parse import  parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import os
import re
import pprint


class YouTubeProcessor:
    def __init__(self, dest_dir):
        self.dest_dir = dest_dir
        self.google_api_key = os.getenv('GOOGLE_API_KEY')



    def summarize(self, url):
        
        print("Download completed!!")

    def get_video_details(self, video_id):
        youtube = build('youtube', 'v3', developerKey=self.google_api_key)
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()

        items = response.get('items', [])
        if not items:
            raise Exception('No video found with the given id')

        
        snippet = items[0]['snippet']
        

        has_time_stamps = False

        if self.has_timestamps(snippet['description']):
            has_time_stamps = True

        channel_title = snippet['channelTitle']
        video_title = snippet['title']
        channel_id = snippet['channelId']
        description = snippet['description']

        return {'has_time_stamps': has_time_stamps, 
                'channel_title': channel_title, 
                'video_title': video_title, 
                'channel_id': channel_id,
                'description': description}
    
    def has_timestamps(self, description):
        # The pattern matches a string that starts with one or two digits, followed by a colon, 
        # followed by two digits, and then a space.
        pattern = re.compile(r'\b\d{1,2}:\d{2}\b')
        matches = re.findall(pattern, description)
        return len(matches) > 0

    def download_yt_transcript(self, parsed_url):

        # parse the query part of the URL
        query_params = parse_qs(parsed_url.query)

        # the video ID is associated with the "v" parameterpyth
        video_id = query_params.get("v")[0]

        if not video_id:
            raise ValueError("The URL does not contain a video ID")
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        video_details  = self.get_video_details(video_id )
        pprint.pprint(video_details, indent=2, width=100)

        # Replace any characters in the titles that aren't safe for file names
        safe_channel_title = "".join(c for c in video_details['channel_title'] if c.isalnum() or c in ' _-')
        safe_video_title = "".join(c for c in video_details['video_title'] if c.isalnum() or c in ' _-')
        
        file_name = f"{safe_channel_title}_{safe_video_title}.txt"

        full_path = os.path.join(self.dest_dir, file_name)

        # Save the transcript to a file
        with open( full_path, 'w', encoding='utf-8') as f:
            for entry in transcript:
                f.write(entry['text'].replace('\n', '') + ' ')

        return full_path