from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from api import routes
from application.services.orchestrator_service import OrchestratorService
from infrastructure.clients.http_client import HttpClient
from fastapi.middleware.cors import CORSMiddleware
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Startup
    httpclient = HttpClient()
    orchestrator = OrchestratorService('infrastructure/data/tools_registry.json', httpclient)
    app.state.orchestrator = orchestrator

    yield

    # 🔹 Shutdown
    await orchestrator._close_()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)