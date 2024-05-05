import logging
import json
import pandas as pd
from docxtpl import DocxTemplate
from datetime import datetime
from app.core.config import settings
import os

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def read_ects_config():
    with open(settings.ECTS_JSON_PATH, 'r') as file:
        data = json.load(file)
    return data['M1-S1'][0]  # Returns the dictionary directly

def extract_grades_and_coefficients(grade_str):
    grades_coefficients = []
    if not grade_str.strip():
        return grades_coefficients  # Return empty list if string is empty
    parts = grade_str.split(" - ")
    for part in parts:
        if "Absent au devoir" in part:
            continue
        if "(" in part:
            grade_part, coefficient_part = part[:-1].split("(")
        else:
            grade_part = part
            coefficient_part = "1.0"
        grade = grade_part.replace(",", ".").strip()
        coefficient = coefficient_part.replace(",", ".").strip()
        grades_coefficients.append((float(grade), float(coefficient)))
    return grades_coefficients

def calculate_weighted_average(notes, ects):
    if not notes or not ects:
        return 0.0
    total_grade = sum(note * ects for note, ects in zip(notes, ects))
    total_ects = sum(ects)
    return total_grade / total_ects if total_ects != 0 else 0

def generate_word_document(student_data, titles_row, template_path, output_dir):
    ects_config = read_ects_config()
    current_date = datetime.now().strftime("%d/%m/%Y")
    group_name = student_data["Nom Groupe"]
    is_relevant_group = group_name in settings.RELEVANT_GROUPS
    logger.debug("Processing document for group: %s", group_name)

    placeholders = {
        "nomApprenant": student_data["Nom"],
        "etendugroupe": student_data["Étendu Groupe"],
        "dateNaissance": student_data["Date de Naissance"],
        "groupe": student_data["Nom Groupe"],
        "campus": student_data["Nom Site"],
        "justifiee": student_data["ABS justifiées"],
        "injustifiee": student_data["ABS injustifiées"],
        "retard": student_data["Retards"],
        "datedujour": current_date,
        "UE1_Title": titles_row[2],
        "matiere1": titles_row[5],
        "matiere2": titles_row[8],
        "matiere3": titles_row[11],
        "UE2_Title": titles_row[14],
        "matiere4": titles_row[17],
        "UE3_Title": titles_row[20],
        "matiere5": titles_row[23],
        "matiere6": titles_row[26],
        "UE4_Title": titles_row[29],
        "matiere7": titles_row[32],
        "matiere8": titles_row[35],
        "matiere9": titles_row[38],
        "matiere10": titles_row[41],
        "matiere11": titles_row[44],
        "matiere12": titles_row[47],
        "UESPE_Title": titles_row[50],
        "matiere13": titles_row[53],
        "matiere14": titles_row[56],
        "matiere15": titles_row[59]
    }

    grade_column_indices = [5, 8, 11, 17, 23, 26, 32, 35, 38, 41, 44, 47, 53, 56, 59]
    ects_sum_indices = {
        'ECTSUE1': [1, 2, 3],
        'ECTSUE2': [4],
        'ECTSUE3': [5, 6],
        'ECTSUE4': [7, 11],
        'ECTSUE5': [13, 14, 15]
    }

    for i, col_index in enumerate(grade_column_indices, start=1):
        grade_str = str(student_data.iat[col_index]).strip() if pd.notna(student_data.iat[col_index]) else ""
        if grade_str:
            grades_coefficients = extract_grades_and_coefficients(grade_str)
            individual_average = calculate_weighted_average([g[0] for g in grades_coefficients], [g[1] for g in grades_coefficients])
            placeholders[f"note{i}"] = f"{individual_average:.2f}" if individual_average else ""
            if individual_average >= 8 and is_relevant_group:
                ects_value = int(ects_config.get(f"ECTS{i}", 0))  # Assurez-vous que c'est un entier
                placeholders[f"ECTS{i}"] = ects_value
            else:
                placeholders[f"ECTS{i}"] = 0
        else:
            placeholders[f"note{i}"] = ""
            placeholders[f"ECTS{i}"] = 0

    # Calcul des ECTS par UE
    for ue, indices in ects_sum_indices.items():
        sum_ects = sum(int(placeholders.get(f"ECTS{i}", 0)) for i in indices)  # Conversion en entier
        placeholders[ue] = sum_ects
    
    # Calcul de la moyenne totale des ECTS
    total_ects = sum(placeholders[ue] for ue in ects_sum_indices.keys())
    placeholders['moyenneECTS'] = total_ects

    doc = DocxTemplate(template_path)
    doc.render(placeholders)
    output_filename = f"{student_data['Nom']}_bulletin.docx"
    output_filepath = os.path.join(output_dir, output_filename)
    doc.save(output_filepath)
    return output_filepath