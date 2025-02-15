from PIL import Image
from flask import Flask, request, send_file, abort
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app)


@app.route("/convert", methods=["POST"])
def converter():
    if request.method == "POST":
        try:
            file = request.files["file"]
            img_bytes = file.read()
            im = Image.open(BytesIO(img_bytes))
            out = im.convert("RGB")
            img_io = BytesIO()
            out.save(img_io, "jpeg")
            img_io.seek(0)
            return send_file(img_io, mimetype="image/jpeg")
        except Exception as e:
            print(e)
            image = Image.open("./misc/error.jpg")
            img_io = BytesIO()
            image.save(img_io, "jpeg")
            img_io.seek(0)
            return send_file(img_io, mimetype="image/jpeg")


@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return "Converter microservice healthcheck"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001")
