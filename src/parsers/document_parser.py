from langchain_core.documents import Document

def create_document(text: str, metadata: dict) -> Document:
    """Create a Document object from text and metadata."""
    return Document(page_content=text, metadata=metadata)
