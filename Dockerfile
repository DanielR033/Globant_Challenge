FROM python:3.9-slim

# Copiar los requisitos e instalarlos
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la aplicación al contenedor
COPY app /app

# Establecer el PYTHONPATH
ENV PYTHONPATH=/app

# Configurar el directorio de trabajo raíz
WORKDIR /

# Exponer el puerto de la API
EXPOSE 8000

# Comando para iniciar FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
