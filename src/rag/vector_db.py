from abc import ABC, abstractmethod
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

# Initialize embedding function (using a small open-source model)
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize Chroma vector database

class VectorDB(ABC):
    @abstractmethod
    def add_document(self, documents: Document):
        """Add documents to the vector database."""
        pass

    @abstractmethod
    def query(self, query: str, top_k: int = 5) -> list[Document]:
        """Query the vector database and return the most relevant documents."""
        pass

    @abstractmethod
    def as_retriever(self):
        """Return a retriever object for the vector database."""
        pass
    
class ChromaVectorDB(VectorDB):
    def __init__(self, collection_name: str, embedding_function, persist_directory="./rag/vector_databases/chroma_db"):
        self.vector_db = Chroma(collection_name=collection_name, 
                                embedding_function=embedding_function,
                                persist_directory=persist_directory,
                   )

    def add_document(self, document: Document):
        """Add documents to the vector database."""
        self.vector_db.add_documents(document)

    def query(self, query: str, top_k: int = 5) -> list[Document]:
        """Query the vector database and return the most relevant documents."""
        return self.vector_db.similarity_search(query, k=top_k)
    
    def as_retriever(self):
        """Return a retriever object for the vector database."""
        return self.vector_db.as_retriever()