import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Bulletin = () => {
  const [bulletinData, setBulletinData] = useState([]);

  useEffect(() => {
    // Effectue une requête GET vers l'endpoint Flask pour récupérer les données du bulletin
    axios.get('http://localhost:5000/convert-excel')
      .then(response => {
        setBulletinData(response.data);
      })
      .catch(error => {
        console.error('Une erreur s\'est produite lors de la récupération des données du bulletin :', error);
      });
  }, []);

  return (
    <div>
      <h1>Bulletin de notes</h1>
      <table>
        <thead>
          <tr>
            <th>Enseignements</th>
            <th>Moyenne</th>
            <th>Total ECTS</th>
            <th>Etat</th>
          </tr>
        </thead>
        <tbody>
          {bulletinData.map((item, index) => (
            <tr key={index}>
              <td>{item.enseignement}</td>
              <td>{item.moyenne}</td>
              <td>{item.total_ects}</td>
              <td>{item.etat}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Bulletin;
