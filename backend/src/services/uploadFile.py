import shutil
from pathlib import Path
from fastapi import UploadFile, File

import os
from pathlib import Path

DATA_ROOT = Path(
    os.getenv("DATA_ROOT", "/app/data")
)

DATA_DIR = DATA_ROOT / "raw"

async def upload_file_service(file: UploadFile = File(...)):
    # 1. Create the directories if they don't exist yet
    # parents=True creates missing nested folders; exist_ok=True prevents crashes if they already exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path