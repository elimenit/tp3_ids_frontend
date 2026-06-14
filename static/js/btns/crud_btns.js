const modal = document.querySelector('[data-openby="adminUser"]');
const overlay = document.querySelector('.overlay');
const form = document.getElementById('form-principal');
const deleteForm = document.getElementById('eliminarUser');
const addBtn = document.getElementById('add-btn');
const submitBtn = document.querySelector('.submit-btn[type="submit"]');
const deleteBtn = document.querySelector('.delete-btn');
const title = document.querySelector('.signup').querySelector('.block-header').querySelector('h2');

const openModal = () => {
    modal.classList.add('open');
    overlay.classList.add('active');
};

const closeModal = () => {
    modal.classList.remove('open');
    overlay.classList.remove('active');
};

const fillForm = ({ userid, username, email, category }) => {
    document.getElementById('username').value = username || '';
    document.getElementById('email').value = email || '';
    document.getElementById('category').value = category || 'normal';

    if (userid) {
        form.action = `/admin/users/update/${userid}`;
        deleteForm.action = `/admin/users/toggle_status/${userid}`;
    }
};

document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        deleteBtn.hidden = false;
        submitBtn.textContent = 'Actualizar usuario';
        title.textContent = 'Actualizar usuario';
        fillForm(btn.dataset);
        openModal();
    });
});

addBtn.addEventListener('click', () => {
    deleteBtn.hidden = true;
    submitBtn.textContent = 'Crear usuario';
    title.textContent = 'Crear usuario';
    form.reset();
    form.action = '/admin/users/create';
    openModal();
});

document.getElementById('closeAdminUser')?.addEventListener('click', closeModal);
overlay.addEventListener('click', closeModal);