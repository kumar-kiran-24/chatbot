import os
os.environ["USE_TF"] = "0"

from langchain_community.document_loaders import TextLoader

class TextTransfer:
    def __init__(self):
        pass
    def transfer(self,path):
        loader=TextLoader(file_path=path)
        text_documnet=loader.load()
        return text_documnet
    