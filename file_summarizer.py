import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter




class FileSummarizer:
    def __init__(self, model_var, max_tokens):
        # Load the .env file
        load_dotenv()
        self.max_tokens = int(max_tokens)
        self.llm = ChatOpenAI(temperature=0, 
                          model_name=model_var, 
                          openai_api_key=os.getenv('OPENAI_API_KEY'))
        self.one_shot_ratio = 0.75
        self.chunk_ratio = 0.1




    def summarize_file(self, full_content_path, summarization_method, path_to_save):


        with open(full_content_path, 'r') as f:
            full_content = f.read()

        num_words = len(full_content.split())
        num_tokens = self.llm.get_num_tokens(full_content)
        
        print(f"max_tokens: {self.max_tokens} ")
        print(f"Number of tokens: {num_tokens} ")
        print(f"Number of words: {num_words} ")
        print(f"Ratio: {float(num_words/num_tokens)} ")
        summarization_methods = {
            'small': {
                'Simple': self.summarize_small_simple,
                # Still use simple for small mapreduce
                'MapReduce': self.summarize_small_simple
                # Add more methods if needed
            },
            'large': {
                'Simple': self.summarize_large_simple,
                'MapReduce': self.summarize_large_map_reduce,
                # Add more methods if needed
            }
        }

        if num_tokens < int(self.max_tokens*self.one_shot_ratio):
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
        
        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size = 200,
            chunk_overlap  = 20,
            length_function = len,
        )

        texts = text_splitter.split_text(input_text)
        docs = [Document(page_content=t) for t in texts]

        prompt_template = """
        Please write a detailed summary of the following:

       {text}

       CONCISE SUMMARY: """

        PROMPT = PromptTemplate(input_variables=["text"],template=prompt_template)

        chain = load_summarize_chain(self.llm, chain_type="stuff", prompt=PROMPT)

        summary = chain.run(docs)
        return self.write_summary(summary, full_content_path, path_to_save)

    def summarize_large_simple(self, input_text, full_content_path, path_to_save):
        """
        Function to summarize large files using map-reduce method.
        :param full_content: The content of the file as a string.
        :return: The summarized content.
        """
        model_chunk_size = int(self.max_tokens/2)
        text_splitter = RecursiveCharacterTextSplitter(
            # Set a really small chunk size, just to show.
            chunk_size = model_chunk_size,
            chunk_overlap  = model_chunk_size*self.chunk_ratio,
            length_function = len,
        )

        docs = text_splitter.create_documents([input_text])

        map_prompt = """
        Write a detailed summary of the following:
        "{text}"
        """
        map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])



        combine_prompt = """
        Write a detailed summary of the following text delimited by triple backquotes.
        Return your response in a detailed outline markdown format which covers the key points of the text.
        text=```{text}```
        """
        combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])




        summary_chain = load_summarize_chain(llm=self.llm,
                                            chain_type='map_reduce',
                                            map_prompt=map_prompt_template,
                                            combine_prompt=combine_prompt_template,
                                              verbose=True
                                            )



        summary = summary_chain.run(docs)
        return self.write_summary(summary, full_content_path, path_to_save)

    def summarize_large_map_reduce(self, full_content, full_content_path, path_to_save):
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