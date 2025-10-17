import os
from pathlib import Path
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Header
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
UPLOAD_DIR = Path("attachments")
UPLOAD_DIR.mkdir(exist_ok=True)


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return x_api_key


@app.post("/upload")
async def upload_photo(
    file: UploadFile = File(...),
    filename: Optional[str] = Form(None),
    api_key: str = Header(None, alias="X-API-KEY")
):
    verify_api_key(api_key)

    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    file_extension = Path(file.filename).suffix if file.filename else ".jpg"

    if not filename:
        timestamp = int(datetime.now().timestamp())
        filename = f"photo_{timestamp}"

    final_filename = f"{filename}{file_extension}"
    file_path = UPLOAD_DIR / final_filename

    content = await file.read()
    file_size = len(content)

    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "filename": final_filename,
        "size": file_size
    }
