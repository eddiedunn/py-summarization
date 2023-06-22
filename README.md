# Summarizer App

Summarizer App is a Python application written for Linux that allows you to summarize text from different sources such as files, clipboard, or URLs using langchain and OpenAI models. The app provides a user-friendly interface built with the Tkinter library.

Currently it can deal with local or downloaded files:

 - **Web pages** (download only) Extracts text using Beautiful Soup
 - **PDF Files** Extracts using PyMuPDF 
 - **Text Files**
 - **Youtube URLS** Downloads transcripts using youtube_transcript_api and google-api-python-client
 - **Audio/Video Files** Creates transcript of audio using OpenAI whisper


## Features

- **Source selection**: You can choose the source of the text you want to summarize, including file, clipboard, or URL.
- **File selection**: If you select the file as the source, you can browse and select the desired file using a file selector.
- **URL input**: If you choose the URL as the source, you can enter the URL of the web page you want to summarize.
- **Destination selection**: You can specify the directory where you want to save the summarized output.
- **Summary method selection**: You can choose between two summary methods: "Simple" and "MapReduce."
- **Model selection**: You can select the language model for the summarization process.
- **Summarize button**: Clicking this button initiates the summarization process based on the selected options.
- **Previous settings**: The app remembers the previously selected settings (destination directory, source type, summary method, and model) and loads them if available.

## Prerequisites

Before running the application, make sure you have the following dependencies installed:

- tkinter: This library is used for the graphical user interface.
- openai: This library is used for LLM models (requires API key)
- langchain: This library is used to make the process easier
- Beautiful Soup: This is used to extact text from web pages.
- dotenv: This library is used to load environment variables from the .env file.
- whisper: This library is used for audio/video transcription.
- fitz: This library is used for PDF text extraction.
- youtube_transcript_api: Used to download Youtube transcripts
- google-api-python-client: Used to get Titles and Channel Names from Youtube videos (requires API key)
- pymupdf: Used to extract text from pdf files
- pyperclip: This library is used for clipboard interaction.

You can install the dependencies by running the following command:

```bash
pip install tkinter python-dotenv whisper pymupdf pyperclip bs4 youtube-transcript-api google-api-python-client langchain openai
```

## Usage

1. Clone the repository and navigate to the project directory.
2. Create a .env file in the project directory and add your OpenAI API key:

```bash
OPENAI_API_KEY=your-api-key
GOOGLE_API_KEY=your-google-api-key
```

3. Run the main.py file:

```bash
python main.py
```

4. The Summarizer App window will open.
5. Select the source type from the dropdown menu (File, Clipboard, or URL).
6. Depending on the selected source type, provide the necessary information (e.g., select a file or enter a URL). NOTE: A URL can be a local path.
7. Choose the destination directory where the summarized output will be saved by clicking the "Select Destination" button.
8. Select the desired summary method and language model from the respective dropdown menus.
9. Click the "Summarize" button to initiate the summarization process.
10. The summarized output will be saved in the specified destination directory.
11. The summarized file will open in a new window.

## File Structure

The project contains the following files:

- `main.py`: The main script that initializes the Summarizer App and handles the GUI interactions.
- `file_summarizer.py`: A module that provides the functionality to summarize files using different methods.
- `file_downloader.py`: A module that handles downloading files from URLs.
- `file_transcriber.py`: A module that handles transcribing audio/video files and clipboard content.
- `settings.json`: A JSON file that stores the previous settings of the application.
- `models.json`: A JSON file that stores the available language models for summarization.

## Acknowledgments

The Summarizer App uses the following libraries:

- tkinter: A standard GUI library for Python.
- dotenv: A library for loading environment variables from a file.
- whisper: A library for audio/video transcription.
- fitz: A library for PDF text extraction.
- pyperclip: A library for clipboard interaction.

## License

This project is licensed under the Apache License.
