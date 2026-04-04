from fastapi import FastAPI, Request, UploadFile, File
import uvicorn, os, shutil
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
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


app = FastAPI()
app.mount("/data/predict", StaticFiles(directory="data/predict"), name="predict")
templates = Jinja2Templates(directory="infrastructure/templates")

# Folder to save uploaded files
UPLOAD_DIR = "data/predict"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "data": {
                "image_analysis_url": os.getenv("ORCHESTRATOR_DOMAIN"), 
                "chat_url": os.getenv("ORCHESTRATOR_DOMAIN"),
                "ui_url": os.getenv("UI_DOMAIN")
            }
        }
    )


# 🔹 File Upload API
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ROOT_DIR = os.path.dirname(BASE_DIR)

        print(BASE_DIR, ROOT_DIR)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return JSONResponse(
            content={
                "message": "File uploaded successfully",
                "filename": file.filename,
                "path": os.getenv("UI_DOMAIN") + "/" + UPLOAD_DIR + "/" + file.filename
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)