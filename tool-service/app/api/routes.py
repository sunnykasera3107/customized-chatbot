from fastapi import APIRouter, Request
from application.services.tool_service import ToolService

router = APIRouter()

tools_service = ToolService()

@router.post("/")
async def handle_query():
    return {'error': f"Invalid endpoint call '/'"}

@router.post("/flight_booking")
async def flight_booking(request: Request):
    data = await request.json()
    payload = data.get("payload")
    tool_class_name = data.get("tool_class")
    return tools_service.handle(tool_class_name, payload)

@router.post("/greeting")
async def greeting(request: Request):
    data = await request.json()
    payload = data.get("payload")
    tool_class_name = data.get("tool_class")
    return tools_service.handle(tool_class_name, payload)

@router.post("/weather")
async def weather(request: Request):
    data = await request.json()
    payload = data.get("payload")
    tool_class_name = data.get("tool_class")
    return tools_service.handle(tool_class_name, payload)


if __name__ == "__main__":
    pass