import whisper 
import os
import json
import sys
import argparse
import fitz
import pyperclip

class FileTranscriber:

    def __init__(self, dest_dir):
        self.whisper_model_name = "base"
        self.dest_dir = dest_dir
        

    def transcribe(self, file_to_transcribe, is_clipboard=False):
        filename_with_extension = os.path.basename(file_to_transcribe)
        filename, extension = os.path.splitext(filename_with_extension)

        text_to_return = ""
        if extension.lower() in ['.mp3', '.wav', '.mp4', '.avi', '.mov', '.flv', '.wmv', '.mkv']:
            # transcribe audio/video file
            speech_to_text = whisper.load_model(self.whisper_model_name)
            text_to_return = speech_to_text.transcribe(file_to_transcribe)["text"]
        elif is_clipboard:
            if not filename:
                filename='clipboard_content.txt'
            text_to_return = pyperclip.paste()
        else:
            text_to_return = self.convert_to_text(file_to_transcribe)

        final_file_to_save = os.path.join(self.dest_dir, filename + ".txt")
        self.save_transcript(text_to_return, final_file_to_save)

        return final_file_to_save
    

    def save_transcript(self, transcript, file_name):
        path_to_save = os.path.join(self.dest_dir, file_name)
        with open(path_to_save, "w") as f:
            f.write(transcript)
        return path_to_save
    

    
    def convert_to_text(self, file_path):
        base, ext = os.path.splitext(file_path)
        
        # If it is a pdf file, convert it to text and write it to a new text file
        if ext.lower() == '.pdf':
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()


        # If it is a text file, just read it
        elif ext.lower() == '.txt':
            with open(file_path, 'r') as f:
                text = f.read()

        else:
            print("File is not a PDF or TXT")
        
        return text
    
def is_av_file(filename, transcribe_all=False):
    """Check if a file should be transcribed."""
    if not transcribe_all:
        if filename.lower().endswith(('.mp3', '.wav', '.mp4', '.avi', '.mov', '.flv', '.wmv', '.mkv')):
            return True
    else:
        return True
    return False

def main(args):
    # Load settings from 'settings.json'
    with open('settings.json', 'r') as settings_file:
        settings = json.load(settings_file)

    # Get the destination directory from settings
    dest_dir = settings['destination_directory']

    # Initialize the FileTranscriber
    transcriber = FileTranscriber(dest_dir)

    # Check if the input is a directory or a file
    if os.path.isdir(args.file_or_dir):
        # If it's a directory, transcribe each file in it
        for root, dirs, files in os.walk(args.file_or_dir):
            for file in files:
                if is_av_file(file, args.all_files):
                    file_path = os.path.join(root, file)
                    print(transcriber.transcribe(file_path))  # transcribe the file
    else:
        # If it's a single file, just transcribe it
        if is_av_file(args.file_or_dir, args.all_files):
            print(transcriber.transcribe(args.file_or_dir))  # transcribe the file


# If this script is being run from the command line
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transcribe files. Only Audio/Video files are transcribed by default.')
    parser.add_argument('file_or_dir', type=str, help='File or directory to transcribe.')
    parser.add_argument('--all_files', action='store_true', help='Transcribe all files, not only audio/video.')
    args = parser.parse_args()

    main(args)  # Pass the arguments to main