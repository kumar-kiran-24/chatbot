import os
from dotenv import load_dotenv
load_dotenv()
hf_token=os.getenv("HF_TOKEN")

from langchain_huggingface import HuggingFaceEmbeddings
embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

from langchain_community.vectorstores import FAISS


class DataEmbedding:
    def __init__(self):
        
        pass
    def initiate_embedding(self,documnets):
        DB=FAISS.from_documents(documents=documnets,embedding=embeddings)
        DB.save_local(r"C:\GEN_AI\chatbot\embeddings")
        return DB


