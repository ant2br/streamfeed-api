# Utiliza uma imagem oficial do Python 3.12
FROM python:3.12-slim

# Cria um diretório de trabalho
WORKDIR /app

# Copia os arquivos requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Instala o Gunicorn
RUN pip install gunicorn

# Cria um usuário não-root
RUN useradd -m appuser
USER appuser

# Copia o código da aplicação para o diretório de trabalho e define a propriedade
COPY --chown=appuser:appuser . .

# Define a variável de ambiente para o FastAPI
ENV FASTAPI_ENV=production

# Expõe a porta 8000 para acesso externo
EXPOSE 8000

# Comando para rodar a aplicação com Gunicorn usando Uvicorn como worker
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--bind", "0.0.0.0:8000"]
