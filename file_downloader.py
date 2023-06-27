

import os
import requests
import re
import json
import sys
from bs4 import BeautifulSoup
from urllib.parse import unquote, urlparse
from yt_processor import YouTubeProcessor


class FileDownloader:

    def __init__(self, dest_dir):
        self.dest_dir = dest_dir



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
            yt_processor = YouTubeProcessor(self.dest_dir )
            full_filepath = yt_processor.download_yt_transcript(parsed_url)
        else: # assume it's a web page or downloadable file
            full_filepath = self.get_url_content(url)
            full_filepath = self.convert_to_text(full_filepath)

        return full_filepath



def main(url_to_download):
    # Load settings from 'settings.json'
    with open('settings.json', 'r') as settings_file:
        settings = json.load(settings_file)

    # Get the destination directory from settings
    dest_dir = settings['destination_directory']

    # Initialize the FileDownloader
    downloader = FileDownloader(dest_dir)

    # Perform the file download
    return downloader.download_full_content(url_to_download)

# If this script is being run from the command line
if __name__ == '__main__':
    # Ensure a URL was provided
    if len(sys.argv) < 2:
        print("Please provide a URL to be downloaded.")
    else:
        print(main(sys.argv[1]))  # sys.argv[1] contains the second argument provided to the script