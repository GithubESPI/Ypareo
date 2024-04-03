import React, { useCallback, useState } from 'react'
import { Button } from '../ui/button'
import { useDropzone } from "react-dropzone";
import upload from "/assets/icons/upload.svg"


const FileUploader = ({ fieldChange, mediaUrl }) => {
  const [file, setFile] = useState([]);
  const [fileUrl, setFileUrl] = useState(mediaUrl);
  
  const onDrop = useCallback(
    (acceptedFiles) => {
      setFile(acceptedFiles);
      fieldChange(acceptedFiles);
      setFileUrl(convertFileToUrl(acceptedFiles[0]));
    },
    [file]
  );


  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      "image/*": [".png", ".jpeg", ".jpg", ".svg"],
    },
  });

  return (
    <div {...getRootProps()} className="flex flex-center flex-col bg-dark rounded-xl cursor-pointer bg-grey-50">
        <input {...getInputProps()} className="cursor-pointer" />
        {fileUrl ? (
            <>
             <div className="flex flex-1 justify-center w-full p-5 lg:p-10">
             {" "}
             <img src={fileUrl} alt="image" className="file_uploader-img" />
             </div>
             <p className="file_uploader-label">
               Cliquer ou faire glisser le document
             </p>
            </>
        ): (
            <div className="file_uploader-box">
                <img src={upload} width={96} height={77} alt="file-upload" />
                <h3 className="base-medium text-light-2 mb-2 mt-2">
                    Glisser le document ici
                </h3>
                <p className="p-medium-12 mb-4">Excel</p>
                <Button className="shad-button_dark_4">
                    Sélectionner à partir de l'ordinateur
                </Button>
            </div>
        )}
    </div>
  )
}

export default FileUploader