import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class FileSummarizer:
    def __init__(self):
        self.small_threshold = int(os.getenv('SMALL_THRESHOLD'))
        self.medium_threshold = int(os.getenv('MEDIUM_THRESHOLD'))

    def summarize_file(self, full_content_path, summarization_method):
        file_size = os.path.getsize(full_content_path)

        with open(full_content_path, 'r') as f:
            full_content = f.read()

        print(full_content)
        summarization_methods = {
            'small': {
                'method1': summarize_small_method1,
                'method2': summarize_small_method2,
                # Add more methods if needed
            },
            'medium': {
                'method1': summarize_medium_method1,
                'method2': summarize_medium_method2,
                # Add more methods if needed
            },
            'large': {
                'method1': summarize_large_method1,
                'method2': summarize_large_method2,
                # Add more methods if needed
            }
        }

        if file_size < self.small_threshold:
            size_category = 'small'
        elif self.small_threshold <= file_size < self.medium_threshold:
            size_category = 'medium'
        else:
            size_category = 'large'

        summarization_func = summarization_methods.get(size_category, {}).get(summarization_method)

        if summarization_func:
            return summarization_func(full_content)
        else:
            raise ValueError(f'Invalid summarization method: {summarization_method}')
