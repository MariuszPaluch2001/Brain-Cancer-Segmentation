import JSZip from "jszip";
import React, {FC, JSX, useEffect, useState} from "react";
import {converTifImagePost} from "../../services/convert_tif";
import {modelApiPost} from "../../services/model_api";
import DropZone from "../dropzone/dropzone";
import "./home.css";

const Home: FC = (): JSX.Element => {
    const [zipFile, setFile] = useState<JSZip | null>(null);
    const [urls, setUrls] = useState<any[]>([]);

    const maskCancerShow = async () => {
        if (!!zipFile) {
            const buff_urls: any[] = [];
            for (let filename of Object.keys(zipFile.files).sort()) {
                if (zipFile.files[filename].dir) {
                    continue;
                }
                const blob = await zipFile.files[filename].async("blob");
                const data = await converTifImagePost(blob);
                if (!!data) {
                    const img_url = URL.createObjectURL(data);

                    if (!filename.includes("mask")) {
                        const data = await modelApiPost(blob);
                        if (!!data) {
                            const result_url = URL.createObjectURL(data);
                            buff_urls.push({
                                filename: filename.substring(0, filename.length - 4),
                                img: img_url,
                                result: result_url,
                            });
                        }
                    } else {
                        const maskName = filename.substring(0, filename.length - 9);
                        const obj = buff_urls.find((x) => x.filename === maskName);
                        obj["mask"] = img_url;
                    }
                }
            }
            setUrls(buff_urls);
        }
    };
    useEffect(() => {
        maskCancerShow();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [zipFile]);

    return (
        <div className="header">
            <DropZone {...{setFile: setFile}} />

            <div>
                <hr />
                {!!urls &&
                    urls.map((obj, index) => {
                        return (
                            <div>
                                <h5>{obj.filename}</h5>
                                <div key={index} className="float-container">
                                    <div className="float-child">
                                        <img src={obj.img} alt={obj.img} />
                                        <p>Image</p>
                                    </div>
                                    <div className="float-child">
                                        <img src={obj.mask} alt={obj.mask} />
                                        <p>Mask</p>
                                    </div>
                                    <div className="float-child">
                                        <img src={obj.result} alt={obj.result} />
                                        <p>Result</p>
                                    </div>
                                </div>
                                <hr />
                            </div>
                        );
                    })}
            </div>
        </div>
    );
};

export default Home;
