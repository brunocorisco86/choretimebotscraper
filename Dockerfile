FROM python:3.9-slim-buster

# Evita que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do sistema para o Chrome e Selenium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Instala o Chromium (versão otimizada para ARM/Linux em vez do Google Chrome oficial)
RUN apt-get update && apt-get install -y chromium-driver chromium

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Comando para iniciar o agendador principal
CMD ["python", "app/main.py"]
