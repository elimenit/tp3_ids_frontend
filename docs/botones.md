# Botones

## Actualización de datos
Se tomó la decisión de concentrar la administración de datos en un mismo panel, incluyendo actualización completa, parcial y/o eliminado del registro.

### Botones de eliminado
Los botones de eliminado estarán dentro del formulario general de actualización, pero con el objetivo de abrir el modal de confirmado (vease `/docs/alertas.md`) para continuar con la eliminación. 

Estos botones a su vez tendrán un atributo llamado `formid`, el cual hará referencia al formulario destino.
```html
<button class="delete-btn" data-formid="eliminarUser" type="button"></button>
...
<form id=eliminarUser method="POST" ...>
```
