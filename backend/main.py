from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from docxtpl import DocxTemplate
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

# Récupération du répertoire du script actuel
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "bulletins/M1_S1")
TEMPLATE_FILE = os.path.join(OUTPUT_DIR, "modeleM1S1.docx")  # Chemin ajusté

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_name_for_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', '', name)

def process_excel_file(file_path: str, template_path: str, output_dir: str) -> list:
    try:
        # Load the Excel file, skipping headers for the main data as before
        df_titles = pd.read_excel(file_path, header=None)
        titles_row = df_titles.iloc[3]  # Extracting title row as before
        
        # Reload for student data, assuming headers start from row 4 (index 3 in Python)
        df_students = pd.read_excel(file_path, header=4)
        
        bulletin_paths = []
        # Iterate over each student in the DataFrame
        for index, student_row in df_students.iterrows():
            # Call the document generation function for the current student
            bulletin_path = generate_word_document(student_row, titles_row, template_path, output_dir)
            bulletin_paths.append(bulletin_path)

        return bulletin_paths
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing Excel file: {e}")

def generate_word_document(student_row, titles_row, template_path, output_dir):
    student_name = clean_name_for_filename(str(student_row["Nom"]).strip())
    
    # Define the column indices for the grades you want to extract
    grade_column_indices = [5, 8, 11, 17, 23, 26, 32, 35, 38, 41, 44, 47, 53, 56, 59]  # Updated indices

    placeholders = {
        "nomApprenant": student_name,
        "UE1_Title": titles_row[2],
        "strat": titles_row[5],
        "finance": titles_row[8],
        "economie": titles_row[11],
        "UE2_Title": titles_row[14],
        "droit": titles_row[17],
        "UE3_Title": titles_row[20],
        "ville": titles_row[23],
        "politique": titles_row[26],
        "UE4_Title": titles_row[29],
        "real": titles_row[32],
        "rencontre": titles_row[35],
        "career": titles_row[38],
        "inside": titles_row[41],
        "immersion": titles_row[44],
        "voltaire": titles_row[47],
        "UESPE_Title": titles_row[50],
        "fonciere": titles_row[53],
        "montage": titles_row[56],
        "acquisition": titles_row[59],
    }
    
    # Dynamically add the grades to the placeholders dictionary using the specific columns
    for i, col_index in enumerate(grade_column_indices, start=1):
        grade = student_row.iat[col_index]
        placeholders[f"note{i}"] = str(grade).strip() if pd.notna(grade) else ""
    
    doc = DocxTemplate(template_path)
    doc.render(placeholders)
    
    output_filename = f"{student_name}_bulletin.docx"
    output_filepath = os.path.join(output_dir, output_filename)
    doc.save(output_filepath)
    return output_filepath



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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
