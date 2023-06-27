import json
import os
from file_summarizer import FileSummarizer
from file_downloader import FileDownloader
from file_transcriber import FileTranscriber

class Model:
    def __init__(self):
        # Load the openai_llm_models.json file
        with open('openai_llm_models.json', 'r') as f:
            self.models = json.load(f)
        self.model_names = [model['model_name'] for model in self.models]

        self.dest_dir = ''
        self.source_type = 'Clipboard'
        self.summary_method = 'Simple'
        self.model_var = self.model_names[0]

        # Initialize file handler objects
        self.file_dl = FileDownloader(self.dest_dir)
        self.transcriber = FileTranscriber(self.dest_dir)
        self.summarizer = FileSummarizer(self.model_var, self.max_tokens)

    def update_button_text(self, transcribe_var):
        if transcribe_var == 1:
            return "Transcribe"
        else:
            return "Summarize"


    def update_model(self, model_name, max_tokens):
        model = next((m for m in self.models if m["model_name"] == model_name), None)
        if model is not None:
            self.max_tokens = max_tokens
            self.endpoint = model["endpoint"]
            self.model_var = model_name
            return True
        else:
            return False




    def update_summary_method(self, summary_method):
        self.summary_method = summary_method
        self.save_settings()  # save settings every time a new summary method is selected

    def update_dest_dir(self, new_dest_dir):
        self.dest_dir = new_dest_dir
        self.save_settings()


    def download_url(self, url):
        try:
            file_dl = FileDownloader(self.dest_dir)
            full_content_path = file_dl.download_full_content(url)
            return full_content_path, None
        except Exception as e:
            return None, str(e)

    def transcribe_file(self, full_content_path, is_clipboard):
        transcriber = FileTranscriber(self.dest_dir)
        full_content_path = transcriber.transcribe(full_content_path, is_clipboard)
        return full_content_path

    def summarize_file(self, full_content_path):
        summarizer = FileSummarizer(self.model_var, self.max_tokens)
        summary_path = summarizer.summarize_file(full_content_path, self.summary_method, self.endpoint)
        return summary_path