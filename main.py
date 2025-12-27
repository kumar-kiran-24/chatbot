import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from src.dataembedding import DataEmbedding
from src.dataingestion import Dataingestion
from src.components.ragchatbot import RagChatbot
from src.datatransformer.webdatatransfer import WebTransfer
from src.datatransformer.textdatatransfer import TextTransfer
from src.datatransformer.pdfdatatransfer import PdfTransfer
from pathlib import Path

load_dotenv()

from datetime import datetime

class Main:

    def __init__(self):
        self.ingest = Dataingestion()
        self.embeder = DataEmbedding()
        self.chatbot = RagChatbot()
        self.webbaseloader = WebTransfer()
        self.texttransefr=TextTransfer()
        self.pdf_loader=PdfTransfer()
        self.session_id=1
        self.text_loder=Dataingestion()


        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # self.DB_PATH = r"C:\GEN_AI\chatbot\embeddings"
        BASE_DIR = Path.cwd()          # current working directory
        self.DB_PATH = BASE_DIR / "embeddings"

        self.DB_PATH.mkdir(parents=True, exist_ok=True)

    def data_loader(self, documents):
        db_path=self.embeder.initiate_embedding(documents=documents)
        return db_path
    
    def load_vector(self, db_path,question):

        db=FAISS.load_local(db_path,self.embeddings,allow_dangerous_deserialization=True)
        results=db.similarity_search(question,k=4)
        return results
        



    def main_for_web(self,link,question):
        

        documnets=self.ingest.from_website(link=link)
        db_path=self.data_loader(documents=documnets)
        data=self.load_vector(db_path=db_path,question=question)
        resopnse=self.chatbot.ragchatbot(context=data,question=question,session_id=self.session_id)
        return str(resopnse)
    
    def mian_for_pdf(self,text,question):
        documnets=self.text_loder.for_pdf(text=text)
        # documnets=self.pdf_loader.transfer(pdf_path=pdf)
        db_path=self.data_loader(documents=documnets)
        data=self.load_vector(db_path=db_path,question=question)
        resopnse=self.chatbot.ragchatbot(context=data,question=question,session_id=self.session_id)
        # print(resopnse)
        return resopnse
    
    def mian_for_text(self,text_path,question):
        documnets=self.text_loder.for_pdf(text=text_path)
        db_path=self.data_loader(documents=documnets)
        data=self.load_vector(db_path=db_path,question=question)
        resopnse=self.chatbot.ragchatbot(context=data,question=question,session_id=self.session_id)
        return resopnse
    
    def reset_fuction(self):
        self.session_id+=1
        print(self.session_id)
