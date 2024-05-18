# Dockerfile.app
FROM python:3.10

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . .

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Comando para iniciar la aplicación con impresión de la URL
CMD ["sh", "-c", "echo 'Running migrations...' && sleep 10 && alembic upgrade head && echo 'Migrations complete!' && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]

# Expone el puerto 8000 si es necesario
EXPOSE 8000
