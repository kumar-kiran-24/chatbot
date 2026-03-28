import os
os.environ["USE_TF"] = "0"

from langchain_community.document_loaders import PyPDFLoader

class PdfTransfer:
    def transfer(self, pdf_path):
        loader = PyPDFLoader(pdf_path)
        return loader.load()

obj = PdfTransfer()
pages = obj.transfer(r"/media/kirankumars/Windows-SSD/GEN_AI/chatbot/uploads/2b11a980-a17f-4367-8d07-0565044ddf84.pdf")
print(pages)