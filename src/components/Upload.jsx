import React, { useState } from 'react'
import Dropzone from 'react-dropzone'

const Upload = () => {
  const [fileUrl, setFileUrl] = useState();
  return (
    <section>
        <h1>Upload vos fichiers</h1>
        <div className="flex flex-center flex-col bg-zinc-200 rounded-xl cursor-pointer">
            <input className='cursor-pointer' />
            {fileUrl ? (
             <>
                <div className="flex flex-1 justify-center w-full p-5 lg:p-10">
                    {" "}
                    <img src={fileUrl} alt="excel" />
                </div>
                <p>
                    Cliquez ou faire glisser le document à remplacer
                </p>
             </>
            ) : (
                <div>
                    <img src="src/assets/icons/file-up.svg" alt="file-upload" width={96} height={77} />
                    <h3 className="base-medium text-light-2 mb-2 mt-6">Glisser le document ici</h3>
                    <p className="text-light-4 small-regular mb-6">Excel</p>

                    <button>Séléctionner à partir de l'ordinateur</button>
                </div>
            )}
        </div>
    </section>
  )
}

export default Upload