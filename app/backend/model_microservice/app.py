import torchvision
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, request, send_file, abort
import torch
from io import BytesIO
from models.unet import UNet2D
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = UNet2D(3, 1)
model.load_state_dict(
    torch.load("models/unet.pt", weights_only=True, map_location=torch.device("cpu"))
)
model.eval()


def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(256), transforms.ToTensor()])
    image = Image.open(BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_segmentation(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    output = model(tensor)
    return output


@app.route("/segmentation", methods=["POST"])
def segmentation():
    if request.method == "POST":
        try:
            file = request.files["file"]
            img_bytes = file.read()
            output = get_segmentation(image_bytes=img_bytes)
        except Exception as e:
            print(e)
            image = Image.open("./misc/error.jpg")
            img_io = BytesIO()
            image.save(img_io, "jpeg")
            img_io.seek(0)
            return send_file(img_io, mimetype="image/jpeg")

        output[output >= 0.0] = 1
        output[output < 0.0] = 0

        output = output.squeeze(0).detach().cpu()
        image = torchvision.transforms.ToPILImage()(output)
        img_io = BytesIO()
        image.save(img_io, "PNG")
        img_io.seek(0)
        return send_file(img_io, mimetype="image/jpeg")


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return "Model microservice healthcheck"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
