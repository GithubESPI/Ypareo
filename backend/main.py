from dotenv import load_dotenv

load_dotenv()  # Prend les variables d'environnement à partir du fichier .env

from app.api import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
