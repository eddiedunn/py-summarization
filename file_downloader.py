
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import os
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import unquote

from urllib.parse import urlparse, parse_qs

class FileDownloader:

    def __init__(self, dest_dir):
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.dest_dir = dest_dir

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
        channel_title = snippet['channelTitle']
        video_title = snippet['title']
        return channel_title, video_title
    

    def download_yt_transcript(self, parsed_url):

        # parse the query part of the URL
        query_params = parse_qs(parsed_url.query)

        # the video ID is associated with the "v" parameter
        video_id = query_params.get("v")[0]

        if not video_id:
            raise ValueError("The URL does not contain a video ID")
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        channel_title, video_title = self.get_video_details(video_id )

        # Replace any characters in the titles that aren't safe for file names
        safe_channel_title = "".join(c for c in channel_title if c.isalnum() or c in ' _-')
        safe_video_title = "".join(c for c in video_title if c.isalnum() or c in ' _-')
        
        file_name = f"{safe_channel_title}_{safe_video_title}.txt"

        full_path = os.path.join(self.dest_dir, file_name)

        # Save the transcript to a file
        with open( full_path, 'w', encoding='utf-8') as f:
            for entry in transcript:
                f.write(entry['text'].replace('\n', '') + ' ')

        return full_path

    def save_webpage_content(self, url):
        r = requests.get(url)
        r.raise_for_status()

        # Parse the HTML content of the page with BeautifulSoup
        soup = BeautifulSoup(r.text, 'html.parser')

        # Try to find the main content of the page
        # Here we're guessing that it's in a tag 'main', 'article' or a 'div' with class 'main' or 'content'
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=lambda x: x and ('main' in x or 'content' in x))

        if main_content is None:
            print("Could not find the main content")
        else:
            # Use the URL to generate a filename
            parsed_url = urlparse(url)
            base_name = parsed_url.netloc
            path = parsed_url.path
            filename = f"{base_name}_{path.replace('/', '_')}.txt"
            text = main_content.get_text(strip=True).replace('\n', '')
            full_filepath = os.path.join(self.dest_dir, filename)
            with open(full_filepath, 'w', encoding='utf-8') as f:
                f.write(text)

            return  full_filepath # return the full path
        
    def download_file(self, url):
        
        # Send a HTTP request to the URL
        with requests.get(url, stream=True) as r:
            # Throw an error if the request was unsuccessful
            r.raise_for_status()

            # Get the filename from the Content-Disposition header
            content_disposition = r.headers.get('content-disposition')
            if content_disposition:
                filename = re.findall('filename=(.+)', content_disposition)
                if filename:
                    local_filename = unquote(filename[0])
            else:
                # If there's no Content-Disposition header, fallback to the URL
                local_filename = url.split("/")[-1]

            full_filepath = os.path.join(self.dest_dir, local_filename)

            # Open the file in write-binary mode
            with open(full_filepath, 'wb') as f:
                # Write the contents of the response to the file
                for chunk in r.iter_content(chunk_size=8192):
                    # Filter out keep-alive new chunks
                    if chunk:
                        f.write(chunk)

        print(f"File downloaded as {full_filepath}")

        return full_filepath

    def get_url_content(self, parsed_url):

        # Make a HEAD request
        response = requests.head(parsed_url)

        # Check the Content-Type header
        if 'text/html' in response.headers['Content-Type']:
            # This is probably a web page, let's download it
            full_path = self.save_webpage_content(parsed_url)

        else:
            # This is likely a downloadable file. Let's download it
            full_path = self.download_file(parsed_url)

        return full_path
    
    def download_full_content(self, url):
        full_filepath = ''

        # parse the URL
        parsed_url = urlparse(url)
        if "youtube.com" in parsed_url.netloc:
            full_filepath = self.download_yt_transcript(parsed_url)
        else: # assume it's a web page or downloadable file
            full_filepath = self.get_url_content(url)
            full_filepath = self.convert_to_text(full_filepath)

        return full_filepath



