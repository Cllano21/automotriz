import pandas as pd
import sqlalchemy

# Configurar la base de datos de Google Cloud SQL
username = 'sqlserver'
password = '1987'
server = '34.123.53.230'
port = '1433'
database = 'tienda'

# Crear la cadena de conexión
connection_string = (
    f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}"
    "?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&TrustServerCertificate=yes&Connection Timeout=30"
)

# Crear el engine
engine = sqlalchemy.create_engine(connection_string)

# Consulta para obtener los nombres de las tablas
tables_query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"

try:
    # Ejecutar la consulta y almacenar el resultado
    tables = pd.read_sql(tables_query, engine)
    print("Tablas en la base de datos:")
    print(tables)
except Exception as e:
    print("Error al ejecutar la consulta:", e)
