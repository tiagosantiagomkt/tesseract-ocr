from flask import Flask, request, jsonify
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import io
import re
import csv

app = Flask(__name__)

# Certifique-se de que o Tesseract está acessível no contêiner
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

@app.route("/ocr", methods=["POST"])
def ocr():
    try:
        # Carregar a imagem enviada
        file = request.files["image"]
        image = Image.open(file.stream)

        # Capturar parâmetros opcionais
        lang = request.form.get("lang", "por")  # Idioma padrão: Português
        psm = request.form.get("psm", "3")  # Modo padrão: Automático
        oem = request.form.get("oem", "3")  # Mecanismo padrão: LSTM OCR
        preprocess = request.form.get("preprocess", "")
        extract_fields = request.form.get("extract_fields", "false").lower() == "true"
        detect_tables = request.form.get("detect_tables", "false").lower() == "true"
        output_format = request.form.get("output_format", "text")  # text, json, csv

        # Pré-processamento de imagem, se configurado
        if preprocess == "grayscale":
            image = image.convert("L")  # Converter para escala de cinza
        elif preprocess == "contrast":
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2)  # Aumentar contraste
        elif preprocess == "sharpen":
            image = image.filter(ImageFilter.SHARPEN)  # Aplicar filtro de nitidez

        # Configuração personalizada do Tesseract
        config = f"--psm {psm} --oem {oem}"

        # Executar OCR
        raw_text = pytesseract.image_to_string(image, lang=lang, config=config)

        # Extração de campos específicos
        if extract_fields:
            extracted_fields = {
                "cpf": re.findall(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b", raw_text),
                "dates": re.findall(r"\b\d{2}/\d{2}/\d{4}\b", raw_text),
                "values": re.findall(r"\b\d+,\d{2}\b", raw_text),
            }
            return jsonify({"fields": extracted_fields})

        # Detecção de tabelas
        if detect_tables:
            config += " --psm 6"
            raw_text = pytesseract.image_to_string(image, lang=lang, config=config)
            rows = [line.split() for line in raw_text.split("\n") if line.strip()]
            return jsonify({"table": rows})

        # Formato de saída
        if output_format == "json":
            return jsonify({"text": raw_text})
        elif output_format == "csv":
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerows([line.split() for line in raw_text.split("\n")])
            output.seek(0)
            return output.getvalue(), 200, {"Content-Type": "text/csv"}
        else:
            return raw_text

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
