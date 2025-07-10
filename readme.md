# 🚀 API REST con Django + JWT + Roles + Recuperación por Correo

Una API REST robusta y escalable desarrollada con Django REST Framework, que incluye autenticación JWT, sistema de roles y permisos, y recuperación de contraseña por correo electrónico.

## 📋 Descripción

Este proyecto fue diseñado con el objetivo de crear un sistema seguro, escalable y siguiendo buenas prácticas de desarrollo (OOP, modularización, separación de responsabilidades). Es ideal para aplicaciones multiusuario y multiempresa que requieren un sistema de autenticación y autorización robusto.

## ✨ Características Principales

- 🔐 **Autenticación y autorización segura con JWT**
- 👥 **Gestión de usuarios y roles mediante grupos y permisos**
- 🔄 **Recuperación de contraseña con envío de correo usando Google SMTP**
- 🏗️ **Arquitectura escalable y multiusuario (multiempresa)**
- ⚙️ **Configuración por entornos (desarrollo, producción)**

## 🔧 Tecnologías Implementadas

- ✅ Django REST Framework
- ✅ Autenticación JWT
- ✅ Sistema de roles y permisos
- ✅ Integración con Gmail para recuperación de contraseñas
- ✅ Arquitectura multiusuario
- ✅ Configuración de entornos de desarrollo

## 🧰 Requisitos

- Python 3.10+
- pip
- Git
- MariaDB / MySQL / PostgreSQL
- (opcional) Virtualenv / Poetry / .venv
- (opcional) Docker y Docker Compose

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno 🔐

Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
DJANGO_SECRET_KEY=tu_clave_secreta
DJANGO_ENV=dev
DEBUG=True

DB_ENGINE=django.db.backends.mysql
DB_NAME=nombre_bd
DB_USER=usuario
DB_PASSWORD=clave
DB_HOST=localhost
DB_PORT=3306

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=clave_app_google
EMAIL_USE_TLS=True
```

⚠️ **Importante**: Asegúrate de usar una contraseña de aplicación de Gmail para el `EMAIL_HOST_PASSWORD`.

### 5. Configurar la base de datos

Crea una base de datos en MariaDB/MySQL/PostgreSQL con el mismo nombre que colocaste en `.env`:

```sql
CREATE DATABASE nombre_bd CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

### 6. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear superusuario

```bash
python manage.py createsuperuser
```

### 8. Iniciar el servidor

```bash
python manage.py runserver
```

Accede en: http://127.0.0.1:8000/api/v1/

### 9. (Opcional) Cargar roles y permisos

Este proyecto incluye un comando personalizado para inicializar grupos y permisos:

```bash
python manage.py init_roles
```

Esto crea grupos como "Administradores", "Usuarios" y asigna permisos a cada uno.

### 10. Probar endpoints

Puedes usar herramientas como Postman o Insomnia para probar los endpoints:

**Autenticación JWT:**
- `POST /api/v1/auth/login/`
- `POST /api/v1/auth/refresh/`

**Registro empresa + administrador:**
- `POST /api/v1/companies/create-company/`

**Recuperación de clave:**
- `POST /api/v1/auth/request-reset-email/`
- `POST /api/v1/auth/password-reset/confirm/`

### 11. Ejecutar pruebas

```bash
python manage.py test
```

## 📚 Documentación de la API

### Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/v1/auth/login/` | Iniciar sesión |
| POST | `/api/v1/auth/refresh/` | Refrescar token JWT |
| POST | `/api/v1/companies/create-company/` | Crear empresa y administrador |
| POST | `/api/v1/auth/request-reset-email/` | Solicitar recuperación de contraseña |
| POST | `/api/v1/auth/password-reset/confirm/` | Confirmar nueva contraseña |

### Estructura de Respuestas

Las respuestas siguen el siguiente formato estándar:

```json
{
  "success": true,
  "message": "Mensaje descriptivo",
  "data": {
    // Datos de respuesta
  }
}
```

### Códigos de Error

- `400` - Bad Request: Datos inválidos
- `401` - Unauthorized: No autenticado
- `403` - Forbidden: Sin permisos
- `404` - Not Found: Recurso no encontrado
- `500` - Internal Server Error: Error del servidor

## 🏗️ Arquitectura del Proyecto

```
proyecto/
├── apps/
│   ├── authentication/
│   ├── companies/
│   └── users/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   └── urls.py
├── requirements.txt
├── manage.py
└── .env.example
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - mira el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Maggiver Acevedo**
- 💼 LinkedIn: [Maggiver Acevedo](https://www.linkedin.com/in/maggiver-acevedo-6287b01a3/)
- 🐱 GitHub: [@magg77](https://github.com/magg77)
- 📧 Email: escenariopaloma@gmail.com
*Desarrollador Backend especializado en Django, Python y APIs REST. Apasionado por crear soluciones escalables y seguras.*

## 🌟 Reconocimientos

- Django REST Framework por la excelente documentación
- La comunidad de Django por el apoyo continuo

---

⭐ **¿Te gustó el proyecto?**
¡Dale una estrella al repo y conéctate conmigo en LinkedIn!

💼 **¿Qué opinas del stack tecnológico?**
¿Agregarías alguna funcionalidad adicional? ¡Déjame saber en los issues!


## 📸 Capturas de Pantalla y Diagramas

### Ejemplo de Request/Response
![API Demo](https://raw.githubusercontent.com/magg77/imgs/master/request.jpg)

### Modelo de Datos
![API Demo](https://github.com/magg77/imgs/blob/master/model-shema.bmp)