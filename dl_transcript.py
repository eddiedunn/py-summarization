import sys
from youtube_transcript_api import YouTubeTranscriptApi



def download_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)


    # Save the transcript to a file
    with open(f"{video_id}.txt", 'w', encoding='utf-8') as f:
        for entry in transcript:
            f.write(entry['text'].replace('\n', '') + ' ')

# Check if video ID is provided as a command line argument
if len(sys.argv) < 2:
    print("Please provide the video ID as a command line argument.")
    print("Example usage: python script_name.py <video_id>")
else:
    video_id = sys.argv[1]
    download_transcript(video_id)