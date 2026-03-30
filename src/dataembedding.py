import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from langchain_qdrant import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
load_dotenv()

hf_token=os.getenv("HF_TOKEN")

from pathlib import Path





class DataEmbedding:

    def __init__(self):
        self.embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        BASE_DIR = Path.cwd()          # current working directory
        self.save_path = Path("tmp/ embeddings")
        self.embeddings_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        self.url = os.getenv("QDRANT_URL")
        self.api_key = os.getenv("QDRANT_API_KEY")

    def initiate_embedding(self, documents):
        print("inate the embeddings")
        save_path=QdrantVectorStore.from_documents(
            documents=documents,
            embedding=self.embeddings_model,
            url=self.url,
            api_key=self.api_key,
            collection_name="chatbot",
            force_recreate=True
        )
        print("dat is embddings",save_path)
        
        return save_path
if __name__=="__main__":
    obj=DataEmbedding()
    obj.initiate_embedding(documents="my name is kiran kumar s i am the ai engineer ")

        
    


