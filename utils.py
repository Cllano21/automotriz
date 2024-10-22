import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Crear una instancia de la aplicación Dash
app = dash.Dash(__name__)

# Datos de ejemplo
df = pd.DataFrame({
    'Fruit': ['Apple', 'Orange', 'Banana', 'Grape', 'Strawberry'],
    'Amount': [10, 15, 7, 5, 12],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
})

# Crear una figura con Plotly
fig = px.bar(df, x='Fruit', y='Amount', color='City', barmode='group')

# Layout del dashboard
app.layout = html.Div(children=[
    html.H1(children='Dashboard de Ejemplo'),

    html.Div(children='''
        Ejemplo de dashboard interactivo con Python y Dash.
    '''),

    # Dropdown para seleccionar una ciudad
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': city, 'value': city} for city in df['City'].unique()],
        value='New York',  # Valor por defecto
        clearable=False
    ),

    # Gráfico de barras que se actualiza con el dropdown
    dcc.Graph(
        id='bar-graph',
        figure=fig
    )
])

# Callback para actualizar el gráfico basado en la selección del dropdown
@app.callback(
    Output('bar-graph', 'figure'),
    [Input('city-dropdown', 'value')]
)
def update_graph(selected_city):
    filtered_df = df[df['City'] == selected_city]
    fig = px.bar(filtered_df, x='Fruit', y='Amount', color='Fruit', barmode='group')
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
