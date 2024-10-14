from flask import Flask, render_template_string, request
import pandas as pd
import plotly
import plotly.express as px
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mostrar_ranking():
    # Cargar el archivo CSV principal
    df_ranking = pd.read_csv('./bi_ranking.csv')
    
    # Cargar el archivo CSV secundario para obtener nombres
    df_compania = pd.read_csv('./bi_compania.csv')
    
    # Crear el ranking basado en la columna 'ingresos_ventas'
    df_ranking['ranking'] = df_ranking['ingresos_ventas'].rank(ascending=False)

    # Ordenar el DataFrame por 'ingresos_ventas' en orden descendente
    df_ranking = df_ranking.sort_values(by='ingresos_ventas', ascending=False)

    # Formatear la columna 'ingresos_ventas' para mostrar en formato decimal
    df_ranking['ingresos_ventas'] = df_ranking['ingresos_ventas'].map('${:,.2f}'.format)  # Formato de moneda con dos decimales

    # Unir ambos DataFrames usando 'expediente' como clave
    df_combined = pd.merge(df_ranking, df_compania[['expediente', 'nombre']], on='expediente', how='left')

    # Si el formulario ha enviado una búsqueda, filtrar los resultados por el nombre introducido
    if request.method == 'POST':
        nombre_busqueda = request.form.get('nombre')
        if nombre_busqueda:
            df_combined = df_combined[df_combined['nombre'].str.contains(nombre_busqueda, case=False, na=False)]
    
    # Seleccionar las primeras 20 filas con sus rankings, 'expediente', y 'nombre'
    tabla = df_combined[['anio','expediente', 'nombre', 'ingresos_ventas', 'ranking']].head(20).to_html(classes='table table-striped', index=False)
    
    # Crear el gráfico de puntos conectados con Plotly
    df_graph = df_combined.groupby('anio').sum().reset_index()  # Agrupar por año y sumar los ingresos
    df_graph = df_graph.sort_values(by='anio')  # Asegurar que esté ordenado por año de menor a mayor
    
    # Crear el gráfico de dispersión con líneas que unan los puntos
    fig = px.scatter(
        df_graph, 
        x='anio', 
        y='ingresos_ventas', 
        title='Ingresos por Año (Gráfico de Puntos Conectados)', 
        labels={'ingresos_ventas': 'Ingresos Ventas', 'anio': 'Año'}
    )
    
    # Añadir líneas que conecten los puntos
    fig.update_traces(mode='lines+markers')  # Esto añade líneas entre los puntos
    
    # Establecer el rango del eje Y para que comience desde 0
    fig.update_layout(
        yaxis=dict(range=[0, df_graph['ingresos_ventas'].max() * 1.1])  # De 0 al máximo con un 10% adicional en el eje Y
    )
    
    # Convertir el gráfico a JSON para Plotly en el frontend
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # HTML con el gráfico interactivo y la tabla
    html = f"""
    <html>
    <head>
        <title>Ranking de Ingresos</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <div class="container">
            <h1>Ranking de Ingresos por Ventas</h1>
            <form method="POST">
                <div class="form-group">
                    <label for="nombre">Buscar por nombre:</label>
                    <input type="text" class="form-control" id="nombre" name="nombre" placeholder="Ingrese un nombre">
                </div>
                <button type="submit" class="btn btn-primary">Buscar</button>
            </form>
            <h2>Gráfico de Ingresos por Año</h2>
            <div id="grafico"></div>
            <script>
                var plot_data = {graph_json};
                Plotly.newPlot('grafico', plot_data.data, plot_data.layout);
            </script>
            {tabla}
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
