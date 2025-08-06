from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "mi_clave_secreta_123"
CORS(app, supports_credentials=True)

db = SQLAlchemy(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)


# Modelo Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    clave = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.route('/registro', methods=['POST'])
def registro():
    data = request.json
    correo = data['correo']
    clave = data['clave']
    if not validar_email(correo):
        return jsonify({'mensaje': 'Correo no válido.'}), 400
    if not clave or len(clave) < 6:
        return jsonify({'mensaje': 'La contraseña debe tener al menos 6 caracteres.'}), 400
    if Usuario.query.filter_by(correo=correo).first():
        return jsonify({'mensaje': 'Correo ya registrado.'}), 400
    nuevo_usuario = Usuario(correo=correo, clave=clave)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Registro exitoso.'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    correo = data['correo']
    clave = data['clave']
    usuario = Usuario.query.filter_by(correo=correo, clave=clave).first()
    if usuario:
        session['usuario'] = usuario.correo
        return jsonify({'mensaje': '¡Bienvenido!'})
    else:
        return jsonify({'mensaje': 'Credenciales incorrectas.'}), 401

@app.route('/protegido', methods=['GET'])
def protegido():
    if 'usuario' in session:
        return jsonify({'mensaje': f'Acceso permitido para {session["usuario"]}.'})
    else:
        return jsonify({'mensaje': 'No autorizado.'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    return jsonify({'mensaje': 'Sesión cerrada.'})

# ===========================
# CRUD PRODUCTOS
# ===========================

@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    resultado = [
        {"id": p.id, "nombre": p.nombre, "precio": p.precio, "cantidad": p.cantidad}
        for p in productos
    ]
    return jsonify(resultado)

@app.route('/api/productos', methods=['POST'])
def agregar_producto():
    data = request.json
    nuevo = Producto(
        nombre=data['nombre'],
        precio=data['precio'],
        cantidad=data['cantidad']
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Producto agregado correctamente."}), 201

@app.route('/api/productos/<int:id>', methods=['PUT'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    data = request.json
    producto.nombre = data['nombre']
    producto.precio = data['precio']
    producto.cantidad = data['cantidad']
    db.session.commit()
    return jsonify({"mensaje": "Producto actualizado correctamente."})

@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return jsonify({"mensaje": "Producto eliminado correctamente."})



if __name__ == '__main__':
    app.run(debug=True)
