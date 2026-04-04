from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from application.services.extractor_service import ExtractorService

router = APIRouter()

@router.post("/")
async def handle_query(request: Request):
    body = await request.json()
    extractor_service = ExtractorService()
    response = extractor_service.handle(body["query"])
    return {'response': response }

if __name__ == "__main__":
    pass