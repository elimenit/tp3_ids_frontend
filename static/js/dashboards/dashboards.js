/**
 * disables all buttons and selects the clicked one 
 * 
 * 
 * @param {Element} clickedBtn 
 * @param {NodeList} allBtns 
 */
const selectOption = (clickedBtn, allBtns) => {
    allBtns.forEach(btn => {btn.classList.remove('active')});
    clickedBtn.classList.add('active');
    console.log(clickedBtn);
};

const graphSidebar = document.querySelector('.graphs-sidebar');
const panelList = graphSidebar.querySelector('.panel-list');
const uls = panelList.querySelectorAll('ul');

uls.forEach(ul => {
    const ulType = ul.dataset.name;
    const btns = ul.querySelectorAll('button');
    btns.forEach(btn => {
        const btnType = btn.dataset[ulType];
        btn.addEventListener('click', () => {
            selectOption(btn, btns);
             // Aquí puedes agregar la lógica para actualizar los gráficos según el área y el rango de fechas seleccionados
             console.log(`Área seleccionada: ${btnType}, Rango de fechas seleccionado: ${ulType}`);
        });
    });
});