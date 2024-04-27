import logging
import pandas as pd
from fastapi import HTTPException
from .word_service import generate_word_document
import os

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def process_excel_file(file_path: str, template_path: str, output_dir: str) -> list:
    try:
        logger.debug("Chargement du fichier Excel.")
        df_titles = pd.read_excel(file_path, header=None)
        titles_row = df_titles.iloc[3]
        
        df_students = pd.read_excel(file_path, header=4)
        logger.debug(f"{len(df_students)} étudiants trouvés dans le fichier.")

        bulletin_paths = []
        ects_columns = [3, 15, 21, 30, 51, 6, 9, 12, 18, 24, 27, 33, 36, 39, 42, 48, 45, 54, 57, 60]

        for index, student_data in df_students.iterrows():
            ects_values = [student_data.iloc[col] for col in ects_columns]
            bulletin_path = generate_word_document(student_data, ects_values, titles_row, template_path, output_dir)
            bulletin_paths.append(bulletin_path)
            logger.debug(f"Bulletin généré pour {student_data.get('Nom', 'N/A')}: {bulletin_path}")

        return bulletin_paths
    except Exception as e:
        logger.error("Erreur lors du traitement du fichier Excel", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Error processing Excel file: {e}")