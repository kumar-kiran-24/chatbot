from langchain_text_splitters import RecursiveCharacterTextSplitter

class DataSplitter:
    splitter=RecursiveCharacterTextSplitter(chunk_size=2000,
                chunk_overlap=100)
    def spliter(self,documnets):
        chunks=self.splitter.split_documents(documents=documnets)
        return chunks