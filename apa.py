from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Crear la instancia de la aplicación Flask
app = Flask(__name__)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = r'mssql+pyodbc://sa:1987@LAPTOP-8FGD0OMN\SQLEXPRESS/tienda?driver=ODBC+Driver+17+for+SQL+Server'

db = SQLAlchemy(app)

# Definición de los modelos
class BiCompania(db.Model):
    __tablename__ = 'bi_compania'
    expediente = db.Column(db.String(50), primary_key=True)  # Clave primaria es expediente
    nombre = db.Column(db.String(255))

class BiRanking(db.Model):
    __tablename__ = 'bi_ranking'
    expediente = db.Column(db.String(50), db.ForeignKey('bi_compania.expediente'), primary_key=True)  # Usando expediente como clave primaria
    utilidad_ejercicio = db.Column(db.Integer)
    anio = db.Column(db.Integer)  # Asegúrate de incluir esta línea
    compania = db.relationship('BiCompania', backref='rankings')

# Definición de la ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    data = []  # Inicializar data aquí

    if request.method == 'POST':
        search_term = request.form['search']
        results = db.session.query(BiCompania, BiRanking).join(BiRanking, BiCompania.expediente == BiRanking.expediente)\
            .filter(BiCompania.nombre.like(f'%{search_term}%')).all()
        
        # Extraer los datos de utilidad_ejercicio y anio
        data = [(ranking.utilidad_ejercicio, ranking.anio) for compania, ranking in results]
        print(data)  # Para depuración

    return render_template('index.html', results=results, data=data)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
