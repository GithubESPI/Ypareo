import { UploadCloud, X } from "lucide-react";
import { useState } from "react";
import { useDropzone } from "react-dropzone";
import { useToast } from "../ui/use-toast";

// Define a type for the files in the state that extends the File type with a preview string
type ExtendedFile = File & {
  preview: string;
};

export default function ExcelDropzone() {
  const { toast } = useToast();
  // Initialize the state with the correct type
  const [files, setFiles] = useState<ExtendedFile[]>([]);

  const { getRootProps, getInputProps } = useDropzone({
    accept: {
      "application/vnd.ms-excel": [".xls"],
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
    },
    onDrop: (acceptedFiles) => {
      setFiles(
        acceptedFiles.map((file) =>
          Object.assign(file, {
            preview: URL.createObjectURL(file),
          })
        )
      );
      toast({
        variant: "default",
        title: "Success",
        description: "Excel files uploaded successfully.",
        duration: 5000,
      });
    },
    onDropRejected: () => {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Only Excel files are allowed.",
        duration: 5000,
      });
    },
  });

  const removeFile = (file: ExtendedFile) => {
    setFiles((curr) => curr.filter((f) => f !== file));
    URL.revokeObjectURL(file.preview);
  };

  return (
    <div>
      <div
        {...getRootProps()}
        className="bg-background h-72 lg:h-80 xl:h-96 rounded-3xl shadow-sm border-secondary border-2 border-dashed cursor-pointer flex items-center justify-center"
      >
        <input {...getInputProps()} />
        <div className="space-y-4 text-foreground">
          <div className="justify-center flex text-6xl">
            <UploadCloud width={85} height={85} />
          </div>
          <h3 className="text-center font-medium text-2xl">
            Cliquez ou déposez vos fichiers Excel ici
          </h3>
        </div>
      </div>
      {files.length > 0 && (
        <div className="mt-4 space-y-4">
          {files.map((file) => (
            <div key={file.name} className="flex items-center justify-between p-2 border rounded">
              <span>{file.name}</span>
              <button onClick={() => removeFile(file)}>
                <X />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
