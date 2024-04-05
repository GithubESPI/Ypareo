from flask import Flask, request, jsonify, render_template
import pandas as pd
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.route('/convert-excel', methods=['GET', 'POST'])
@cross_origin(origin='http://localhost:5173', headers=['Content-Type', 'Authorization'])
def convert_excel_to_bulletin():
    if request.method == 'POST':
        if request.is_json:
            data = request.json.get('data')
            df = pd.DataFrame(data)
            print("Données Excel reçues :\n", df)
            # Votre logique de traitement des données ici

            # Convertir les données en un format utilisable dans le template HTML
            bulletin_data = []
            for index, row in df.iterrows():
                bulletin_data.append({
                    'enseignement': row['Enseignements'],
                    'moyenne': row['Moyenne'],
                    'total_ects': row['Total ECTS'],
                    'etat': row['Etat']
                })

            # Renvoyer le template HTML avec les données
            return render_template('bulletin_template.html', data=bulletin_data)
        else:
            return jsonify({"error": "La requête ne contient pas de données JSON"}), 400
    elif request.method == 'GET':
        return jsonify({"message": "Endpoint pour la conversion Excel en bulletin"})

if __name__ == '__main__':
    app.run(debug=True)
