import JSZip from "jszip";
import React, {FC, JSX, useCallback, useMemo} from "react";
import {useDropzone} from "react-dropzone";
import {acceptStyle, activeStyle, baseStyle, rejectStyle} from "./styles";

interface Props {
    setFile: (file: JSZip) => void;
}

const DropZone: FC<Props> = (props): JSX.Element => {
    const onDrop = useCallback(
        (acceptedFiles: any) => {
            acceptedFiles.forEach(async (file: any) => {
                const data = await JSZip.loadAsync(file);
                props.setFile(data);
            });
        },
        [props]
    );

    const {getRootProps, getInputProps, isDragActive, isDragAccept, isDragReject} = useDropzone({
        onDrop,
        accept: {
            "application/zip": [".zip"],
        },
        multiple: false,
        onDragEnter: undefined,
        onDragOver: undefined,
        onDragLeave: undefined,
    });

    const style = useMemo(
        () => ({
            ...baseStyle,
            ...(isDragActive ? activeStyle : {}),
            ...(isDragAccept ? acceptStyle : {}),
            ...(isDragReject ? rejectStyle : {}),
        }),
        [isDragActive, isDragReject, isDragAccept]
    );

    return (
        <div {...getRootProps({style})}>
            <input {...getInputProps()} />
            <div>Drag and drop your images here.</div>
        </div>
    );
};

export default DropZone;
