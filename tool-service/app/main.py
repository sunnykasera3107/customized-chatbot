import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import TransportSecuritySettings
from application.services.tool_service import ToolService
import logging, os

def setup_logging():
    if os.getenv("DEBUG_ENABLED", "false").lower() == "true":
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(
            level=logging.WARNING,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

# 🔥 Call this ONCE at startup
setup_logging()

mcp_server = FastMCP(
    "Tools services",
    host="0.0.0.0",
    json_response=True,
    stateless_http=True,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False
    )
)

class CustomTools:
    def __init__(self):
        self._tool_service = ToolService()

    def register(self):
        @mcp_server.tool()
        def add_numbers(numbers: list[int | float]) -> float:
            return sum(numbers)
        
        @mcp_server.tool()
        def subtract_numbers(numbers: list[int | float]) -> float:
            if len(numbers) < 2:
                return numbers if not len(numbers) == 0 else 0
            result = numbers[0]
            for x in numbers[1:]:
                result -= x
            return result
        
        @mcp_server.tool()
        def plant_disease_detector(image_path: str) -> dict:
            disease_class = self._tool_service.handle("plant_disease_detector", image_path)
            return {
                "Disease": disease_class,
            }


# Instantiate and register
math_tools = CustomTools()
math_tools.register()

app = mcp_server.streamable_http_app()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)