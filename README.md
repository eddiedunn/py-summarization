# Summarizer App

Summarizer App is a Python application that allows you to summarize text from different sources such as files, clipboard, or URLs. The app provides a user-friendly interface built with the Tkinter library.

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
- dotenv: This library is used to load environment variables from the .env file.
- whisper: This library is used for audio/video transcription.
- fitz: This library is used for PDF text extraction.
- pyperclip: This library is used for clipboard interaction.

You can install the dependencies by running the following command:

```bash
pip install tkinter python-dotenv whisper pymupdf pyperclip
```

## Usage

1. Clone the repository and navigate to the project directory.
2. Create a .env file in the project directory and add your OpenAI API key:

```bash
OPENAI_API_KEY=your-api-key
```

3. Run the main.py file:

```bash
python main.py
```

4. The Summarizer App window will open.
5. Select the source type from the dropdown menu (File, Clipboard, or URL).
6. Depending on the selected source type, provide the necessary information (e.g., select a file or enter a URL).
7. Choose the destination directory where the summarized output will be saved by clicking the "Select Destination" button.
8. Select the desired summary method and language model from the respective dropdown menus.
9. Click the "Summarize" button to initiate the summarization process.
10. The summarized output will be saved in the specified destination directory.
11. To view the summarized content, click the "Open File" button in the application window.

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
