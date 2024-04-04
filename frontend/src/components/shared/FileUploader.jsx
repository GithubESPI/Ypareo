import React, { useState } from 'react';
import axios from 'axios'; 
import * as XLSX from 'xlsx';
import { Input } from '../ui/input';
import upload from "/assets/icons/upload.svg";
import { Button } from '../ui/button';
import { useToast } from "@/components/ui/use-toast"


const FileUploader = () => {
  const [data, setData] = useState([]);
  const [isDataUploaded, setIsDataUploaded] = useState(false);
  const { toast } = useToast()

  const handleFileUpload = (e) => {
    const reader = new FileReader();
    reader.readAsArrayBuffer(e.target.files[0]);
    reader.onload = (e) => {
      const data = e.target.result;
      const workbook = XLSX.read(data, {type: "binary"});
      const sheetName = workbook.SheetNames[0];
      const sheet = workbook.Sheets[sheetName];
      const parsedData = XLSX.utils.sheet_to_json(sheet);
      setData(parsedData);
      setIsDataUploaded(true);
      console.log("Les données Excel ont été récupérées avec succès :", parsedData);
    }
  }

  const convertExcelToBulletin = async () => {
    try {
      const response = await axios.post('http://localhost:5000/convert-excel', { data: data }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log(response.data); // Affiche la réponse du backend
      toast({
        description: "Conversion réussi",
      })
    } catch (error) {
      toast({
        description: "échec de la conversion",
      })
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
          <Input type="file" accept=".xlsx, .xls" className="shad-button_dark_4 cursor-pointer" onChange={handleFileUpload} />
        </div>
      </div>

      <div>
        {isDataUploaded && (
          <div className="flex justify-center mt-4">
            <Button className="shad-button_dark_4" onClick={convertExcelToBulletin}>
              Convertir l'excel en bulletin
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}

export default FileUploader;
