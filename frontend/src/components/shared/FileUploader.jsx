import React, { useState } from 'react';
import axios from 'axios'; 
import * as XLSX from 'xlsx';
import { Input } from '../ui/input';
import upload from "/assets/icons/upload.svg";
import { Button } from '../ui/button';
import { useToast } from "@/components/ui/use-toast"


const FileUploader = () => {
  const [file, setFile] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/upload-excel/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Fichier uploadé et converti avec succès');
    } catch (error) {
      console.error('Erreur lors de l\'upload du fichier : ', error);
      alert('Erreur lors de l\'upload du fichier');
    }
  };
  
  return (
    <div>
      <div className="flex flex-center flex-col bg-dark rounded-xl cursor-pointer bg-grey-50">
        <div className="file_uploader-box">
          <img src={upload} width={96} height={77} alt="file-upload" />
          <h3 className="base-medium text-light-2 mb-2 mt-2">
            Mettre le document ici
          </h3>
          <p className="p-medium-12 mb-4">Excel</p>
          <Input type="file" accept=".xlsx, .xls" className="shad-button_dark_4 cursor-pointer" onChange={handleFileChange} />
        </div>
      </div>

      <div>
        <div className="flex justify-center mt-4">
          <Button className="shad-button_dark_4" onClick={handleUpload}>
            Convertir l'excel en bulletin
          </Button>
        </div>
      </div>
    </div>
  )
}

export default FileUploader;
