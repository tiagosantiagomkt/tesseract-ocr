# Use uma imagem base do Python leve
FROM python:3.9-slim

# Atualize os pacotes do sistema e instale o Tesseract OCR e o idioma português
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Defina a variável de ambiente TESSDATA_PREFIX para o diretório correto
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/

# Instale as dependências do Python
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação
COPY . /app

# Exponha a porta 5000
EXPOSE 5000

# Comando padrão para rodar a aplicação
CMD ["python", "app.py"]

