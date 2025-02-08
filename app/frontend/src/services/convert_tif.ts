import {default as axios} from "axios";

export const converTifImagePost = async (image: Blob) => {
    let formData = new FormData();
    formData.append("file", image);

    try {
        const response = await axios.post<Blob>("http://127.0.0.1:5000/segmentation", formData, {
            headers: {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Content-Type": "multipart/form-data",
            },
            responseType: "blob",
        });
        return response.data;
    } catch (error) {
        console.log(error);
    }
};
