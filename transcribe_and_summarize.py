import os
import json
import sys
from file_summarizer import FileSummarizer
from file_transcriber import FileTranscriber

def main(file_to_transcribe):
    # Load settings from 'settings.json'
    with open('settings.json', 'r') as settings_file:
        settings = json.load(settings_file)

    # Load model details from 'models.json'
    with open('models.json', 'r') as models_file:
        models = json.load(models_file)

    # Get the model details for the model specified in the settings
    model_details = next((model for model in models if model['model_name'] == settings['model_name']), None)

    # If the model details are not found, throw an error
    if not model_details:
        raise ValueError(f"Model details for model {settings['model_name']} not found in 'models.json'")

    # Get the destination directory from settings
    dest_dir = settings['destination_directory']

    # Initialize the FileTranscriber
    transcriber = FileTranscriber(dest_dir)

    # Perform the file transcription
    transcribed_file_path = transcriber.transcribe(file_to_transcribe)

    # Initialize the FileSummarizer
    summarizer = FileSummarizer(model_details['model_name'], model_details['max_tokens'])

    # Perform the file summarization
    summary_file_path = summarizer.summarize_file(
        transcribed_file_path,
        settings['summary_method'], 
        dest_dir
    )

    return summary_file_path

# If this script is being run from the command line
if __name__ == '__main__':
    # Ensure a file path was provided
    if len(sys.argv) < 2:
        print("Please provide a file path to be transcribed and summarized.")
    else:
        print(main(sys.argv[1]))  # sys.argv[1] contains the second argument provided to the script
