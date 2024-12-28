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
