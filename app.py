from flask import Flask, request, jsonify
import pytesseract
from PIL import Image

app = Flask(__name__)

# Certifique-se de que o Tesseract está acessível no contêiner
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

@app.route("/ocr", methods=["POST"])
def ocr():
    try:
        # Recebe a imagem do formulário
        file = request.files["image"]
        # Abre a imagem
        image = Image.open(file.stream)
        # Realiza o OCR com o idioma português
        text = pytesseract.image_to_string(image, lang="por")
        # Retorna o texto extraído
        return jsonify({"text": text}), 200
    except Exception as e:
        # Caso ocorra algum erro, retorna uma mensagem de erro
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

