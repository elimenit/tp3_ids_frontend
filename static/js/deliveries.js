// static/js/deliveries.js
console.log("Deliveries JS cargado");

window.viewDetail = function(deliveryId) {
    // Ejemplo: Podrías usar SweetAlert para mostrar un detalle rápido
    Swal.fire({
        title: `Detalle del Pedido #${deliveryId}`,
        text: "Aquí podrías cargar más info vía fetch si fuera necesario.",
        icon: 'info',
        confirmButtonColor: '#ffffff71',
        background: 'rgb(43, 43, 43)',
        color: '#ffffff'
    });
}