import whisper 
import os
import json
import sys
import fitz
import pyperclip

class FileTranscriber:

    def __init__(self, dest_dir):
        self.model_name = "base"
        self.dest_dir = dest_dir
        

    def transcribe(self, file_to_transcribe, is_clipboard=False):
        filename_with_extension = os.path.basename(file_to_transcribe)
        filename, extension = os.path.splitext(filename_with_extension)

        text_to_return = ""
        if extension.lower() in ['.mp3', '.wav', '.mp4', '.avi', '.mov', '.flv', '.wmv']:
            # transcribe audio/video file
            speech_to_text = whisper.load_model(self.model_name)
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
    
def main(file_to_transcribe):
    # Load settings from 'settings.json'
    with open('settings.json', 'r') as settings_file:
        settings = json.load(settings_file)

    # Get the destination directory from settings
    dest_dir = settings['destination_directory']

    # Initialize the FileTranscriber
    transcriber = FileTranscriber(dest_dir)

    # Perform the file transcription
    return transcriber.transcribe(file_to_transcribe)

# If this script is being run from the command line
if __name__ == '__main__':
    # Ensure a file path was provided
    if len(sys.argv) < 2:
        print("Please provide a file path to be transcribed.")
    else:
        print(main(sys.argv[1]))  # sys.argv[1] contains the second argument provided to the script