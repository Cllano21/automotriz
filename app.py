import os
from flask import Flask, render_template, request
import pandas as pd
from sqlalchemy import create_engine
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Crear la instancia de la aplicación Flask
app = Flask(__name__)

# Configurar la base de datos
server = 'LAPTOP-8FGD0OMN\\SQLEXPRESS'
database = 'tienda'
username = 'sa'
password = '1987'
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC%20Driver%2018%20for%20SQL%20Server'
engine = create_engine(connection_string)

# Crear la instancia de la aplicación Dash
dash_app = Dash(__name__, server=app, url_base_pathname='/dash/')

# Configuración de la consulta para las compañías
query_companias = """
    SELECT DISTINCT c.expediente, c.nombre 
    FROM bi_compania c
    JOIN bi_ranking r ON c.expediente = r.expediente
    WHERE r.anio = 2023 AND r.ciiu_n4 = 'C2910'
    ORDER BY c.nombre
"""
companias = pd.read_sql(query_companias, engine)

# Layout de la aplicación Dash
dash_app.layout = html.Div([
    dcc.Dropdown(
        id='company-dropdown',
        options=[{'label': row.nombre, 'value': row.expediente} for row in companias.itertuples()],
        value=None,
        placeholder="Selecciona una compañía"
    ),
    dcc.Graph(id='graph-output'),
])

# Callback para actualizar el gráfico
@dash_app.callback(
    Output('graph-output', 'figure'),
    Input('company-dropdown', 'value')
)
def update_graph(selected_company):
    if selected_company:
        query_ranking = f"""
            SELECT anio, utilidad_ejercicio 
            FROM bi_ranking 
            WHERE expediente = '{selected_company}'
        """
        data = pd.read_sql(query_ranking, engine)
        data['utilidad_ejercicio'] = pd.to_numeric(data['utilidad_ejercicio'], errors='coerce')
        data = data.sort_values(by='anio')
        fig = px.scatter(data, x='anio', y='utilidad_ejercicio',
                         title=f'Utilidad por Año para {selected_company}',
                         labels={'anio': 'Año', 'utilidad_ejercicio': 'Utilidad del Ejercicio'})
        return fig
    else:
        return {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


