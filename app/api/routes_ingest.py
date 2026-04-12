from fastapi import APIRouter, HTTPException

from app.schemas.ingest import (
    IngestRequest,
    IngestResponse,
    IngestedChunkInfo,
)
from app.ingestion.chunker import chunk_text
from app.retrieval.embedder import embedder
from app.retrieval.vector_store import vector_store


router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("", response_model=IngestResponse)
def ingest_documents(payload: IngestRequest) -> IngestResponse:
    try:
        all_chunks = []

        for doc in payload.documents:
            chunks = chunk_text(
                doc_id=doc.doc_id,
                title=doc.title,
                text=doc.text,
                chunk_size=300,
                chunk_overlap=50,
            )
            all_chunks.extend(chunks)

        if not all_chunks:
            return IngestResponse(
                message="No chunks created",
                num_documents=len(payload.documents),
                num_chunks=0,
                chunks=[],
            )

        chunk_texts = [chunk["text"] for chunk in all_chunks]
        chunk_vectors = embedder.embed_texts(chunk_texts)

        items_to_store = []
        for chunk, vector in zip(all_chunks, chunk_vectors):
            item = dict(chunk)
            item["embedding"] = vector
            items_to_store.append(item)

        vector_store.add_items(items_to_store)

        response_chunks = [
            IngestedChunkInfo(
                chunk_id=chunk["chunk_id"],
                doc_id=chunk["doc_id"],
                title=chunk["title"],
                chunk_index=chunk["chunk_index"],
                text=chunk["text"],
            )
            for chunk in all_chunks
        ]

        return IngestResponse(
            message="Documents ingested successfully",
            num_documents=len(payload.documents),
            num_chunks=len(all_chunks),
            chunks=response_chunks,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "INGEST_ERROR",
                "message": str(exc),
            },
        ) from exc