const API_VENTAS = 'http://localhost:5000/api/ventas';

document.addEventListener('DOMContentLoaded', () => {
  cargarVentas();

  document.getElementById('form-venta').addEventListener('submit', e => {
    e.preventDefault();

    const id = document.getElementById('venta-id').value;
    const producto = document.getElementById('producto').value;
    const cantidad = parseInt(document.getElementById('cantidad').value);
    const total = parseFloat(document.getElementById('total').value);

    const data = { producto, cantidad, total };

    if (id) {
      fetch(`${API_VENTAS}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(() => {
        cargarVentas();
        document.getElementById('form-venta').reset();
      });
    } else {
      fetch(API_VENTAS, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(() => {
        cargarVentas();
        document.getElementById('form-venta').reset();
      });
    }
  });
});

function cargarVentas() {
  fetch(API_VENTAS)
    .then(res => res.json())
    .then(data => {
      const lista = document.getElementById('lista-ventas');
      lista.innerHTML = '';
      data.forEach(v => {
        const li = document.createElement('li');
        li.innerHTML = `
          ${v.producto} - ${v.cantidad} unds - Total: $${v.total}
          <button onclick="editarVenta(${v.id}, '${v.producto}', ${v.cantidad}, ${v.total})">Editar</button>
          <button onclick="eliminarVenta(${v.id})">Eliminar</button>
        `;
        lista.appendChild(li);
      });
    });
}

function editarVenta(id, producto, cantidad, total) {
  document.getElementById('venta-id').value = id;
  document.getElementById('producto').value = producto;
  document.getElementById('cantidad').value = cantidad;
  document.getElementById('total').value = total;
}

function eliminarVenta(id) {
  fetch(`${API_VENTAS}/${id}`, { method: 'DELETE' })
    .then(() => cargarVentas());
}
