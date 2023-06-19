from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate

#llm = OpenAI(temperature=0)

text_splitter = CharacterTextSplitter()

with open("TechnologicalSingularity.txt") as f:
    singularity = f.read()
texts = text_splitter.split_text(singularity)

print(f"length of texts is {len(texts)}")

# for text in texts:
#     print(text)
#     print("--------------------------------------------------------------")

