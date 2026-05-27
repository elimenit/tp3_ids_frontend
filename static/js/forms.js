import { showAlert } from './alerts.js';
/*
Se asegura de que las contraseñas coincidan antes de enviar el formulario de registro. Si las contraseñas no coinciden, se muestra una alerta y se evita que el formulario se envíe.
*/
const checkPasswordMatch = () => {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const confirmPasswordInput = form.querySelector('input[name="confirm_password"]');
        const passwordInput = form.querySelector('input[name="password"]');
        if (confirmPasswordInput && passwordInput) {
            form.addEventListener('submit', (e) => {
                if (confirmPasswordInput.value !== passwordInput.value) {
                    e.preventDefault();
                    showAlert('Error', 'Las contraseñas no coinciden. Por favor, inténtalo de nuevo.', 'error');
                }
            });
        }
    });
};

const alertElimination = () => {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            showAlert(
                'Confirmación', 
                '¿Estás seguro de que deseas eliminar este usuario?', 
                'warning').then((result) => {   
                if (result.isConfirmed) {
                const form = document.getElementById(button.dataset.formid);
                    if (form) { 
                        form.submit();
                    }
                }
            });
        });
    });
};

checkPasswordMatch();
alertElimination();