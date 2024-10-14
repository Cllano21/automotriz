import pandas as pd

# Leer el archivo CSV
file_path = './bi_ranking.csv'
data = pd.read_csv(file_path)

# Intentar convertir la columna 'ingresos_ventas' a números, los errores se convierten en NaN
data['ingresos_ventas_numeric'] = pd.to_numeric(data['ingresos_ventas'], errors='coerce')

# Filtrar los valores que no son numéricos (NaN en la columna 'ingresos_ventas_numeric')
valores_no_numericos = data[data['ingresos_ventas_numeric'].isna()]

# Mostrar los registros con valores no numéricos en 'ingresos_ventas'
if not valores_no_numericos.empty:
    print("Registros con valores no numéricos en 'ingresos_ventas':")
    print(valores_no_numericos[['ingresos_ventas']])
else:
    print("No se encontraron valores no numéricos en 'ingresos_ventas'.")