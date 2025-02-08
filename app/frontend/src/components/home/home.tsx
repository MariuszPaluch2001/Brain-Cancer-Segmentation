import JSZip from "jszip";
import React, {FC, JSX, useEffect, useState} from "react";
import {converTifImagePost} from "../../services/convert_tif";
import {modelApiPost} from "../../services/model_api";
import DropZone from "../dropzone/dropzone";
import Gallery from "../gallery/gallery";
import "./home.css";

const Home: FC = (): JSX.Element => {
    const [zipFile, setFile] = useState<JSZip | null>(null);
    const selectorMRI = "MRI";
    const selectorMask = "Mask";
    const selectorResults = "Results";

    useEffect(() => {
        if (!!zipFile) {
            for (let filename of Object.keys(zipFile.files).sort()) {
                zipFile.files[filename].async("blob").then(async (blob) => {
                    const data = await converTifImagePost(blob);
                    if (!!data) {
                        const img = new Image();
                        img.src = URL.createObjectURL(data);
                        let selector = "#" + filename.includes("mask") ? selectorMask : selectorMRI;
                        const elem = document.querySelector(selector);
                        if (!!elem) elem.prepend(img);

                        if (selector === "#" + selectorMRI) {
                            const data = await modelApiPost(blob);
                            if (!!data) {
                                const img = new Image();
                                img.src = URL.createObjectURL(data);
                                selector = "#" + selectorResults;
                                const elem = document.querySelector(selector);
                                if (!!elem) elem.prepend(img);
                            }
                        }
                    }
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
                    <Gallery selector={selectorMRI} />
                    <Gallery selector={selectorMask} />
                    <Gallery selector={selectorResults} />
                </div>
            )}
        </div>
    );
};

export default Home;
