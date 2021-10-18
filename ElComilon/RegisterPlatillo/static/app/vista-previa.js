const nombre = document.getElementById('Nombre');
const ingredientes = document.getElementById('Ingredientes');
const valor = document.getElementById('Valor');

const previaNombre = document.getElementById('previaNombre');
const previaIngredientes = document.getElementById('previaIngredientes');
const previaValor = document.getElementById('previaValor');


nombre.addEventListener('input', updateNombre);
ingredientes.addEventListener('input', updateIngredientes);
valor.addEventListener('input', updateValor);


function updateNombre(e) {
    previaNombre.textContent = e.target.value;
}
function updateIngredientes(e) {
    previaIngredientes.textContent = e.target.value;
}
function updateValor(e) {
    previaValor.textContent = e.target.value;
}


