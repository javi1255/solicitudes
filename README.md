# Plataforma de Control de Solicitudes

## Objetivo del sistema
Desarrollar una plataforma web para la gestión de solicitudes dirigida a un asistente de un político. La plataforma permitirá registrar, visualizar y dar seguimiento a las solicitudes ciudadanas, con un sistema de autenticación básico para el usuario administrador.

## Requerimientos del sistema

### 1. Autenticación de usuario
Implementar un sistema de autenticación con un único usuario:
- Usuario: admin
- Contraseña: 12345

La autenticación deberá ser segura, utilizando hashing para almacenar la contraseña. Una vez autenticado, el usuario podrá acceder al panel de control de solicitudes.

### 2. Registro y gestión de solicitudes
Cada solicitud deberá contener la siguiente información:
- Fecha de solicitud (formato DD/MM/AAAA HH:MM)
- Datos del solicitante: Nombre completo, teléfono y correo electrónico.
- Descripción de la solicitud
- Estatus: Pendiente, En proceso, Resuelta.
- Contador de días sin resolver
  - Se calculará automáticamente desde la fecha de registro hasta la fecha actual.
  - Se representará con un código de colores:
    - 🟢 Verde: 0 a 5 días
    - 🟡 Amarillo: 6 a 10 días
    - 🔴 Rojo: 11 a 15 días

#### Filtro de búsqueda y ordenamiento
- Buscar por nombre del solicitante, estatus o fecha.
- Ordenar por fecha de generación de la solicitud.

### 3. Panel de administración
- Visualización de todas las solicitudes en una tabla ordenada por fecha de creación.
- Botón para cambiar el estatus de la solicitud.
- Generación de reportes con posibilidad de exportar a PDF o Excel.

### 4. Diseño y estilo
- El diseño de la plataforma deberá estar basado en colores verdes, representando al Partido Verde Ecologista de México (PVEM).
- La interfaz debe ser simple, intuitiva y responsiva.
- Uso de Bootstrap o Tailwind CSS para mejorar la apariencia.

### 5. Tecnologías a utilizar
- Backend: Python (Flask o Django)
- Base de datos: SQLite o PostgreSQL
- Frontend: HTML, CSS, JavaScript (opcionalmente con algún framework como React o Vue.js)
- Seguridad: Implementar hashing de contraseñas y prevención de inyecciones SQL.

### 6. Funcionalidades extra sugeridas
- Notificaciones por correo electrónico cuando una solicitud cambia de estado.
- Dashboard con estadísticas de las solicitudes gestionadas.
- Historial de cambios en cada solicitud.

## Instalación y configuración

### Prerrequisitos
- Python 3.8+
- pip
- Node.js (si se utiliza React o Vue.js)

### Instalación

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_PROYECTO>
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar las variables de entorno:
   Crear un archivo `.env` en la raíz del proyecto y agregar las siguientes variables:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=<TU_SECRET_KEY>
   ```

5. Inicializar la base de datos:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Ejecutar la aplicación:
   ```bash
   flask run
   ```

### Frontend (opcional)

1. Instalar dependencias:
   ```bash
   npm install
   ```

2. Ejecutar el servidor de desarrollo:
   ```bash
   npm run serve
   ```

## Estructura del Proyecto

```
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   └── solicitud.html
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   └── js
│   │       └── scripts.js
├── migrations
├── venv
├── .env
├── config.py
├── requirements.txt
└── run.py
```