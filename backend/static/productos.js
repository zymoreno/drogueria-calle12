const API_URL = 'http://localhost:5000/api/productos';

document.addEventListener('DOMContentLoaded', () => {
  cargarProductos();

  document.getElementById('form-producto').addEventListener('submit', async (e) => {
    e.preventDefault();

    const id = document.getElementById('producto-id').value;
    const nombre = document.getElementById('nombre').value.trim();
    const precio = parseFloat(document.getElementById('precio').value);
    const cantidad = parseInt(document.getElementById('cantidad').value);

    const data = { nombre, precio, cantidad };

    try {
      let response;
      if (id) {
        // Editar producto
        response = await fetch(`${API_URL}/${id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
      } else {
        // Agregar nuevo producto
        response = await fetch(API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
      }

      if (!response.ok) throw new Error('Error al guardar el producto.');

      alert('Producto guardado exitosamente.');
      document.getElementById('form-producto').reset();
      cargarProductos();

    

    } catch (error) {
      console.error('Error:', error);
      alert('Ocurrió un error al guardar el producto. Revisa la consola.');
    }
  });
});

function cargarProductos() {
  fetch(API_URL)
    .then(res => res.json())
    .then(data => {
      const lista = document.getElementById('lista-productos');
      lista.innerHTML = '';

      data.forEach(p => {
        const li = document.createElement('li');
        li.innerHTML = `
          ${p.nombre} - $${p.precio} (${p.cantidad} unds)
          <button onclick="editarProducto(${p.id}, '${p.nombre}', ${p.precio}, ${p.cantidad})">Editar</button>
          <button onclick="eliminarProducto(${p.id})">Eliminar</button>
        `;
        lista.appendChild(li);
      });
    })
    .catch(error => {
      console.error('Error al cargar productos:', error);
      alert('No se pudieron cargar los productos.');
    });
}

function editarProducto(id, nombre, precio, cantidad) {
  document.getElementById('producto-id').value = id;
  document.getElementById('nombre').value = nombre;
  document.getElementById('precio').value = precio;
  document.getElementById('cantidad').value = cantidad;
}

function eliminarProducto(id) {
  if (confirm('¿Estás seguro de eliminar este producto?')) {
    fetch(`${API_URL}/${id}`, { method: 'DELETE' })
      .then(() => {
        alert('Producto eliminado.');
        cargarProductos();
      })
      .catch(error => {
        console.error('Error al eliminar producto:', error);
        alert('Ocurrió un error al eliminar el producto.');
      });
  }
}
