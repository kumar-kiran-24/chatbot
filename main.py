from src.dataingestion import Dataingestion
from src.dataembedding import DataEmbedding

import os 
from dotenv import load_dotenv
load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings

class Main:
    def __init__(self):
        self.embedding_model=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.dataingestion=Dataingestion()

    def web(self,url):
        chunks=self.dataingestion.from_website(link=url)
        return chunks
    
    def pdf(self,path):
        chunks=self.dataingestion.from_pdf(path=path)
        return chunks
    def text(self,text:str):
        chunks=self.dataingestion.for_text(text=text)
        return chunks
