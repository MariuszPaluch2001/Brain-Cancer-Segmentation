import {default as axios} from "axios";

export const apiCall = (image: any) => {
    let formData = new FormData();
    formData.append("file", image);

    return axios.post("http://127.0.0.1:5000/segmentation", formData, {
        headers: {
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Headers": "*",
            'Content-Type': 'multipart/form-data',
        },
        responseType: 'blob'
    }).then(response => {
        return response.data as Blob
     })
     .catch(error => {
        console.log(error)
     });
};
