from .vector_db import VectorDB
from llm_models.enums import EmbeddingModels
from parsers.pdf_parser import get_pdf_metadata_and_text 
from langchain_core.documents import Document
from parsers.document_parser import create_document
from schemas.metadata import DocMetadata
from datetime import datetime


class RAGPipeline:
    def __init__(self, vector_db: VectorDB, embedding_model: EmbeddingModels):
        self.vector_db = vector_db
        self.embedding_model = embedding_model
        self.retriever = self.vector_db.as_retriever()
    
    def query(self, query: str) -> str:
        """Process a query through the RAG pipeline and return the response."""
        # Step 1: Retrieve relevant documents from the vector database
        relevant_docs = self.vector_db.query(query)
        
        # Step 2: Generate a response using the LLM model based on the retrieved documents
        #TODO: Implement the logic to generate a response using the LLM model based on the retrieved documents
        
        # return response
    
    def add_document_from_file(self, file_path: str):
        """Add documents to the vector database from a list of Document objects."""
        # extension = file_path.split(".")[-1].lower()
        metadata = get_pdf_metadata_and_text
        for page_text in get_pdf_metadata_and_text(file_path):
            doc = create_document(page_text, metadata)
            self.vector_db.add_document(doc)

    def parse_docs_metadata(self,metadata):
        """Parse metadata from the document and return a dictionary."""
        # Implement your metadata parsing logic here
        parsed_metadata = DocMetadata(
            title=metadata.get("Title", "unknown"),
            author=metadata.get("Author", "unknown"),
            doc_type=metadata.get("doc_type", "theory"),
            created_at=datetime.now().strftime("%Y-%m-%d  %H:%M:%S"),  # Use current time if created_at is not available
            topic=input("Tag this document with a topic: ").lower()  # Prompt user for topic tagging
        )
        
        return parsed_metadata