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

checkPasswordMatch();