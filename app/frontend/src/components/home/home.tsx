import React, {useEffect, useState} from "react";
import DropZone from "../dropzone/dropzone";
import "./home.css";
import Gallery from "../gallery/gallery";
import JSZip from "jszip";

function Home() {
    const [zipFile, setFile] = useState<JSZip | null>(null);

    useEffect(() => {
        if (!!zipFile) {
            for (let filename of Object.keys(zipFile.files).sort()) {
                zipFile.files[filename].async("blob").then((blob) => {
                    const img = new Image();
                    img.src = URL.createObjectURL(blob);
                    let selector = filename.includes("mask") ? "#Mask" : "#MRI";
                    const elem = document.querySelector(selector);
                    if (!!elem) elem.prepend(img);
                });
            }
        }
    }, [zipFile]);

    return (
        <div className="header">
            {!zipFile ? (
                <DropZone {...{setFile: setFile}} />
            ) : (
                <div>
                    <Gallery selector="MRI" />
                    <Gallery selector="Mask" />
                    <Gallery selector="Results" />
                </div>
            )}
        </div>
    );
}

export default Home;
