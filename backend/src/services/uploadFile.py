import shutil
from pathlib import Path
from fastapi import UploadFile, File

ROOT = Path(__file__).resolve().parent.parent.parent

uploaded_file_path = ROOT / "data" / "raw" 

async def upload_file_service(file: UploadFile = File(...)):
    # 1. Create the directories if they don't exist yet
    # parents=True creates missing nested folders; exist_ok=True prevents crashes if they already exist
    uploaded_file_path.mkdir(parents=True, exist_ok=True)
    file_path = uploaded_file_path / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path