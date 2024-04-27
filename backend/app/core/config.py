from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Upload de Bulletins"
    BASE_DIR: str = os.getcwd()
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")
    OUTPUT_DIR: str = os.path.join(BASE_DIR, "template", "S1")
    TEMPLATE_FILE: str = os.path.join(BASE_DIR, "template", "modeleM1S1.docx")
    
    # Paramètres d'API externe
    YPAERO_BASE_URL: str
    YPAERO_API_TOKEN: str

    class Config:
        # Chargez les variables d'environnement à partir d'un fichier .env situé à la racine du projet.
        env_file = ".env"

# Instanciez les paramètres pour qu'ils soient importés et utilisés dans d'autres fichiers
settings = Settings()
