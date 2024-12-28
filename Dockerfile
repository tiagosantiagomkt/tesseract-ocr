# Use uma imagem base do Debian slim
FROM debian:bullseye-slim

# Instale as dependências necessárias para compilar o Tesseract
RUN apt-get update && apt-get install -y \
    autoconf \
    automake \
    build-essential \
    ca-certificates \
    g++ \
    git \
    libtool \
    libleptonica-dev \
    pkg-config \
    wget \
    zlib1g-dev

# Clone o repositório oficial do Tesseract
RUN git clone https://github.com/tesseract-ocr/tesseract.git /tesseract

# Compile e instale o Tesseract a partir do código-fonte
WORKDIR /tesseract
RUN ./autogen.sh && \
    ./configure && \
    make && \
    make install && \
    ldconfig

# Configure o diretório de trabalho e copie o código da aplicação
WORKDIR /app
COPY . .

# Instale as dependências do Python
RUN apt-get install -y python3-pip && pip3 install -r requirements.txt

# Exponha a porta 5000
EXPOSE 5000

# Comando padrão para rodar a aplicação
CMD ["python3", "app.py"]
