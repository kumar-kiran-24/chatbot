import os
from dotenv import load_dotenv
import bs4

from langchain_core.documents import Document


from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
text_splliter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)


class Dataingestion:
    def __init__(self):
        
        pass

    def from_pdf(self,link):
        self.link=link
        loader=PyMuPDFLoader.load(link)
        documnet=text_splliter.split_documents(loader)
        return documnet


    def from_website(self,link):
        webbase_loader=WebBaseLoader(web_paths=(link,))
        loadre=webbase_loader.load()
        document=text_splliter.split_documents(loadre)
        return document
    
    def for_pdf(self, text: str):
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
