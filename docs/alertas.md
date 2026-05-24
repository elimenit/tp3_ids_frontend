# Alertas

Para las alertas y mensajes de error se utilizó la libreria de **SweetAlert2**, la cual trae estilos personalizados, haciendo más simple todo.

## Uso
Para satisfactoriamente hacer uso de esta herramienta, decidí que al cargar cada `base.html` esté la opción en el `render_template()` de agregar parámetros `title` y `description`, los cuales son obtenidos desde el Back-End, basándome en la función `error_response`.

Por ejemplo:
```python
message=""
description=""
if not request_example.ok:
    message = data.get('mensaje', 'Error desconocido')
    description = data.get('description', 'Se ha producido un error desconocido en el servidor, intentelo de nuevo más tarde')
return render_template('mi_plantilla.html', title=message, description=description)
```

## En el Back...
En el Back-End controlamos los errores de las requests con el handler de Flask, teniendo la opción de añadir nuestros propios atributos a la excepción de manera artificial, y teniendo valores predeterminados en caso faltante.