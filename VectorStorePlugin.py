import csv
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class AnalogicalDatabase:
    def __init__(self,data_file,x_col,y_col,k=2,chunk_size=1000,gemini_model="models/embedding-001"):
        loader = CSVLoader(data_file)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        embeddings = GoogleGenerativeAIEmbeddings(model=gemini_model,task_type="retrieval_document")
        db = FAISS.from_documents(docs, embeddings)
        self.retr = db.as_retriever(search_type='similarity',search_kwargs={"k":k})
   
    def retrieve_similar_queries(self,query_text):
        docs = self.retr.get_relevant_documents(query_text)
        return docs
    
    def get_retr(self):
        return self.retr