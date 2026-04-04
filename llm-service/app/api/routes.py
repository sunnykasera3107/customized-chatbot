from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from application.services.llm_service import LLMService

router = APIRouter()

@router.post("/")
async def handle_query(request: Request):
    body = await request.json()
    llm_service = LLMService()
    return await llm_service.handle(body['query'], body['messages'])
    
if __name__ == "__main__":
    pass