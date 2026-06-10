function elegirMesa(elemento) {
    // 1. Extraemos los atributos 'data-' de la tarjeta HTML que tocó el usuario
    var idReal = elemento.getAttribute('data-id');
    var numeroMesa = elemento.getAttribute('data-number');

    // 2. Impactamos los valores en los inputs del formulario
    document.getElementById('table_id').value = idReal; // El ID oculto para el Back
    document.getElementById('table_display').value = "Mesa N° " + numeroMesa; // El texto visual

    // 3. Scroll suave hasta el bloque del formulario para comodidad del usuario
    document.querySelector('.fixed-block').scrollIntoView({ behavior: 'smooth' });
}