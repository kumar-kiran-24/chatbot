import os
from dotenv import load_dotenv
import bs4

from langchain_core.documents import Document

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splliter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)


class Dataingestion:
    def __init__(self):
        
        pass

    def from_pdf(self,path):
        loader = PyPDFLoader(path)
        return loader.load()

    def from_website(self,link):
        webbase_loader=WebBaseLoader(web_paths=(link,))
        loader=webbase_loader.load()
        document=text_splliter.split_documents(loader)
        return document
    
    def for_text(self, text: str):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_text(text)

        documents = [
            Document(
                page_content=chunk,
                metadata={"source": "pdf"}
            )
            for chunk in chunks
        ]

        return documents
if __name__=="__main__":
    pass
