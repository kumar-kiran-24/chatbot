import os
os.environ["USE_TF"] = "0"

from langchain_community.document_loaders import PyPDFLoader

class PdfTransfer:
    def transfer(self, pdf_path):
        loader = PyPDFLoader(pdf_path)
        return loader.load()

# obj = PdfTransfer()
# pages = obj.transfer(r"C:\Users\kiran\Downloads\Project_Objectives_and_Overview.pdf")
# print(pages)