from youtube_transcript_api import YouTubeTranscriptApi

def download_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Save the transcript to a file
    with open(f"{video_id}.txt", 'w', encoding='utf-8') as f:
        for entry in transcript:
            f.write(entry['text'] + '\n')

video_id = 'CjHP1W3nxe8'
download_transcript(video_id)