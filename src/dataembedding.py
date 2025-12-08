import os
from dotenv import load_dotenv
load_dotenv()
hf_token=os.getenv("HF_TOKEN")

from langchain_huggingface import HuggingFaceEmbeddings
embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

from langchain_community.vectorstores import FAISS


class DataEmbedding:

    def __init__(self):
        self.embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.save_path=r"C:\GEN_AI\chatbot\embeddings"

    def initiate_embedding(self, documents):
        db = FAISS.from_documents(documents, self.embedder)
        db.save_local(self.save_path)
        
        return self.save_path
        
    


