const API_URL = 'http://localhost:5000/api/clientes';

document.addEventListener('DOMContentLoaded', () => {
  cargarClientes();

  const form = document.getElementById('form-cliente');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const id = document.getElementById('cliente-id').value;
    const nombre = document.getElementById('nombre').value.trim();
    const correo = document.getElementById('correo').value.trim();
    const telefono = document.getElementById('telefono').value.trim();

    if (!nombre || !correo || !telefono) {
      alert('Todos los campos son obligatorios.');
      return;
    }

    const data = { nombre, correo, telefono };

    try {
      let respuesta;
      if (id) {
        respuesta = await fetch(`${API_URL}/${id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        console.log(`Cliente con ID ${id} actualizado`);
      } else {
        respuesta = await fetch(API_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        console.log('Cliente nuevo agregado');
      }

      if (!respuesta.ok) {
        const error = await respuesta.json();
        alert(`Error: ${error.mensaje}`);
        return;
      }

      form.reset();
      cargarClientes();
    } catch (error) {
      console.error('Error al guardar cliente:', error);
      alert('Error al guardar cliente.');
    }
  });
});

function cargarClientes() {
  fetch(API_URL)
    .then(res => res.json())
    .then(data => {
      const lista = document.getElementById('lista-clientes');
      lista.innerHTML = '';

      data.forEach(c => {
        const li = document.createElement('li');
        li.innerHTML = `
          ${c.nombre} - ${c.correo} - ${c.telefono}
          <button onclick="editarCliente(${c.id}, '${c.nombre}', '${c.correo}', '${c.telefono}')">Editar</button>
          <button onclick="eliminarCliente(${c.id})">Eliminar</button>
        `;
        lista.appendChild(li);
      });
    })
    .catch(error => {
      console.error('Error al cargar clientes:', error);
      alert('Error al cargar clientes.');
    });
}

function editarCliente(id, nombre, correo, telefono) {
  document.getElementById('cliente-id').value = id;
  document.getElementById('nombre').value = nombre;
  document.getElementById('correo').value = correo;
  document.getElementById('telefono').value = telefono;
}

function eliminarCliente(id) {
  if (!confirm('¿Seguro que deseas eliminar este cliente?')) return;

  fetch(`${API_URL}/${id}`, { method: 'DELETE' })
    .then(() => {
      console.log(`Cliente con ID ${id} eliminado`);
      cargarClientes();
    })
    .catch(error => {
      console.error('Error al eliminar cliente:', error);
      alert('No se pudo eliminar el cliente.');
    });
}
