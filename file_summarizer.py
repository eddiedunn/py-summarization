import os

from dotenv import load_dotenv
from langchain import OpenAI
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter




class FileSummarizer:
    def __init__(self):
        # Load the .env file
        load_dotenv()
        self.context_window_size = int(os.getenv('CONTEXT_WINDOW_SIZE'))
        self.llm = OpenAI(temperature=0, openai_api_key=os.getenv('OPENAI_API_KEY'))
        self.one_shot_ratio = 0.75




    def summarize_file(self, full_content_path, summarization_method, path_to_save):


        with open(full_content_path, 'r') as f:
            full_content = f.read()

        num_words = len(full_content.split())
        num_tokens = self.llm.get_num_tokens(full_content)
        
        print(f"Number of tokens: {num_tokens} ")
        print(f"Number of words: {num_words} ")
        print(f"Ratio: {float(num_words/num_tokens)} ")
        summarization_methods = {
            'small': {
                'Simple': self.summarize_small_simple
                # Add more methods if needed
            },
            'large': {
                'map_reduce': self.summarize_large_map_reduce,
                'method2': self.summarize_large_method2,
                # Add more methods if needed
            }
        }

        if num_tokens < int(self.context_window_size*self.one_shot_ratio):
            size_category = 'small'
        else:
            size_category = 'large'

        summarization_func = summarization_methods.get(size_category, {}).get(summarization_method)

        if summarization_func:
            return summarization_func(full_content, full_content_path, path_to_save)
        else:
            raise ValueError(f'Invalid summarization method: {summarization_method}')

    def summarize_small_simple(self, input_text, full_content_path, path_to_save):
        """
        Function to summarize small files using simple method.
        :param full_content: The content of the file as a string.
        :return: The summarized content.
        """

        text_splitter = CharacterTextSplitter()

        texts = text_splitter.split_text(input_text)
        docs = [Document(page_content=t) for t in texts]

        prompt_template = """
        Please write a concise summary of the following:

       {text}

       CONCISE SUMMARY: """

        PROMPT = PromptTemplate(input_variables=["text"],template=prompt_template)

        chain = load_summarize_chain(self.llm, chain_type="stuff", prompt=PROMPT)

        summary = chain.run(docs)
        return self.write_summary(summary, full_content_path, path_to_save)

    def summarize_large_map_reduce(self, full_content, full_content_path, path_to_save):
        """
        Function to summarize large files using map-reduce method.
        :param full_content: The content of the file as a string.
        :return: The summarized content.
        """

        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size = 100,
            chunk_overlap  = 20,
            length_function = len,
        )

        
        # TODO: Implement the map-reduce method for large file summarization.
        pass

    def summarize_large_method2(self, full_content, full_content_path, path_to_save):
        """
        Function to summarize large files using method 2.
        :param full_content: The content of the file as a string.
        :return: The summarized content.
        """
        # TODO: Implement the method2 for large file summarization.
        pass

    def write_summary(self, summary_text, full_content_path, path_to_save):
        file_to_write = os.path.splitext(os.path.basename(full_content_path))[0]
        full_output_path = os.path.join(path_to_save, file_to_write + '.summary.txt')

        with open(full_output_path, 'w') as f:
            f.write(summary_text)

        return full_output_path