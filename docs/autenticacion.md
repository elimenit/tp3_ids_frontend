# Autenticación

Para el manejo de sesiones de usuario se optó por el generado de tokens temporales, los cuales contienen el ID de usuario con el cual se realizarán las distintas consultas al backend.

## Flujo
```text
-> Usuario inicia sesión/registro
-> Back-end genera el token con ID de usuario 
-> Front-end guarda el token en una cookie
-> El Front-end hace las requests con el header {"Authorization": f"Bearer {token}"}
-> El Back-end valida el token y extrae el ID, generando la respuesta
```

## En la práctica
```python
# Envío las requests
auth_token = request.cookies.get('session_token')
make_request("localhost:10000", "GET", token=auth_token)
```
El token en esta función es opcional. En el caso de que sea proporcionado, entonces automáticamente se introduce en el header previamente dicho.