from typing import Optional, TypedDict

class DocMetadata(TypedDict):
    title: str
    author: str
    doc_type: str = "theory | command"
    created_at: str
    topic: Optional[str]
