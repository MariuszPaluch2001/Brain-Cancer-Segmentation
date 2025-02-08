from PIL import Image
from flask import Flask, request, send_file, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/convert", methods=["POST"])
def converter():
    if request.method == "POST":
        ...

@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    return "Converter microservice healthcheck"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001")
