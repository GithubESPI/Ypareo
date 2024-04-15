# api.py
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .file_processing import process_excel_file, extract_grades_and_coefficients, calculate_weighted_average_from_string, generate_word_document
from .utils import clean_name_for_filename
import os
import httpx
from starlette.responses import JSONResponse

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

base_url = os.getenv("YPAERO_BASE_URL", "https://groupe-espi.ymag.cloud/index.php")
jeton = os.getenv("YPAERO_API_TOKEN")


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
    
@app.get("/get-groupes/")
async def get_groupes():
    endpoint = "/r/v1/formation-longue/groupes"
    url = f"{base_url}{endpoint}"
    headers = {
        "X-Auth-Token": jeton,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        print(jeton)
        response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Erreur lors de l'appel API")

# Exemple d'une autre route utilisant httpx et des variables d'environnement
@app.get("/get-apprenants/")
async def get_apprenants():
    endpoint_apprenant = "/r/v1/formation-longue/apprenants?codesPeriode=2"
    url_apprenant = f"{base_url}{endpoint_apprenant}"
    headers = {
        "X-Auth-Token": jeton,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url_apprenant, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Erreur lors de l'appel API pour les apprenants")
        
@app.get("/get-absences/")
async def get_absences(date_deb: str = Query(..., regex="^\\d{2}-\\d{2}-\\d{4}$"), date_fin: str = Query(..., regex="^\\d{2}-\\d{2}-\\d{4}$")):
    endpoint = f"/r/v1/absences/{date_deb}/{date_fin}"
    url = f"{base_url}{endpoint}"
    headers = {
        "X-Auth-Token": jeton,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Erreur lors de l'appel API pour les absences")