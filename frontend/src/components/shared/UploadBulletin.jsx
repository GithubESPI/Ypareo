import React from 'react'
import FileUploader from './FileUploader'

const UploadBulletin = () => {
  return (
    <>
        <section className="bg-primary-50 bg-cover bg-center py-5 md:py-10">
            <h3 className="wrapper h3-bold text-center text-white sm:text-left">
                Upload des bulletins
            </h3>
        </section>

        <div className="wrapper my-8">
            <FileUploader />
        </div>
    </>
  )
}

export default UploadBulletin