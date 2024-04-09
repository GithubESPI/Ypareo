from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from docx import Document
import pandas as pd
import os
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "bulletins/M1_S1/"
TEMPLATE_FILE = "modeleM1S1.docx"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_name_for_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', '', name)

def replace_in_paragraph(paragraph, placeholder, value):
    print("Avant remplacement:", paragraph.text)  # Débogage
    if placeholder in paragraph.text:
        inline = paragraph.runs
        for run in inline: print("Run:", run.text)  # Voir le contenu de chaque run
        text = ''.join([run.text for run in inline])
        if placeholder in text:
            newText = text.replace(placeholder, value)
            paragraph.clear()
            paragraph.add_run(newText)
    print("Après remplacement:", paragraph.text)  # Débogage

def process_excel_file(file_path: str, template_path: str, output_dir: str) -> list:
    try:
        df = pd.read_excel(file_path, header=4)
        print("DataFrame loaded from Excel:")  # Débogage
        print(df.head())  # Affiche les premières lignes du DataFrame pour vérifier

        bulletin_paths = []
        for _, row in df.iterrows():
            bulletin_path = generate_word_document(row, template_path, output_dir)
            bulletin_paths.append(bulletin_path)
        return bulletin_paths
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing Excel file: {e}")

def replace_placeholder(doc, placeholder, value):
    for paragraph in doc.paragraphs:
        if placeholder in paragraph.text:
            inline = paragraph.runs
            for run in inline:
                run.text = run.text.replace(placeholder, value)

def generate_word_document(data, template_path, output_dir):
    document = Document(template_path)
    student_name = clean_name_for_filename(str(data["Nom"]).strip())
    # Avant de remplacer, imprimez la valeur actuelle et la nouvelle valeur
    print(f"Replacing {{{{nomApprenant}}}} with {student_name}")  # Débogage
    replace_placeholder(document, "{{nomApprenant}}", student_name)
    # Ajoutez des impressions similaires pour chaque placeholder que vous remplacez

    output_filename = f"{student_name}_bulletin.docx"
    output_filepath = os.path.join(output_dir, output_filename)
    document.save(output_filepath)
    return output_filepath

@app.post("/upload-excel/")
async def upload_excel(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        bulletin_paths = process_excel_file(file_location, os.path.join(OUTPUT_DIR, TEMPLATE_FILE), OUTPUT_DIR)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

