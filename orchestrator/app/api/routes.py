from fastapi import APIRouter, Request
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

router = APIRouter()

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    messages: List
    file_path: Optional[str] = None


    @field_validator("query", mode="before")  # ← 'before' runs before min_length check
    @classmethod
    def strip_and_validate_query(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Query must be a string")
        stripped = value.strip()
        if len(stripped) < 2:
            raise ValueError("Query must be at least 2 characters after trimming spaces")
        return stripped


@router.post("/")
async def handle_query(request: Request, queryrequest: QueryRequest):
    body = queryrequest
    query = body.query.strip()
    messages = body.messages
    file_path = body.file_path
    orchestrator_service = request.app.state.orchestrator
    return await orchestrator_service.handle(query, messages, file_path)
    
if __name__ == "__main__":
    pass