# 🍽️ Restaurant Reservation System - Flask Frontend

Sistema web gastronómico desarrollado con **Flask** que permite administrar reservas, menú, reseñas y servicios adicionales para restaurantes, cafeterías, bares o locales de comida rápida.

---
## Participantes
- Tiziano Longo
- Pedro Osorio
- Hernan Condori
- Lucas Vera
- Facundo Nunes
- Lucas Fontana
- Agustin Tarcaya 
- Rodrigo Cuellar
- Yachak Vilcapuma

## 👨‍🍳 Frontend Público

El sitio web ofrece:

- Información del restaurante
- Galería de imágenes
- Menú con precios
- Restricciones alimenticias
- Reseñas de clientes
- Servicios extras
- Sistema de reservas online
- Diseño responsive adaptable a dispositivos móviles

---

## 📅 Sistema de Reservas

El usuario puede realizar reservas de forma rápida e intuitiva.

### Flujo de reserva

1. Selección de fecha disponible
2. Selección de horario
3. Cantidad de personas
4. Confirmación de datos
5. Envío de email automático
6. Generación de código QR

### Funcionalidades

- Validación de disponibilidad
- Generación automática de QR
- Confirmación por correo electrónico
- Botón de cancelación desde el email
- Escaneo del QR en el local

---

## 🛠️ Panel Administrador

Acceso exclusivo para administradores.

### Funciones disponibles

- Gestión completa del menú (ABM)
- Gestión de reseñas
- Gestión de servicios extras
- Administración de reservas
- Visualización de estadísticas
- Historial de reservas
- Usuarios que cancelaron reservas
- Control de ocupación

---

# 🍔 ABM Menú

Administración completa de platos:

- Crear platos
- Editar platos
- Eliminar platos
- Subir imágenes
- Categorías
- Precio
- Descripción
- Restricciones alimenticias

### Ejemplos de restricciones

- Vegano
- Vegetariano
- Sin gluten
- Sin lactosa
- Picante

---

# ⭐ ABM Reseñas

Las reseñas son publicadas únicamente por usuarios que realizaron una reserva.

### Funcionalidades

- Crear reseñas
- Aprobar/rechazar reseñas
- Eliminar reseñas
- Calificación por estrellas
- Comentarios de clientes

---

# ♿ ABM Servicios Extras

Gestión de servicios disponibles en el local:

- Acceso para discapacitados
- Playa de estacionamiento
- WiFi
- Zona fumadores
- Delivery
- Take away
- Espacios al aire libre

---

# 📊 Dashboard Administrativo

El administrador cuenta con dashboards informativos:

- Cantidad total de reservas
- Reservas activas
- Historial de reservas
- Reservas canceladas
- Usuarios frecuentes
- Estadísticas mensuales
- Horarios más solicitados
- Platos más pedidos

---

# 🧰 Tecnologías Utilizadas

## Backend
- Python
- Flask
- Flask Login
- Flask Mail

## Frontend
- HTML5
- CSS3
- Bootstrap
- JavaScript

## Base de Datos
MySQL 

## Librerías Adicionales
- QRCode
- Pillow
- WTForms

---

# 📁 Estructura del Proyecto

```bash
restaurant-app/
│
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   │
│   ├── templates/
│   │   ├── admin/
│   │   └── public/
│   │
│   ├── routes/
│   ├── services/
│   └── utils/
│
├── requirements.txt
|── LICENSE
├── .env
├── setup.sh
├── app.py
└── README.md
```

---

# ⚙️ Instalación

## 1️⃣ Clonar repositorio

```bash
git clone https://github.com/elimenit/tp3_ids_frontend.git
cd tp3_ids_frontend
```

---

## 2️⃣ Correr aplicacion

```bash
sudo bash setup.sh
```

### Activar entorno virtual

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configurar variables de entorno

Crear archivo `.env`

```env
SECRET_KEY=secretkey
MAIL_USERNAME=correo@gmail.com
MAIL_PASSWORD=password
DATABASE_URL=sqlite:///restaurant.db
```

---

## 5️⃣ Ejecutar migraciones

```bash
flask db init
flask db migrate
flask db upgrade
```

---

## 6️⃣ Ejecutar proyecto

```bash
python run.py
```

Servidor disponible en:

```bash
http://127.0.0.1:5000
```

---

# 🔐 Acceso Administrador

Ruta:

```bash
/admin
```

Funciones:

- Login seguro
- Gestión de contenido
- Dashboard administrativo
- Control de reservas

---

# 📧 Sistema de Emails

Al confirmar una reserva:

✅ Se envía un email automático  
✅ Incluye QR de la reserva  
✅ Incluye botón de cancelación  

---

# 📱 Diseño Responsive

El sistema se adapta a:

- Celulares
- Tablets
- Laptops
- Monitores desktop

---

# 🐳 Docker (Opcional)

## Construir imagen

```bash
docker build -t restaurant-app .
```

## Ejecutar contenedor

```bash
docker run -p 5000:5000 restaurant-app
```

---

# ☁️ Deploy (Opcional)

El proyecto puede desplegarse en:

- PythonAnywhere
- Render
- Railway
- Heroku
- VPS Linux

---

# ✅ Funcionalidades Mínimas Cubiertas

| Requisito | Estado |
|---|---|
| Frontend gastronómico | ✅ |
| Sistema de reservas | ✅ |
| Generación de QR | ✅ |
| Confirmación por email | ✅ |
| ABM menú | ✅ |
| ABM reseñas | ✅ |
| ABM servicios extras | ✅ |
| Dashboard administrador | ✅ |
| Estadísticas | ✅ |
| Responsive Design | ✅ |

---

# 🚀 Mejoras Futuras

- Integración con Mercado Pago
- Notificaciones WhatsApp
- Reservas en tiempo real
- Sistema de puntos/fidelización
- API REST
- Multi sucursal
- Chat online

---

Proyecto desarrollado con Flask para gestión gastronómica y reservas online.