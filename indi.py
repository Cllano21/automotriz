from sqlalchemy import create_engine, text

# Configurar la base de datos
server = 'LAPTOP-8FGD0OMN\\SQLEXPRESS'
database = 'tienda'
username = 'sa'
password = '1987'
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(connection_string)

# Crear los índices
with engine.connect() as connection:
    connection.execute(text("CREATE NONCLUSTERED INDEX idx_expediente_compania ON bi_compania(expediente);"))
    connection.execute(text("CREATE NONCLUSTERED INDEX idx_expediente_ranking ON bi_ranking(expediente);"))

print("Índices creados exitosamente.")
