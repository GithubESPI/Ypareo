from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Upload de Bulletins"
    BASE_DIR: str = os.getcwd()
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")
    OUTPUT_DIR: str = os.path.join(BASE_DIR, "template", "S1")
    TEMPLATE_FILE: str = os.path.join(BASE_DIR, "template", "modeleM1S1.docx")
    ECTS_JSON_PATH: str = os.path.join(BASE_DIR, "json", "ects.json")  # Ajout du chemin JSON
    RELEVANT_GROUPS: list = [
        "N-M1 MAPI ALT 1", "P-M1 MAPI ALT 2", "L-M1 MAPI ALT 2", "MP-M1 MAPI ALT", 
        "P-M1 MAPI ALT 5", "L-M1 MAPI ALT 1", "P-M1 MAPI ALT 1", "P-M1 MAPI ALT 3", 
        "B-M1 MAPI ALT 1", "M-M1 MAPI ALT 1", "LI-M1 MAPI ALT", "N-M1 MAPI ALT 2", 
        "M-M1 MAPI ALT 2", "P-M1 MAPI ALT 4", "B-M1 MAPI ALT 2", "MP-M1 MAPI ALT", 
        "L-M1 MAPI ALT 3", "P-M1 MAGI ALT 1", "N-M1 MAGI ALT", "M-M1 MAGI ALT", 
        "LI-M1 MAGI ALT", "B-M1 MAGI ALT", "MP-M1 MAGI ALT", "L-M1 MAGI ALT", 
        "P-M1 MAGI ALT 2", "LI-M1 MAGI ALT", "P-M1 MAGI ALT 2", "M-M1 MIFIM ALT", 
        "N-M1 MIFIM ALT", "P-M1 MIFIM ALT 1", "P-M1 MIFIM ALT 2", "P-M1 MIFIM ALT 3", 
        "LI-M1 MIFIM ALT", "B-M1 MIFIM ALT", "MP-M1 MIFIM ALT", "L-M1 MIFIM ALT"
    ]

    # Paramètres d'API externe
    YPAERO_BASE_URL: str
    YPAERO_API_TOKEN: str

    class Config:
        # Chargez les variables d'environnement à partir d'un fichier .env situé à la racine du projet.
        env_file = ".env"

# Instanciez les paramètres pour qu'ils soient importés et utilisés dans d'autres fichiers
settings = Settings()

