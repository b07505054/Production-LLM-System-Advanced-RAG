from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.api.routes_query import router as query_router
from app.api.routes_ingest import router as ingest_router
from app.api.routes_store import router as store_router
from app.api.routes_monitoring import router as monitoring_router
from app.api.routes_eval import router as eval_router
app = FastAPI(
    title="Production LLM System",
    version="0.3.0",
    description="Advanced RAG system with retrieval, reranking, evaluation, monitoring, and caching",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "production-llm-system",
        "version": "0.3.0",
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request payload",
                "details": exc.errors(),
            }
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if hasattr(exc, "detail"):
        detail = exc.detail
        if isinstance(detail, dict):
            status_code = 500
            if detail.get("code") in {"EMPTY_STORE", "NO_RELEVANT_CHUNKS"}:
                status_code = 400 if detail["code"] == "EMPTY_STORE" else 404
            return JSONResponse(status_code=status_code, content={"error": detail})

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": str(detail),
                }
            },
        )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "UNEXPECTED_ERROR",
                "message": str(exc),
            }
        },
    )


app.include_router(query_router)
app.include_router(ingest_router)
app.include_router(store_router)
app.include_router(eval_router)
app.include_router(monitoring_router)