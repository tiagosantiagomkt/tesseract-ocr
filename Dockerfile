# Use uma imagem base do Python leve
FROM python:3.9-slim

# Instale o curl e outras dependências necessárias
RUN apt-get update && apt-get install -y \
    curl \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

# Baixe o arquivo de idioma português (por.traineddata) diretamente de um repositório confiável
RUN mkdir -p /usr/share/tesseract-ocr/5.0/tessdata && \
    curl -Lo /usr/share/tesseract-ocr/5.0/tessdata/por.traineddata \
    https://github.com/tesseract-ocr/tessdata/raw/master/por.traineddata

# Defina a variável de ambiente TESSDATA_PREFIX para o diretório correto
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5.0/

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
