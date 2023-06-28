from urllib.parse import  parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
from googleapiclient.discovery import build
import os
import re
import pprint
import whisper
from pydub import AudioSegment
from file_summarizer import FileSummarizer
from urllib.parse import urlparse


class YouTubeProcessor:
    def __init__(self, dest_dir, summary_method, model_var, max_tokens):
        self.dest_dir = dest_dir
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.summary_method = summary_method
        self.model_var = model_var
        self.max_tokens = max_tokens
        self.timestamp_regex = r'\b\d{1,2}:\d{2}\b'
        self.whisper_model_name = 'base'

    def transcribe_video(self, url):
        self.download_yt_transcript(url)

    def summarize_video(self, url):
        video_id = self.get_video_id(url)
        details = self.get_video_details(video_id)
        has_time_stamps = details['has_time_stamps']
        if has_time_stamps:
            summary_path = self.summarize_with_timestamps(url, details)
        else:
            full_path = self.download_yt_transcript(url)
            summary_path = self.call_summarizer(full_path)
        
        return summary_path
    
    def summarize_with_timestamps(self, url, details):
        downloaded_file = self.download_video(url)
        timestamps = self.extract_timestamps(details['description'])
        extracted = self.extract_audio_segments(downloaded_file, timestamps)
        speech_to_text = whisper.load_model(self.whisper_model_name)
        summaries = []
        for segment in extracted:
            segment_full_text = segment+'.txt'
            text = speech_to_text.transcribe(segment)["text"]
            with open(segment_full_text, 'w') as f:
                f.write(text)
            summary_file = self.call_summarizer(segment_full_text)

            with open(summary_file, 'r') as f:
                summary = f.read()

            summaries.append(summary)
            summaries.append('--------------------------------------------------------------------------\n')


        file_path = self.concatenate_and_save(summaries, downloaded_file)

        return file_path

    def concatenate_and_save(self, strings_list, file_path):
        concatenated_string = ' '.join(strings_list)
        file_name = file_path.split('/')[-1].split('.')[0] + '-summary.txt'
        new_file_path = '/'.join(file_path.split('/')[:-1]) + '/' + file_name

        with open(new_file_path, 'w') as file:
            file.write(concatenated_string)

        return new_file_path

    # def extract_audio(self, file_path, start_time, end_time, output_path):
    #     audio = AudioSegment.from_file(file_path)

    #     # pydub calculates in milliseconds
    #     start_time = start_time * 1000  # convert to milliseconds
    #     end_time = end_time * 1000  # convert to milliseconds

    #     extracted = audio[start_time:end_time]


    #     # save the result
    #     extracted.export(output_path, format="webm")

    def call_summarizer(self, full_path):
        summarizer = FileSummarizer(self.model_var, self.max_tokens)
        summary_path = summarizer.summarize_file(full_path, 
                                                self.summary_method, 
                                                self.dest_dir)

        return summary_path
    
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
        pattern = re.compile(self.timestamp_regex)
        matches = re.findall(pattern, description)
        return len(matches) > 0

    def extract_timestamps(self, description):
        # The pattern matches a string that starts with one or two digits, followed by a colon, 
        # followed by two digits, and then a space.
        pattern = re.compile(self.timestamp_regex)
        matches = re.findall(pattern, description)
        return matches

    def extract_audio_segments(self, file_path, timestamps):
        audio = AudioSegment.from_file(file_path)
        output_files = []  # List to hold the names of the output files

        # # Ensure the list starts with '0:00'
        # if timestamps[0] != '0:00' or timestamps[0] != '00:00':
        #     timestamps.insert(0, '00:00')

        # Add a timestamp for the end of the audio
        timestamps.append(str(len(audio) // 1000 // 60) + ':' + str((len(audio) // 1000) % 60))

        for i in range(len(timestamps) - 1):
            start_time = self.timestamp_to_seconds(timestamps[i]) * 1000  # Convert to milliseconds
            end_time = self.timestamp_to_seconds(timestamps[i + 1]) * 1000  # Convert to milliseconds

            segment = audio[start_time:end_time]

            # Define the output file name
            output_file = f'{self.dest_dir}/segment_{i + 1}.webm'

            # Save the segment
            segment.export(output_file, format='webm')

            # Add the output file name to the list
            output_files.append(output_file)

        return output_files  # Return the list of output files



    def timestamp_to_seconds(self, timestamp):
        """Converts a timestamp in 'HH:MM' format to seconds."""
        minutes, seconds = map(int, timestamp.split(':'))
        return minutes * 60 + seconds

    def download_video(self, url):
        ydl_opts = {
            'outtmpl': f'{self.dest_dir}/%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            ydl.download([url])
            filename = ydl.prepare_filename(info_dict)
            return filename #os.path.basename(filename)

    def get_video_id(self, url):
        parsed_url = urlparse(url)
        # parse the query part of the URL
        query_params = parse_qs(parsed_url.query)

        # the video ID is associated with the "v" parameterpyth
        return query_params.get("v")[0]

    def download_yt_transcript(self, parsed_url):

        video_id = self.get_video_id(parsed_url)

        if not video_id:
            raise ValueError("The URL does not contain a video ID")
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        video_details  = self.get_video_details(video_id )
        #pprint.pprint(video_details, indent=2, width=100)

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