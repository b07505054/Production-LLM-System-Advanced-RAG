from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class InputDocument(BaseModel):
    doc_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)
    source: Optional[str] = None

    @field_validator("doc_id", "title", "text")
    @classmethod
    def validate_not_empty(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("field must not be empty")
        return value


class IngestRequest(BaseModel):
    documents: List[InputDocument] = Field(..., min_length=1)


class IngestedChunkInfo(BaseModel):
    chunk_id: str
    doc_id: str
    title: str
    chunk_index: int
    text: str


class IngestResponse(BaseModel):
    message: str
    num_documents: int
    num_chunks: int
    chunks: List[IngestedChunkInfo]