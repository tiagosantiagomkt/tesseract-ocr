from flask import Flask, request
import pytesseract
from PIL import Image

app = Flask(__name__)

# Certifique-se de que o Tesseract está acessível no contêiner
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

@app.route("/ocr", methods=["POST"])
def ocr():
    file = request.files["image"]
    image = Image.open(file.stream)
    text = pytesseract.image_to_string(image, lang="por")
    return {"text": text}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
