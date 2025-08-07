// static/usuarios.js
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-usuario");
  const lista = document.getElementById("lista-usuarios");

  // Cargar usuarios
  fetch("/api/usuarios")
    .then(res => res.json())
    .then(data => {
      lista.innerHTML = "";
      data.forEach(usuario => {
        const li = document.createElement("li");
        li.textContent = `${usuario.correo}`;
        const eliminarBtn = document.createElement("button");
        eliminarBtn.textContent = "Eliminar";
        eliminarBtn.onclick = () => eliminarUsuario(usuario.id);
        li.appendChild(eliminarBtn);
        lista.appendChild(li);
      });
    });

  // Guardar usuario
  form.addEventListener("submit", e => {
    e.preventDefault();
    const id = document.getElementById("usuario-id").value;
    const correo = document.getElementById("correo").value;
    const clave = document.getElementById("clave").value;

    const url = id ? `/api/usuarios/${id}` : "/api/usuarios";
    const metodo = id ? "PUT" : "POST";

    fetch(url, {
      method: metodo,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ correo, clave })
    })
      .then(() => location.reload());
  });

  // Eliminar usuario
  function eliminarUsuario(id) {
    fetch(`/api/usuarios/${id}`, { method: "DELETE" })
      .then(() => location.reload());
  }
});
