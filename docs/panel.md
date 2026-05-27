# Panels

## Atributos
Los páneles tienen un atributo `data-openby` con el ID del botón que los abre y cierra, lo que permite utilizar un único código JS para todos los páneles. Ejemplo:
```html
<div class="panel" data-openby="configBtn">
    <h2>Settings</h2>
    ...
</div>

<!-- Y en el botón -->
<button class="config-btn" id="configBtn">
```