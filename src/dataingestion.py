import os
from dotenv import load_dotenv
import bs4

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
    

if __name__=="__main__":
    obj=Dataingestion()
    final_documents=obj.from_website(r"https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression-and-classification")
    print(final_documents)


