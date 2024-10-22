FROM python:3.10-slim

# Instalar las dependencias necesarias
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    curl \
    gnupg2

# Agregar el repositorio de Microsoft para los drivers ODBC
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Instalar otros requerimientos de Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar tu aplicación
COPY . /app
WORKDIR /app

# Iniciar la aplicación Flask
CMD ["python", "app.py"]
