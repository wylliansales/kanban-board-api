# Usa uma imagem base oficial do Python
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências e instala
# Isso é feito separadamente para aproveitar o cache do Docker.
# As dependências só serão reinstaladas se o requirements.txt mudar.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta em que a aplicação Flask será executada
EXPOSE 5000

# Comando para executar a aplicação Flask.
# As variáveis de ambiente (FLASK_APP, FLASK_DEBUG, etc.) são definidas no docker-compose.yml
CMD ["flask", "run"]
