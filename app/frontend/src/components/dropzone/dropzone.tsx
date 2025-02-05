import React, {FC, JSX, useCallback, useMemo} from 'react'
import {useDropzone} from 'react-dropzone'

interface Props {
  setFile: (file: FileReader) => void
}


const baseStyle = {
  display: 'flex',
  alignItems: 'center',
  padding: '20px',
  borderWidth: 2,
  borderRadius: 2,
  borderColor: '#ffffff',
  borderStyle: 'dashed',
  justifyContent: 'center',
  color: '#bdbdbd',
  transition: 'border .3s ease-in-out',
  marginLeft: "20%",
  marginRight: "20%"
};

const activeStyle = {
  borderColor: '#2196f3'
};

const acceptStyle = {
  borderColor: '#00e676'
};

const rejectStyle = {
  borderColor: '#ff1744'
};

const DropZone: FC<Props> = (props): JSX.Element => {
  const onDrop = useCallback((acceptedFiles: any) => {
    acceptedFiles.forEach((file: any) => {
        const reader = new FileReader()

        reader.onabort = () => console.log('file reading was aborted')
        reader.onerror = () => console.log('file reading has failed')
        props.setFile(file);

        reader.onload = () => {
          reader.readAsArrayBuffer(file);
          props.setFile(reader);
      }
    });
  }, [])

  const {
    getRootProps,
    getInputProps,
    isDragActive,
    isDragAccept,
    isDragReject
  } = useDropzone({
    onDrop,
    accept: {
      'application/zip': ['.zip'],
    },
    multiple: false,
    onDragEnter: undefined,
    onDragOver: undefined,
    onDragLeave: undefined,
  });

  const style = useMemo(() => ({
    ...baseStyle,
    ...(isDragActive ? activeStyle : {}),
    ...(isDragAccept ? acceptStyle : {}),
    ...(isDragReject ? rejectStyle : {})
  }), [
    isDragActive,
    isDragReject,
    isDragAccept
  ]);


  return (
    <div {...getRootProps({style})}>
      <input {...getInputProps()} />
      <div>Drag and drop your images here.</div>
    </div>
  )
};

export default DropZone;