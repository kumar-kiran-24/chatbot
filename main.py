from src.dataingestion import Dataingestion
from src.dataembedding import DataEmbedding
from src.datatransformer.datasplitter import DataSplitter

import os 
from dotenv import load_dotenv
load_dotenv

from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings

class Main:
    def __init__(self):
        self.embedding_model=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.dataingestion=Dataingestion()
        self.dataembeddingd=DataEmbedding()
        self.data_splitter=DataSplitter()

    def web(self,url):
        docs=self.dataingestion.from_website(link=url)
        chunks=self.data_splitter.spliter(documnets=docs)
        path=self.dataembeddingd.initiate_embedding(documents=chunks)
        return path
    
    def pdf(self,path):
        docs=self.dataingestion.from_pdf(path=path)
        chunks=self.data_splitter.spliter(documnets=docs)
        path=self.dataembeddingd.initiate_embedding(documents=chunks)
        print("pdf convert to the embeddings ")
        return path
    def text(self,text:str):
        docs=self.dataingestion.for_text(text=text)
        chunks=self.data_splitter.spliter(documnets=docs)
        print(chunks)
        path=self.dataembeddingd.initiate_embedding(documents=chunks)
        return chunks

    def data_loader(self,question):
        load = FAISS.load_local(
            folder_path="embeddings",
            embeddings=self.embedding_model,
            allow_dangerous_deserialization=True
        )
        context=load.similarity_search(question,k=6)
        print(context)
        return context
if __name__=="__main__":
    obj=Main()
    obj.pdf(path=r"/media/kirankumars/Windows-SSD/GEN_AI/chatbot/uploads/2b11a980-a17f-4367-8d07-0565044ddf84.pdf")
    


        