from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "mi_clave_secreta_123"
CORS(app, supports_credentials=True)

db = SQLAlchemy(app)

# Modelos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    clave = db.Column(db.String(120), nullable=False)

with app.app_context():
    db.create_all()

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# ========== Autenticación ==========
@app.route('/')
@app.route('/login')
def login_view():
    return render_template('login.html')

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

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    return jsonify({'mensaje': 'Sesión cerrada.'})

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

# ========== Rutas de páginas ==========
@app.route('/dashboard')
def vista_dashboard():
    return render_template('dashboard.html')

@app.route('/productos')
def vista_productos():
    return render_template('productos.html')

@app.route('/clientes')
def vista_clientes():
    return render_template('clientes.html')

@app.route('/ventas')
def vista_ventas():
    return render_template('ventas.html')

@app.route('/usuarios')
def vista_usuarios():
    return render_template('usuarios.html')

# ========== API REST ==========
# Productos
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    productos = Producto.query.all()
    return jsonify([
        {"id": p.id, "nombre": p.nombre, "precio": p.precio, "cantidad": p.cantidad}
        for p in productos
    ])

@app.route('/api/productos', methods=['POST'])
def agregar_producto():
    data = request.json
    nuevo = Producto(nombre=data['nombre'], precio=data['precio'], cantidad=data['cantidad'])
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

# Clientes
@app.route('/api/clientes', methods=['GET'])
def obtener_clientes():
    clientes = Cliente.query.all()
    return jsonify([
        {"id": c.id, "nombre": c.nombre, "correo": c.correo, "telefono": c.telefono}
        for c in clientes
    ])

@app.route('/api/clientes', methods=['POST'])
def agregar_cliente():
    data = request.json
    nuevo = Cliente(nombre=data['nombre'], correo=data['correo'], telefono=data.get('telefono'))
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Cliente agregado correctamente."}), 201

@app.route('/api/clientes/<int:id>', methods=['PUT'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.json
    cliente.nombre = data['nombre']
    cliente.correo = data['correo']
    cliente.telefono = data.get('telefono')
    db.session.commit()
    return jsonify({"mensaje": "Cliente actualizado correctamente."})

@app.route('/api/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"mensaje": "Cliente eliminado correctamente."})

# Ventas
@app.route('/api/ventas', methods=['GET'])
def obtener_ventas():
    ventas = Venta.query.all()
    return jsonify([
        {"id": v.id, "producto": v.producto, "cantidad": v.cantidad, "total": v.total}
        for v in ventas
    ])

@app.route('/api/ventas', methods=['POST'])
def agregar_venta():
    data = request.json
    nueva = Venta(producto=data['producto'], cantidad=data['cantidad'], total=data['total'])
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Venta registrada correctamente."}), 201

@app.route('/api/ventas/<int:id>', methods=['PUT'])
def editar_venta(id):
    venta = Venta.query.get_or_404(id)
    data = request.json
    venta.producto = data['producto']
    venta.cantidad = data['cantidad']
    venta.total = data['total']
    db.session.commit()
    return jsonify({"mensaje": "Venta actualizada correctamente."})

@app.route('/api/ventas/<int:id>', methods=['DELETE'])
def eliminar_venta(id):
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()
    return jsonify({"mensaje": "Venta eliminada correctamente."})

# Usuarios
@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    resultado = [{"id": u.id, "correo": u.correo} for u in usuarios]
    return jsonify(resultado)

@app.route('/api/usuarios', methods=['POST'])
def agregar_usuario():
    data = request.json
    correo = data.get('correo')
    clave = data.get('clave')

    if not correo or not clave:
        return jsonify({'mensaje': 'Datos incompletos'}), 400

    if Usuario.query.filter_by(correo=correo).first():
        return jsonify({'mensaje': 'Correo ya registrado'}), 400

    nuevo = Usuario(correo=correo, clave=clave)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario agregado correctamente.'}), 201

@app.route('/api/usuarios/<int:id>', methods=['PUT'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    data = request.json
    usuario.correo = data['correo']
    usuario.clave = data['clave']
    db.session.commit()
    return jsonify({"mensaje": "Usuario actualizado correctamente."})

@app.route('/api/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario eliminado correctamente."})

if __name__ == '__main__':
    app.run(debug=True)
