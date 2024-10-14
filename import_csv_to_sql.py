import pyodbc

# Conectar a SQL Server
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-8FGD0OMN\SQLEXPRESS;'  # Por ejemplo, 'localhost'
    'DATABASE=tienda;'
    'UID=sa;'
    'PWD=1987;'
)

# Crear un cursor y ejecutar una consulta
cursor = conn.cursor()
cursor.execute('SELECT TOP 10 * FROM bi_ranking')

# Obtener los resultados
filas = cursor.fetchall()

for fila in filas:
    print(fila)

# Cerrar la conexión
conn.close()