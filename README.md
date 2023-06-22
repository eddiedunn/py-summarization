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

