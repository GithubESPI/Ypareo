import logging
import json
import os
import pandas as pd
from docxtpl import DocxTemplate
from datetime import datetime  
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def read_ects_config():
    with open(settings.ECTS_JSON_PATH, 'r') as file:
        data = json.load(file)
    return data['M1-S1'][0]

def extract_grades_and_coefficients(grade_str):
    grades_coefficients = []
    if grade_str.strip() == "":
        return grades_coefficients  # Retourner une liste vide si la chaîne est vide
    parts = grade_str.split(" - ")
    for part in parts:
        if "Absent au devoir" in part:
            continue
        if "(" in part:
            grade_part, coefficient_part = part[:-1].split("(")
            grade = grade_part.replace(",", ".").strip()
            coefficient = coefficient_part.replace(",", ".").strip()
        else:
            grade = part.replace(",", ".").strip()
            coefficient = "1.0"
        try:
            grades_coefficients.append((float(grade), float(coefficient)))
            logger.debug(f"Extracted grade: {grade}, coefficient: {coefficient}")
        except ValueError as e:
            logger.error(f"Error converting grade/coefficient to float: {e}")
            continue  # Passer à la partie suivante si une conversion échoue
    return grades_coefficients

def calculate_weighted_average(notes, ects):
    if not notes or not ects:  # Vérifier que les listes ne sont pas vides
        return 0.0
    total_grade = sum(note * ects for note, ects in zip(notes, ects))
    total_ects = sum(ects for ects in ects)
    return total_grade / total_ects if total_ects != 0 else 0

def generate_word_document(student_data, ects_values, titles_row, template_path, output_dir):
    ects_config = read_ects_config()
    group_name = student_data["Nom Groupe"]
    is_relevant_group = group_name in settings.RELEVANT_GROUPS
    logger.debug(f"Processing student: {student_data['Nom']} in group: {group_name} - Relevant: {is_relevant_group}")

    ects_values_as_int = [int(value) if pd.notna(value) else 0 for value in ects_values]
    current_date = datetime.now().strftime("%d/%m/%Y")

    # Log the loaded ECTS values from JSON for verification
    
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
        "matiere15": titles_row[59],
        # ECTS
        # Ajout des placeholders pour les ECTS
        # "ECTSUE1": ects_values_as_int[0],
        # "ECTSUE2": ects_values_as_int[1],
        # "ECTSUE3": ects_values_as_int[2],
        # "ECTSUE4": ects_values_as_int[3],
        # "ECTSUE5": ects_values_as_int[4],
        "ECTS1": ects_values_as_int[5],
        "ECTS2": ects_values_as_int[6],
        "ECTS3": ects_values_as_int[7],
        "ECTS4": ects_values_as_int[8],
        "ECTS5": ects_values_as_int[9],
        "ECTS6": ects_values_as_int[10],
        "ECTS7": ects_values_as_int[11],
        "ECTS8": ects_values_as_int[16],
        "ECTS9": ects_values_as_int[17],
        "ECTS10": ects_values_as_int[18],
        "ECTS11": ects_values_as_int[19],
    }

    all_grades_with_coefficients = []  # Pour calculer la moyenne générale à la fin
    grade_column_indices = [5, 8, 11, 17, 23, 26, 32, 35, 38, 41, 44, 47, 53, 56, 59]

    for i, col_index in enumerate(grade_column_indices, start=1):
        grade_str = str(student_data.iat[col_index]).strip() if pd.notna(student_data.iat[col_index]) else ""
        if grade_str:
            grades_coefficients = extract_grades_and_coefficients(grade_str)
            all_grades_with_coefficients.extend(grades_coefficients)
            individual_average = sum(grade * coefficient for grade, coefficient in grades_coefficients) / sum(coefficient for grade, coefficient in grades_coefficients) if grades_coefficients else 0
            placeholders[f"note{i}"] = f"{individual_average:.2f}"

    all_grades_with_coefficients = []
    # Logique pour parcourir chaque matière
    for i in range(1, 16):  # Supposons qu'il y ait 15 matières
        subject_key = f"matiere{i}"
        if subject_key in student_data and student_data[subject_key]:
            grade_str = student_data[subject_key]
            grades_coefficients = extract_grades_and_coefficients(grade_str)
            if grades_coefficients:
                individual_average = calculate_weighted_average([g[0] for g in grades_coefficients], [g[1] for g in grades_coefficients])
                ects_key = f'ECTS{i}'
                placeholders[subject_key] = f"{individual_average:.2f}"
                placeholders[ects_key] = float(ects_config.get(ects_key, 0)) if individual_average >= 8 and is_relevant_group else 0
                logger.debug(f"Processed {subject_key}: Avg = {individual_average}, ECTS = {placeholders[ects_key]}")
            else:
                placeholders[subject_key] = "N/A"  # Notation N/A pour les matières sans notes valides
                placeholders[f'ECTS{i}'] = 0
                logger.debug(f"No valid grades found for {subject_key}. Set ECTS to 0.")
        else:
            logger.debug(f"{subject_key} is missing or empty in student_data.")




    # Calculate general average
    if all_grades_with_coefficients:
        general_average = sum(grade * coefficient for grade, coefficient in all_grades_with_coefficients) / sum(coefficient for grade, coefficient in all_grades_with_coefficients)
        placeholders['moyenne'] = general_average

    # Process notes and ECTS for UEs
    for ue, (start, end) in enumerate([(1, 3), (4, 4), (5, 6), (7, 12), (13, 15)], start=1):
        notes = [float(student_data.get(f'note{i}', 0)) for i in range(start, end+1)]
        ects = [float(ects_config.get(f'ECTS{i}', 0)) for i in range(start, end+1) if is_relevant_group]
        moy_ue = calculate_weighted_average(notes, ects)
        placeholders[f'moyUE{ue}'] = f"{moy_ue:.2f}"

    doc = DocxTemplate(template_path)
    doc.render(placeholders)
    
    output_filename = f"{student_data['Nom']}_bulletin.docx"
    output_filepath = os.path.join(output_dir, output_filename)
    doc.save(output_filepath)
    return output_filepath
