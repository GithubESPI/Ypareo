from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/convert-excel', methods=['POST'])
def convert_excel_to_bulletin():
    # Vérifie si la requête contient des données JSON
    if request.is_json:
        # Récupère les données JSON envoyées par le frontend
        data = request.json.get('data')

        # Convertit les données JSON en DataFrame Pandas
        df = pd.DataFrame(data)

        # Affiche les données dans la console pour le débogage
        print("Données Excel reçues :\n", df)

        # Votre logique de traitement des données ici

        return jsonify({"message": "Données Excel reçues avec succès"})
    else:
        # Si la requête ne contient pas de données JSON, renvoie une erreur
        return jsonify({"error": "La requête ne contient pas de données JSON"}), 400

if __name__ == '__main__':
    app.run(debug=True)
