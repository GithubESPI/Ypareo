# api.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .file_processing import process_excel_file, extract_grades_and_coefficients, calculate_weighted_average_from_string, generate_word_document
from .utils import clean_name_for_filename
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables de configuration (potentiellement à déplacer dans un fichier de config ou variables d'environnement)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "bulletins/M1_S1")
TEMPLATE_FILE = os.path.join(OUTPUT_DIR, "modeleM1S1.docx")


@app.post("/upload-excel/")
async def upload_excel(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        bulletin_paths = process_excel_file(file_location, TEMPLATE_FILE, OUTPUT_DIR)
        return {"filenames": bulletin_paths}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {e}")

@app.get("/download-bulletin/{student_name}")
async def download_bulletin(student_name: str):
    file_path = os.path.join(OUTPUT_DIR, f"{clean_name_for_filename(student_name)}_bulletin.docx")
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=f"{student_name}_bulletin.docx")
    else:
        raise HTTPException(status_code=404, detail="Bulletin not found")