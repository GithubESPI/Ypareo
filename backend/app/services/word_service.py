import logging
import os
import pandas as pd
from docxtpl import DocxTemplate # Assurez-vous d'implémenter cette fonction
from datetime import datetime  

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def extract_grades_and_coefficients(grade_str):
    grades_coefficients = []
    parts = grade_str.split(" - ")
    for part in parts:
        if "Absent au devoir" in part:
            continue
        if "(" in part:
            grade_part, coefficient_part = part.split("(")
            coefficient = coefficient_part.replace(")", "").replace(",", ".")
            grade = grade_part.replace(",", ".")
        else:
            grade = part.replace(",", ".")
            coefficient = "1.0"
        grades_coefficients.append((float(grade.strip()), float(coefficient.strip())))
    return grades_coefficients

def calculate_weighted_average_from_string(grade_str):
    grades_with_coefficients = extract_grades_and_coefficients(grade_str)
    total_grade = 0.0
    total_coefficient = 0.0
    for grade, coefficient in grades_with_coefficients:
        total_grade += grade * coefficient
        total_coefficient += coefficient
    return total_grade / total_coefficient if total_coefficient else 0

def generate_word_document(student_data, ects_values, titles_row, template_path, output_dir):
    ects_values_as_int = [int(value) if pd.notna(value) else "NaN" for value in ects_values] 

    # Get current date
    current_date = datetime.now().strftime("%d/%m/%Y")
    
    # Preparing the data for the placeholders
    placeholders = {
        "nomApprenant": student_data["Nom"],
        "etendugroupe": student_data["Étendu Groupe"],
        "dateNaissance": student_data["Date de Naissance"],
        "groupe": student_data["Nom Groupe"],
        "campus": student_data["Nom Site"],
        "justifiee": student_data["ABS justifiées"],
        "injustifiee": student_data["ABS injustifiées"],
        "retard": student_data["Retards"],
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
        # ECTS
        # Ajout des placeholders pour les ECTS
        "ECTSUE1": ects_values_as_int[0],
        "ECTSUE2": ects_values_as_int[1],
        "ECTSUE3": ects_values_as_int[2],
        "ECTSUE4": ects_values_as_int[3],
        "ECTSUE5": ects_values_as_int[4],
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
        "datedujour": current_date,  # Add the current date
    }

    all_grades_with_coefficients = []  # Pour calculer la moyenne générale à la fin
    grade_column_indices = [5, 8, 11, 17, 23, 26, 32, 35, 38, 41, 44, 47, 53, 56, 59]  # Assurez-vous que ces indices correspondent

    for i, col_index in enumerate(grade_column_indices, start=1):
        grade_str = str(student_data.iat[col_index]).strip() if pd.notna(student_data.iat[col_index]) else ""
        if grade_str:
            # Assurez-vous que cette fonction renvoie une liste de tuples (note, coefficient)
            grades_coefficients = extract_grades_and_coefficients(grade_str)
            all_grades_with_coefficients.extend(grades_coefficients)  # Ajoutez les tuples à la liste générale

            # Calculer et afficher la moyenne individuelle
            individual_average = sum(grade * coefficient for grade, coefficient in grades_coefficients) / sum(coefficient for grade, coefficient in grades_coefficients) if grades_coefficients else 0
            placeholders[f"note{i}"] = f"{individual_average:.2f}"

    # Calcul de la moyenne générale pour toutes les notes et coefficients collectés
    if all_grades_with_coefficients:
        general_average = sum(grade * coefficient for grade, coefficient in all_grades_with_coefficients) / sum(coefficient for grade, coefficient in all_grades_with_coefficients)
        placeholders["moyenne"] = f"{general_average:.2f}"
    else:
        placeholders["moyenne"] = ""

    # Génération du document avec les placeholders remplis
    doc = DocxTemplate(template_path)
    # Génération du document avec les placeholders remplis
    doc.render(placeholders)
    
    output_filename = f"{student_data['Nom']}_bulletin.docx"
    output_filepath = os.path.join(output_dir, output_filename)
    doc.save(output_filepath)
    return output_filepath