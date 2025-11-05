# 🐱 Kitty Glow - Sistema E-Commerce Django

Sistema completo de comercio electrónico desarrollado con Django 5.2.7 que incluye gestión de productos, autenticación avanzada, sistema de roles y notificaciones por email.

---

## 📋 Tabla de Contenidos

1. [Características Principales](#-características-principales)
2. [Requisitos del Sistema](#-requisitos-del-sistema)
3. [Instalación Rápida](#-instalación-rápida)
4. [Estructura del Proyecto](#-estructura-del-proyecto)
5. [Configuración de Base de Datos](#-configuración-de-base-de-datos)
6. [Sistema de Autenticación](#-sistema-de-autenticación)
7. [Gestión de Cuentas de Usuario](#-gestión-de-cuentas-de-usuario)
8. [Notificaciones por Email](#-notificaciones-por-email)
9. [Modelos de Datos](#-modelos-de-datos)
10. [Comandos Útiles](#-comandos-útiles)
11. [Solución de Problemas](#-solución-de-problemas)
12. [Seguridad](#-seguridad)

---

## ✨ Características Principales

### 🛍️ E-Commerce
- Gestión completa de catálogo de productos
- Sistema de categorías para productos
- Procesamiento de pedidos y carrito de compras
- Reseñas y calificaciones de productos
- Panel de administración Django

### 🔐 Autenticación Avanzada
- **Login flexible**: Inicio de sesión con email o nombre de usuario
- Registro con verificación de email
- Validación estricta de contraseñas (8 requisitos de seguridad)
- Restablecimiento de contraseña por email
- Sistema de roles (Admin, Usuario, Moderador, Invitado)
- Sesiones configurables (30 min de inactividad)
- Historial de inicios de sesión
- **Cambio de contraseña desde el perfil**
  - Requiere contraseña actual para mayor seguridad
  - Validación estricta de nueva contraseña (8 requisitos)
  - Validación ANTES de cerrar sesión
  - Cierre de sesión automático después del cambio
  - Notificación por email con detalles del cambio
- **Gestión de sesiones activas**
  - Detección automática de múltiples inicios de sesión
  - Vista completa de todos los dispositivos conectados
  - Información detallada: IP, navegador, SO, última actividad
  - Cierre remoto de sesiones individuales
  - Cierre masivo de todas las sesiones excepto la actual
  - Protección contra cierre accidental de sesión actual
  - Auto-actualización cada 30 segundos
  - Limpieza automática de sesiones inactivas (+30 días)

### 👥 Gestión de Usuarios (Administradores)
- **Panel completo de gestión de usuarios**
  - Lista de todos los usuarios del sistema con DataTables
  - Búsqueda, filtrado y ordenamiento avanzado
  - Información en tiempo real (reseñas, favoritos, sesiones)
- **Modal Ver Usuario**
  - Visualización completa de datos personales y del sistema
  - Estadísticas en tiempo real
  - Fechas en hora local (Colombia)
- **Modal Editar Usuario**
  - Formulario completo de edición con validación
  - Edición de rol, estado y verificación de email
  - Validación de username y email únicos
  - Feedback inmediato con mensajes
- **Modal Eliminar Usuario**
  - Sistema de eliminación seguro con advertencias
  - Confirmación obligatoria con checkbox
  - Protección contra auto-eliminación
  - Protección del último superusuario
- **Sistema AJAX completo**
  - Sin recargas de página
  - Respuestas rápidas
  - Experiencia fluida

### 🗑️ Gestión de Cuentas
- **Eliminación con período de gracia (30 días)**
  - Desactivación inmediata con opción de cancelar
  - Reactivación automática al iniciar sesión
  - Email de notificación con fecha de eliminación
  
- **Eliminación inmediata**
  - Sin posibilidad de recuperación
  - Múltiples confirmaciones de seguridad
  - Email de confirmación
  
- **Exportación de datos en JSON**
  - Información personal completa
  - Historial de sesiones (últimas 50)
  - Descarga instantánea

### 📧 Notificaciones por Email
- Login desde nuevo dispositivo
- Cambio de contraseña
- Eliminación/desactivación de cuenta
- Verificación de email
- Diseño HTML profesional y responsive
- **Texto plano en desarrollo** - sin HTML en la consola
- **Fechas en hora local** - zona horaria Colombia (UTC-5)

### 🌍 Sistema de Zona Horaria
- **Filtros personalizados de Django**
  - 6 filtros: localtime, local_datetime, local_date, local_time, timezone_name, timezone_offset
  - 2 template tags: current_timezone, now_local
- **Conversión automática UTC → America/Bogota**
  - Todas las fechas en hora de Colombia
  - Formato 12 horas (AM/PM) familiar
  - Fechas legibles en español
- **15 templates actualizados**
  - 6 templates de email con fechas locales
  - 8 templates de interfaz con fechas locales
  - Formato consistente en toda la aplicación

### 🎨 Modales Personalizados
- **Reemplazo completo de alerts/confirms nativos**
  - Diseño Bootstrap 5 consistente
  - Mejor experiencia de usuario
  - Soporte para async/await
- **5 tipos de modales**
  - Success, Error, Warning, Info, Confirm
  - Iconos descriptivos
  - Colores según tipo de mensaje
- **Sistema unificado**
  - Atributos data-confirm en forms
  - Manejo automático de confirmaciones
  - Disponible en toda la aplicación

### 🔒 Seguridad
- 7 capas de validación para eliminación de cuenta
- Protección CSRF en todos los formularios
- Tokens únicos para acciones críticas
- Validación lado cliente y servidor
- Rate limiting preparado

### 🎨 Arquitectura Frontend
- **Separación de responsabilidades**: HTML, CSS y JavaScript en archivos independientes
- **Archivos estáticos optimizados**: CSS y JS externos para mejor cacheo
- **Organización modular**: 
  - 7 archivos CSS específicos por funcionalidad
  - 8 archivos JavaScript con lógica separada
- **Rendimiento mejorado**: Archivos estáticos cacheables por navegador
- **Mantenibilidad**: Código centralizado y reutilizable

---

## 📦 Requisitos del Sistema

- **Python**: 3.14+
- **MySQL**: 8.0+ (opcional, puede usar SQLite)
- **SO**: macOS, Linux o Windows

### Dependencias Principales
```
Django==5.2.7
mysqlclient==2.2.7
mysql-connector-python==9.4.0
PyMySQL==1.1.2
```

---

## 🚀 Instalación Rápida

### Opción 1: Scripts Automáticos (Recomendado)

#### 🍎 **macOS / Linux**
```bash
chmod +x start_server.sh
./start_server.sh
```

#### 🪟 **Windows**
```cmd
start_server.bat
```

#### 🐍 **Multiplataforma (Python)**
```bash
python start_server.py
```

Los scripts realizan automáticamente:
- ✅ Detección y configuración de MySQL
- ✅ Creación del entorno virtual
- ✅ Instalación de dependencias
- ✅ Ejecución de migraciones
- ✅ Inicio del servidor
- ✅ Apertura del navegador

---

### Opción 2: Instalación Manual

#### **1. Crear entorno virtual**

**🍎 macOS ARM (M1/M2/M3) / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**🪟 Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

#### **2. Instalar dependencias**

**Todos los sistemas operativos:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### **3. Configurar base de datos**
Ver sección [Configuración de Base de Datos](#️-configuración-de-base-de-datos)

#### **4. Ejecutar migraciones**

**Todos los sistemas operativos:**
```bash
python manage.py makemigrations
python manage.py migrate
```

#### **5. Crear datos de prueba (opcional)**

**Todos los sistemas operativos:**
```bash
python manage.py crear_datos_prueba
```

#### **6. Crear superusuario**

**Todos los sistemas operativos:**
```bash
python manage.py createsuperuser
```

#### **7. Iniciar servidor**

**Todos los sistemas operativos:**
```bash
python manage.py runserver
```

**Acceso**:
- Aplicación: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

---

## 📁 Estructura del Proyecto

```
kitty_project/
├── kitty_glow/                      # Proyecto Django principal
│   ├── settings.py                  # Configuración
│   ├── local_settings.py            # Config. desarrollo
│   ├── cloud_settings.py            # Config. producción
│   ├── logging_settings.py          # Config. logs
│   ├── urls.py                      # Rutas principales
│   ├── wsgi.py / asgi.py           # Puntos de entrada
│   ├── static/                      # Archivos estáticos globales
│   │   └── js/
│   │       ├── confirmHandlers.js   # Manejo de confirmaciones con data-confirm
│   │       ├── customModals.js      # Sistema de modales personalizados
│   │       ├── initializeDataTables.js
│   │       └── themeBasedOnPreference.js
│   ├── templates/
│   │   └── base.html                # Template base (incluye modales globales)
│   └── templatetags/                # Template tags personalizados
│       ├── __init__.py              # Package marker
│       └── timezone_filters.py      # Filtros de zona horaria
│
├── accounts/                        # App de autenticación
│   ├── models.py                    # CustomUser, UserRole, LoginHistory
│   ├── views.py                     # Vistas de auth
│   ├── forms.py                     # Formularios
│   ├── validators.py                # Validador de contraseñas
│   ├── admin.py                     # Admin personalizado
│   ├── urls.py                      # Rutas de accounts
│   ├── management/
│   │   └── commands/
│   │       └── delete_expired_accounts.py  # Limpieza automática
│   ├── migrations/
│   ├── static/
│   │   └── accounts/
│   │       ├── css/                 # Estilos específicos de accounts
│   │       │   ├── active_sessions.css
│   │       │   ├── auth.css
│   │       │   ├── change_password.css
│   │       │   ├── dashboard.css
│   │       │   ├── delete_account.css
│   │       │   ├── password_reset.css
│   │       │   └── password_reset_confirm.css
│   │       └── js/                  # Scripts específicos de accounts
│   │           ├── active_sessions.js
│   │           ├── auth.js
│   │           ├── change_password.js
│   │           ├── dashboard.js
│   │           ├── delete_account.js
│   │           ├── password_reset_confirm.js
│   │           ├── register.js
│   │           └── user-list.js
│   └── templates/
│       └── accounts/
│           ├── login.html
│           ├── register.html
│           ├── dashboard.html
│           ├── profile.html
│           ├── delete_account.html
│           ├── password_reset_request.html
│           ├── password_reset_confirm.html
│           └── emails/
│               ├── verification_email.html
│               ├── password_reset_email.html
│               ├── login_notification.html
│               ├── password_changed_notification.html
│               ├── account_deleted_notification.html
│               └── account_deactivation_notification.html
│
├── productos/                       # App de e-commerce
│   ├── models.py                    # Producto, Categoria, etc.
│   ├── views.py                     # Vistas públicas
│   ├── views_crud.py                # Vistas CRUD (admin)
│   ├── admin.py
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── crear_datos_prueba.py  # 15 productos de prueba
│   ├── static/
│   │   └── productos/
│   └── templates/
│       └── productos/
├── SQL/MySQL/                       # Scripts SQL
│   ├── Model/
│   │   └── Database_Model.mwb
│   └── Scripts/
│       ├── CreateDB.sql
│       ├── DropDB.sql
│       ├── ModelDB.sql
│       └── QueriesDB.sql
│
├── manage.py                        # Utilidad Django
├── requirements.txt                 # Dependencias
├── runtime.txt                      # Versión Python
├── Procfile                         # Despliegue
├── nixpacks.toml                   # Config Nixpacks
│
├── start_server.sh                  # Script inicio (macOS/Linux)
├── start_server.bat                 # Script inicio (Windows)
├── start_server.py                  # Script inicio (Python)
├── start_server_backup.sh          # Backup del script
│
├── create_default_superuser.py     # Crear superuser automático
├── verify_implementation.sh        # Verificar implementación
│
├── SEPARACION_CSS_JS.md            # Documentación separación CSS/JS
├── .env                            # Variables de entorno (no versionado)
├── .gitignore
├── LICENSE
└── README.md                       # Este archivo
```

---

## 🗄️ Configuración de Base de Datos

### MySQL (Configuración por Defecto)

**Parámetros**:
- Base de datos: `kitty_glow_db`
- Host: `localhost`
- Puerto: `3307`
- Usuario: `root`
- Password: `**********`

### Instalación de MySQL por Sistema Operativo

#### 🍎 **macOS ARM (M1/M2/M3)**

**Paso 1: Instalar MySQL**
```bash
# Opción A: Con Homebrew (recomendado)
brew install mysql
brew services start mysql

# Opción B: Instalador oficial
# Descargar desde: https://dev.mysql.com/downloads/mysql/
```

**Paso 2: Configurar variables de entorno**

Para macOS con chips Apple Silicon, agrega estas variables a `~/.zprofile`:

```bash
# MySQL Configuration para Apple Silicon
export PATH="/usr/local/mysql/bin:$PATH"
export MYSQLCLIENT_CFLAGS="-I/usr/local/mysql/include"
export MYSQLCLIENT_LDFLAGS="-L/usr/local/mysql/lib -lmysqlclient"
export PKG_CONFIG_PATH="/usr/local/mysql/lib/pkgconfig"
export DYLD_LIBRARY_PATH="/usr/local/mysql/lib:$DYLD_LIBRARY_PATH"
export DYLD_FALLBACK_LIBRARY_PATH="/usr/local/mysql/lib:$DYLD_FALLBACK_LIBRARY_PATH"
```

**Paso 3: Recargar configuración**
```bash
source ~/.zprofile
```

#### 🐧 **Linux (Ubuntu/Debian)**

```bash
# Actualizar repositorios
sudo apt update

# Instalar MySQL Server
sudo apt install mysql-server

# Iniciar servicio
sudo systemctl start mysql
sudo systemctl enable mysql

# Configurar seguridad
sudo mysql_secure_installation
```

#### 🪟 **Windows**

1. Descargar MySQL Installer desde: https://dev.mysql.com/downloads/installer/
2. Ejecutar el instalador
3. Seleccionar "Developer Default" o "Custom"
4. Configurar contraseña de root
5. Completar instalación
6. MySQL se ejecutará como servicio automáticamente

### SQLite (Alternativa Simple)

Para desarrollo sin MySQL, modifica `kitty_glow/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Ventajas de SQLite**:
- ✅ Sin instalación adicional
- ✅ Sin configuración de variables
- ✅ Base de datos en un solo archivo
- ✅ Perfecto para desarrollo

---

## 🔐 Sistema de Autenticación

### Login Flexible: Email o Username

El sistema permite iniciar sesión usando **email o nombre de usuario** de forma automática:

**Características**:
- ✅ **Detección automática**: No requiere selector manual
- ✅ **Una sola caja de texto**: Mejora la experiencia de usuario
- ✅ **Seguridad preservada**: No revela si email/username existe
- ✅ **Compatible**: Funciona con todo el sistema de autenticación Django

**Cómo funciona**:
```python
# El usuario puede ingresar cualquiera de estos:
"usuario123"           # Username → se usa directamente
"user@example.com"     # Email → se busca el username asociado

# El sistema detecta automáticamente si hay '@' en el input
# y convierte el email a username antes de autenticar
```

**Ejemplo de uso**:
```
Usuario puede hacer login con:
  • Username: "juan_perez"
  • Email:    "juan@example.com"

Ambas opciones son válidas y funcionan correctamente ✅
```

**Seguridad**:
- Mensaje genérico de error: "Credenciales inválidas"
- No revela si el email o username existe en la base de datos
- Registra todos los intentos en `LoginHistory` (exitosos y fallidos)

### Validación de Contraseñas

Validador personalizado con **8 requisitos estrictos**:

1. ✅ **Longitud**: 8-20 caracteres
2. ✅ **Letra mayúscula**: Al menos una (A-Z)
3. ✅ **Letra minúscula**: Al menos una (a-z)
4. ✅ **Carácter especial**: Al menos uno (`!¡@#$%^&*.-_+(){}[]:;<>?,/\|~`)
5. ✅ **Sin espacios**: No se permiten espacios en blanco ni emojis
6. ✅ **Diferente a la anterior**: Debe ser diferente a la contraseña actual (al cambiar/restablecer)
7. ✅ **No similar a datos personales**: No puede ser similar a username, email o nombre
8. ✅ **Sin caracteres consecutivos**: No permite patrones repetitivos como:
   - Caracteres idénticos: `aaa`, `111`, `AAA`, `!!!`
   - Secuencias alfabéticas: `abc`, `xyz`, `ABC`, `XYZ`
   - Secuencias numéricas: `123`, `789`, `456`, `234`

**Ejemplos de contraseñas válidas**: `Kitty@2024`, `Glow@2w4x`, `Pass@1w4r`

**Ejemplos de contraseñas inválidas**:
- `Pass@aaa1` ❌ (caracteres idénticos consecutivos)
- `Pass@123` ❌ (secuencia numérica consecutiva)
- `Pass@abc` ❌ (secuencia alfabética consecutiva)
- `Andres@2024` ❌ (similar al nombre del usuario)

**Validación en tiempo real**: 
- Templates de registro y restablecimiento incluyen validación JavaScript
- Feedback visual instantáneo (indicadores verdes/rojos)
- Mensajes de ayuda claros y específicos

### Verificación de Email

**Flujo**:
1. Usuario se registra → cuenta creada con `is_active=False`
2. Email de verificación enviado automáticamente
3. Usuario hace clic en enlace único con token
4. Cuenta activada → puede iniciar sesión

**Template**: `accounts/templates/accounts/emails/verification_email.html`

### Restablecimiento de Contraseña

**Flujo**:
1. Usuario hace clic en "¿Olvidaste tu contraseña?"
2. Ingresa su email
3. Recibe email con enlace único (válido 1 hora)
4. Crea nueva contraseña (con validación en tiempo real)
5. Recibe email de confirmación de cambio

**Templates**:
- `password_reset_request.html` - Formulario de solicitud
- `password_reset_confirm.html` - Formulario de nueva contraseña
- `emails/password_reset_email.html` - Email con enlace

### Configuración de Sesiones

```python
SESSION_COOKIE_AGE = 1800              # 30 minutos
SESSION_EXPIRE_AT_BROWSER_CLOSE = True # Expira al cerrar navegador
SESSION_SAVE_EVERY_REQUEST = True      # Renueva con cada request
```

**Comportamiento**:
- Sin "Recordarme": expira al cerrar navegador o 30 min inactividad
- Con "Recordarme": dura 2 semanas

### Sistema de Roles

**Roles disponibles**:
- `ADMIN`: Administrador del sistema
- `USER`: Usuario estándar
- `MODERATOR`: Moderador
- `GUEST`: Invitado

**Métodos de verificación**:
```python
user.is_admin()       # True si es admin
user.is_moderator()   # True si es moderador
user.get_role_display()  # Nombre del rol
```

### URLs de Autenticación

```
/accounts/login/                          # Iniciar sesión (email o username)
/accounts/register/                       # Registro
/accounts/logout/                         # Cerrar sesión
/accounts/verify-email/<uidb64>/<token>/  # Verificar email
/accounts/reset-password/                 # Solicitar reset
/accounts/reset-password/<uidb64>/<token>/ # Crear nueva contraseña
/accounts/dashboard/                      # Panel usuario
/accounts/admin/dashboard/                # Panel admin
/accounts/profile/                        # Editar perfil
/accounts/change-password/                # Cambiar contraseña (con logout)
/accounts/active-sessions/                # Ver y gestionar sesiones activas
/accounts/close-session/<id>/             # Cerrar sesión específica
/accounts/close-all-sessions/             # Cerrar todas las sesiones excepto actual
/accounts/users/                          # Lista usuarios (admin)
/accounts/admin/user/<id>/view/           # Ver detalles usuario (AJAX)
/accounts/admin/user/<id>/edit/           # Editar usuario (AJAX)
/accounts/admin/user/<id>/delete/         # Eliminar usuario (AJAX)
```

---

## 🗑️ Gestión de Cuentas de Usuario

### Eliminación con Período de Gracia (30 días)

**Características**:
- ✅ Cuenta desactivada inmediatamente (no puede iniciar sesión)
- ✅ Eliminación automática después de 30 días
- ✅ Email de notificación con fecha de eliminación
- ✅ **Cancelación sencilla**: solo iniciar sesión antes de la fecha
- ✅ Reactivación automática al hacer login

**Proceso**:
1. Usuario va a Perfil → "Zona de Peligro" → "Eliminar mi cuenta"
2. Lee advertencias y consecuencias
3. Ingresa contraseña
4. Escribe "ELIMINAR MI CUENTA"
5. Hace clic en "Desactivar (30 días de gracia)"
6. Confirma en alerta JavaScript
7. Cuenta desactivada + email enviado + logout
8. Usuario puede cancelar iniciando sesión en cualquier momento

**Campos del modelo**:
```python
is_pending_deletion = BooleanField(default=False)
deletion_requested_at = DateTimeField(null=True, blank=True)
scheduled_deletion_date = DateTimeField(null=True, blank=True)
```

### Eliminación Inmediata

**Características**:
- ✅ Eliminación instantánea y permanente
- ✅ Sin posibilidad de recuperación
- ✅ Requiere confirmación adicional (checkbox)
- ✅ Doble confirmación JavaScript
- ✅ Email de notificación enviado

**Proceso**:
1. Mismo inicio que período de gracia
2. Marca checkbox "Entiendo que es irreversible"
3. Hace clic en "Eliminar Inmediatamente"
4. Confirma en primera alerta
5. Confirma en segunda alerta (más seria)
6. Cuenta eliminada permanentemente

### Exportación de Datos (JSON)

**Información exportada**:
```json
{
  "informacion_personal": {
    "username": "...", "email": "...", 
    "nombre": "...", "apellido": "...",
    "telefono": "...", "fecha_nacimiento": "...",
    "biografia": "...", "direccion": "...",
    "ciudad": "...", "pais": "...", "codigo_postal": "..."
  },
  "informacion_cuenta": {
    "fecha_registro": "...", 
    "ultima_actualizacion": "...",
    "email_verificado": true/false,
    "rol": "...", "activo": true/false
  },
  "historial_sesiones": [
    {"ip": "...", "navegador": "...", 
     "fecha": "...", "exitoso": true/false}
  ]
}
```

**Acceso**: 
- Botón en página de eliminación
- URL directa: `/accounts/export-data/`
- Nombre de archivo: `datos_usuario_[username]_[timestamp].json`

### Seguridad de Eliminación

**7 Capas de Validación**:
1. ✅ Login requerido (`@login_required`)
2. ✅ Protección CSRF (`@csrf_protect`)
3. ✅ Verificación de contraseña
4. ✅ Confirmación textual ("ELIMINAR MI CUENTA")
5. ✅ Checkbox adicional (eliminación inmediata)
6. ✅ Primera alerta JavaScript
7. ✅ Segunda alerta (eliminación inmediata)

### Comando de Mantenimiento

**Eliminar cuentas vencidas**:
```bash
python manage.py delete_expired_accounts
```

Este comando:
- Busca cuentas con `is_pending_deletion=True` y fecha vencida
- Envía email final de notificación
- Elimina la cuenta permanentemente
- Muestra resumen de cuentas eliminadas

**Configurar en crontab** (producción):
```bash
crontab -e

# Agregar:
0 2 * * * cd /ruta/kitty_project && source .venv/bin/activate && python manage.py delete_expired_accounts
```

### URLs de Gestión de Cuenta

```
/accounts/delete-account/     # Página de eliminación
/accounts/cancel-deletion/    # Cancelar eliminación programada
/accounts/export-data/        # Descargar datos en JSON
```

---

## 📧 Notificaciones por Email

### Emails Implementados

#### 1. **Verificación de Email** (Registro)
- **Cuándo**: Al registrar nueva cuenta
- **Contenido**: Enlace de verificación único con token
- **Validez**: 24 horas (informado), real ~3 días
- **Template**: `emails/verification_email.html`

#### 2. **Restablecimiento de Contraseña**
- **Cuándo**: Al solicitar "¿Olvidaste tu contraseña?"
- **Contenido**: Enlace único para crear nueva contraseña
- **Validez**: 1 hora (informado)
- **Template**: `emails/password_reset_email.html`

#### 3. **Notificación de Login**
- **Cuándo**: Cada inicio de sesión exitoso
- **Contenido**: 
  - Fecha y hora del login
  - Dirección IP
  - Información del navegador/dispositivo
  - Advertencia si no fue el usuario
- **Template**: `emails/login_notification.html`
- **Función**: `send_login_notification()`

#### 4. **Cambio de Contraseña**
- **Cuándo**: Al cambiar contraseña (reset o desde perfil)
- **Contenido**:
  - Confirmación del cambio
  - Fecha, hora, IP, dispositivo
  - Consejos de seguridad
  - Advertencia crítica si no fue el usuario
- **Template**: `emails/password_changed_notification.html`
- **Función**: `send_password_changed_notification()`

#### 5. **Desactivación de Cuenta** (Período de Gracia)
- **Cuándo**: Al desactivar cuenta con período de 30 días
- **Contenido**:
  - Fecha de desactivación
  - Fecha de eliminación programada
  - Días restantes
  - Botón para reactivar
  - Instrucciones de cancelación
- **Template**: `emails/account_deactivation_notification.html`
- **Función**: `send_account_deactivation_notification()`

#### 6. **Eliminación de Cuenta**
- **Cuándo**: Al eliminar cuenta (inmediata o después de 30 días)
- **Contenido**:
  - Confirmación de eliminación permanente
  - Fecha y hora
  - Mensaje de despedida
  - Advertencia de seguridad
- **Template**: `emails/account_deleted_notification.html`
- **Función**: `send_account_deletion_notification()`

### Configuración de Email

#### Desarrollo (IS_DEPLOYED=False)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
Los emails se muestran en la **consola/terminal**.

#### Producción (IS_DEPLOYED=True)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = '****************'  # App Password
```

**Configurar en `.env`**:
```env
IS_DEPLOYED=False  # True para producción
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=****************
```

### Características de los Emails

- ✅ **Diseño HTML profesional** con estilos inline
- ✅ **Responsive** - compatible con todos los clientes
- ✅ **Texto plano en desarrollo** - emails limpios en la terminal sin HTML
- ✅ **HTML completo en producción** - con estilos, colores y formato visual
- ✅ **Seguridad visual** - íconos, colores, advertencias
- ✅ **Información detallada** - fecha, hora, IP, dispositivo
- ✅ **Consejos de seguridad** incluidos
- ✅ **Fail-safe** - errores no interrumpen operaciones principales

### Formato de Emails

El sistema envía **dos versiones** de cada email mediante la función `send_html_email()`:

#### 📧 **En DESARROLLO** (`IS_DEPLOYED=False`)
- Usa `send_mail()` simple
- Envía **SOLO texto plano** a la consola
- Sin código HTML visible
- Contenido limpio y legible

**Ejemplo en consola**:
```
Notificación de inicio de sesión

Hola Juan Pérez,

Se ha detectado un inicio de sesión en tu cuenta:

  • Fecha: 04/11/2025 a las 15:30:00
  • IP: 192.168.1.100
  • Navegador: Chrome/120.0

Si no fuiste tú, cambia tu contraseña inmediatamente.

Saludos,
Equipo Kitty Glow
```

#### 🌐 **En PRODUCCIÓN** (`IS_DEPLOYED=True`)
- Usa `EmailMultiAlternatives`
- Envía **formato multipart/alternative**:
  - **Parte 1**: Texto plano (fallback)
  - **Parte 2**: HTML con estilos completos
- Clientes modernos (Gmail, Outlook) muestran versión HTML
- Clientes antiguos muestran versión de texto plano

**Estructura del email en producción**:
```
Content-Type: multipart/alternative

--boundary--
Content-Type: text/plain
[Versión de texto plano]

--boundary--
Content-Type: text/html
<!DOCTYPE html>
<html>
  <head>
    <style>
      .header { background: linear-gradient(#667eea, #764ba2); }
      .button { background: #667eea; color: white; }
    </style>
  </head>
  <body>
    <!-- Email con diseño profesional, colores, botones -->
  </body>
</html>
--boundary--
```

**Conversión automática HTML → Texto Plano**:
- Función `html_to_plain_text()` en `accounts/views.py`
- Elimina tags HTML: `<p>`, `<strong>`, `<div>`, etc.
- Convierte `<li>` a bullets (•)
- Preserva saltos de línea y estructura
- Limpia espacios múltiples

---

## 🗂️ Modelos de Datos

### Accounts App

#### **CustomUser**
```python
# Campos de AbstractUser + adicionales:
role = ForeignKey(UserRole)              # Rol del usuario
phone_number = CharField                  # Teléfono
birth_date = DateField                    # Fecha de nacimiento
avatar = ImageField                       # Foto de perfil
bio = TextField                           # Biografía
address / city / country / postal_code   # Dirección completa
email_verified = BooleanField            # Email verificado
last_login_ip = GenericIPAddressField    # Última IP
is_pending_deletion = BooleanField       # Pendiente eliminación
deletion_requested_at = DateTimeField    # Fecha solicitud
scheduled_deletion_date = DateTimeField  # Fecha programada
created_at / updated_at                  # Timestamps
```

#### **UserRole**
```python
name = CharField(choices=ROLE_CHOICES)   # ADMIN, USER, MODERATOR, GUEST
description = TextField                   # Descripción del rol
permissions = JSONField                   # Permisos personalizados
created_at / updated_at                  # Timestamps
```

#### **LoginHistory**
```python
user = ForeignKey(CustomUser)            # Usuario
ip_address = GenericIPAddressField       # IP del login
user_agent = CharField                    # Navegador/dispositivo
login_time = DateTimeField               # Fecha/hora de login
logout_time = DateTimeField              # Fecha/hora de logout
success = BooleanField                   # Login exitoso/fallido
```

#### **ActiveSession**
```python
user = ForeignKey(CustomUser)            # Usuario
session_key = CharField(unique=True)     # Clave de sesión Django
ip_address = GenericIPAddressField       # IP de la sesión
user_agent = TextField                    # User-Agent completo
device_info = CharField                   # Tipo de dispositivo (Desktop, Mobile, Tablet)
browser_info = CharField                  # Navegador (Chrome, Firefox, Safari, etc.)
location = CharField                      # Ubicación (opcional)
created_at = DateTimeField               # Inicio de sesión
last_activity = DateTimeField            # Última actividad
is_current = BooleanField                # Marca sesión actual

# Métodos
get_device_icon()                        # Retorna ícono FontAwesome
get_browser_name()                       # Extrae nombre del navegador
get_os_name()                            # Extrae nombre del SO
```

### Productos App

#### **Categoria**
```python
nombre = CharField(max_length=100)
descripcion = TextField
```

#### **Producto**
```python
nombre = CharField(max_length=200)
descripcion = TextField
precio = DecimalField(max_digits=10, decimal_places=2)
stock = IntegerField
imagen = ImageField
categorias = ManyToManyField(Categoria)
fecha_creacion = DateTimeField
activo = BooleanField
```

#### **Pedido**
```python
usuario = ForeignKey(CustomUser)
fecha_pedido = DateTimeField
total = DecimalField
estado = CharField  # PENDIENTE, PROCESANDO, ENVIADO, ENTREGADO
```

#### **DetallePedido**
```python
pedido = ForeignKey(Pedido)
producto = ForeignKey(Producto)
cantidad = IntegerField
precio_unitario = DecimalField
```

#### **Reseña**
```python
producto = ForeignKey(Producto)
usuario = ForeignKey(CustomUser)
calificacion = IntegerField(1-5)
comentario = TextField
fecha_reseña = DateTimeField
```

---

## ⚙️ Comandos Útiles

### Gestión del Proyecto

#### **Activar entorno virtual**

**🍎 macOS ARM / 🐧 Linux:**
```bash
source .venv/bin/activate
```

**🪟 Windows (CMD):**
```cmd
.venv\Scripts\activate
```

**🪟 Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

#### **Ejecutar servidor**

**Todos los sistemas operativos:**
```bash
# Puerto por defecto (8000)
python manage.py runserver

# Puerto específico
python manage.py runserver 8080

# Accesible desde red local
python manage.py runserver 0.0.0.0:8000
```

### Migraciones

**Todos los sistemas operativos:**
```bash
# Crear migraciones
python manage.py makemigrations
python manage.py makemigrations accounts
python manage.py makemigrations productos

# Aplicar migraciones
python manage.py migrate

# Ver SQL de una migración
python manage.py sqlmigrate accounts 0001

# Ver estado de migraciones
python manage.py showmigrations
```

### Administración

**Todos los sistemas operativos:**
```bash
# Crear superusuario
python manage.py createsuperuser

# O automáticamente (desarrollo)
python create_default_superuser.py

# Shell de Django
python manage.py shell

# Shell de base de datos
python manage.py dbshell
```

### Datos de Prueba

**Todos los sistemas operativos:**
```bash
# Crear 15 productos en 5 categorías
python manage.py crear_datos_prueba
```

### Gestión de Cuentas

**🍎 macOS ARM / 🐧 Linux:**
```bash
# Eliminar cuentas vencidas (período de gracia)
python manage.py delete_expired_accounts

# Verificar implementación
./verify_implementation.sh
```

**🪟 Windows:**
```cmd
# Eliminar cuentas vencidas (período de gracia)
python manage.py delete_expired_accounts

# Verificar implementación
python verify_implementation.py
```

### Pruebas

**Todos los sistemas operativos:**
```bash
# Todas las pruebas
python manage.py test

# App específica
python manage.py test accounts
python manage.py test productos

# Con verbosidad
python manage.py test --verbosity=2
```

### Archivos Estáticos

**Todos los sistemas operativos:**
```bash
# Recolectar archivos estáticos
python manage.py collectstatic

# Limpiar archivos estáticos
python manage.py collectstatic --clear
```

**Estructura de archivos estáticos**:
```
accounts/static/accounts/
├── css/
│   ├── active_sessions.css       # Estilos para sesiones activas
│   ├── auth.css                  # Estilos de autenticación
│   ├── change_password.css       # Estilos cambio de contraseña
│   ├── dashboard.css             # Estilos del dashboard
│   ├── delete_account.css        # Estilos eliminación de cuenta
│   ├── password_reset.css        # Estilos reset de contraseña
│   └── password_reset_confirm.css # Estilos confirmación reset
└── js/
    ├── active_sessions.js        # Auto-actualización sesiones
    ├── auth.js                   # Lógica de autenticación
    ├── change_password.js        # Validación cambio contraseña
    ├── dashboard.js              # Funcionalidad dashboard
    ├── delete_account.js         # Validación eliminación cuenta
    ├── password_reset_confirm.js # Validación en tiempo real (8 requisitos)
    ├── register.js               # Validación de registro
    └── user-list.js              # Gestión de lista de usuarios
```

**Ventajas de la separación CSS/JS**:
- ✅ **Cacheo**: Navegadores pueden cachear archivos estáticos
- ✅ **Mantenibilidad**: Código organizado y fácil de actualizar
- ✅ **Reutilización**: Estilos y scripts compartibles entre templates
- ✅ **Rendimiento**: Posibilidad de minificar y comprimir
- ✅ **Legibilidad**: Templates HTML más limpios

**Nota**: Los templates de email (`emails/*.html`) mantienen CSS inline porque los clientes de correo no soportan archivos externos.

---

## 🔧 Solución de Problemas

### 🍎 Problemas en macOS ARM

#### Error: "Library not loaded: @rpath/libmysqlclient.24.dylib"

**Causa**: Bibliotecas MySQL no configuradas en macOS Apple Silicon.

**Solución rápida:**
```bash
./start_server.sh  # Configura automáticamente
```

**Solución manual:**
```bash
# 1. Instalar MySQL
brew install mysql

# 2. Configurar variables en ~/.zprofile (ver sección MySQL)

# 3. Reinstalar mysqlclient
source .venv/bin/activate
pip uninstall mysqlclient -y
pip install mysqlclient --no-cache-dir
```

#### Error: "mysql_config not found"

```bash
# Instalar MySQL con Homebrew
brew install mysql

# O descargar instalador oficial
# https://dev.mysql.com/downloads/mysql/
```

### 🐧 Problemas en Linux

#### Error: "No module named 'MySQLdb'"

```bash
# Activar entorno virtual
source .venv/bin/activate

# Instalar dependencias del sistema
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

# Reinstalar mysqlclient
pip install mysqlclient --no-cache-dir
```

#### Error: "mysql_config not found"

```bash
# Ubuntu/Debian
sudo apt-get install libmysqlclient-dev

# CentOS/RHEL
sudo yum install mysql-devel
```

### 🪟 Problemas en Windows

#### Error: "No module named 'MySQLdb'"

```cmd
# Activar entorno virtual
.venv\Scripts\activate

# Reinstalar mysqlclient
pip install mysqlclient --no-cache-dir
```

Si persiste el error, usar PyMySQL como alternativa:
```cmd
pip install pymysql
```

Luego agregar en `kitty_glow/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### 🌍 Problemas Multiplataforma

#### Entorno Virtual Corrupto

**🍎 macOS / 🐧 Linux:**
```bash
rm -rf .venv
./start_server.sh  # Recrea automáticamente
```

**🪟 Windows:**
```cmd
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Emails No Se Envían (Desarrollo)

**Verificar**: Los emails se muestran en la **consola**, no en inbox.

```bash
# En desarrollo, ver terminal donde corre el servidor
python manage.py runserver
# Los emails aparecerán aquí
```

### Error al Hacer Migraciones de Accounts

Si ya tienes datos en la BD y agregaste campos nuevos:

```bash
# Opción 1: Eliminar BD y recrear (desarrollo)
python manage.py flush

# Opción 2: Migración manual
python manage.py makemigrations accounts
# Cuando pregunte, proporcionar valores por defecto
python manage.py migrate accounts
```

---

## 🔒 Seguridad

### Variables de Entorno

**IMPORTANTE**: Nunca versionar credenciales. Usar `.env`:

```env
# .env (no versionado)
SECRET_KEY=tu-secret-key-aqui
IS_DEPLOYED=False
DEBUG=True

# Base de datos
DATABASE_NAME=kitty_glow_db
DATABASE_USER=root
DATABASE_PASSWORD=**********
DATABASE_HOST=localhost
DATABASE_PORT=3307

# Email
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=****************
```

### Configuración de Producción

Antes de desplegar:

```python
# settings.py
SECRET_KEY = env('SECRET_KEY')  # Generar nueva
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# Seguridad HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Checklist de Seguridad

- [ ] `SECRET_KEY` única y segura
- [ ] `DEBUG = False` en producción
- [ ] `ALLOWED_HOSTS` configurado
- [ ] HTTPS habilitado
- [ ] Variables de entorno para credenciales
- [ ] Validación de contraseñas estricta
- [ ] Protección CSRF habilitada
- [ ] Rate limiting implementado
- [ ] Logs de seguridad configurados
- [ ] Backups automáticos de BD

---

## 📚 Recursos Adicionales

### Documentación
- [Django 5.2](https://docs.djangoproject.com/en/5.2/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/)
- [Font Awesome](https://fontawesome.com/docs)

### Endpoints Principales

```
# Públicas
/                           # Home
/productos/                 # Catálogo
/productos/<id>/            # Detalle producto
/categorias/                # Categorías

# Autenticación
/accounts/login/            # Login
/accounts/register/         # Registro
/accounts/dashboard/        # Dashboard usuario

# Admin
/admin/                     # Django admin
/accounts/admin/dashboard/  # Dashboard admin
/accounts/users/            # Gestión usuarios
/productos/admin/           # CRUD productos

# Gestión de cuenta
/accounts/profile/          # Perfil
/accounts/change-password/  # Cambiar contraseña
/accounts/active-sessions/  # Ver y gestionar sesiones activas
/accounts/close-session/<id>/     # Cerrar sesión específica
/accounts/close-all-sessions/     # Cerrar todas excepto actual
/accounts/delete-account/   # Eliminar cuenta
/accounts/export-data/      # Exportar datos
```

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Agrega nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y de desarrollo.

---

## 📞 Soporte

### Comandos de Diagnóstico

#### **Todos los sistemas operativos:**
```bash
# Ver versión de Python
python --version

# Ver paquetes instalados
pip list

# Test de MySQLdb
python -c "import MySQLdb; print('✅ MySQLdb OK')"
```

#### **🍎 macOS ARM / 🐧 Linux:**
```bash
# Ver variables de entorno MySQL
echo $DYLD_LIBRARY_PATH           # macOS
echo $LD_LIBRARY_PATH             # Linux

# Probar conexión a MySQL
mysql -u root -p

# Ver ubicación de MySQL
which mysql
mysql --version
```

#### **🪟 Windows:**
```cmd
# Ver variables de entorno
echo %PATH%

# Probar conexión a MySQL
mysql -u root -p

# Ver versión de MySQL
mysql --version
```

---

**Desarrollado con ❤️ usando Django 5.2.7**

**Última actualización**: 5 de noviembre de 2025  
**Versión**: 1.1.0  
**Autor**: Kitty Glow Team

---

## 📝 Registro de Cambios

### Versión 1.1.0 (5 de noviembre de 2025)
- ✅ **Nuevo**: Sistema completo de gestión de usuarios para administradores
  - **Modales interactivos** con Bootstrap 5:
    * **Modal Ver Usuario**: Visualización completa de datos del usuario
      - Información personal (nombre, email, teléfono, biografía)
      - Información del sistema (rol, estado, verificación, superusuario)
      - Estadísticas en tiempo real (reseñas, favoritos, sesiones activas)
      - Fechas de registro y último acceso en hora local
    * **Modal Editar Usuario**: Formulario completo de edición
      - Campos editables: username, email, nombre, apellido, teléfono, biografía
      - Selector de rol con todos los roles disponibles
      - Switches para estado activo y email verificado
      - Validación en tiempo real (username y email únicos)
      - Feedback inmediato con mensajes de éxito/error
    * **Modal Eliminar Usuario**: Sistema de eliminación seguro
      - Advertencias prominentes con diseño rojo
      - Lista clara de consecuencias de la eliminación
      - Confirmación obligatoria mediante checkbox
      - Protecciones: No auto-eliminación, no eliminar último superusuario
  - **3 nuevas vistas AJAX**:
    * `user_view_ajax()` - Obtener datos del usuario con estadísticas
    * `user_edit_ajax()` - GET/POST para edición de usuario
    * `user_delete_ajax()` - POST para eliminación segura
  - **3 nuevas URLs AJAX**:
    * `/accounts/admin/user/<id>/view/`
    * `/accounts/admin/user/<id>/edit/`
    * `/accounts/admin/user/<id>/delete/`
  - **Seguridad multinivel**:
    * Verificación de permisos de administrador en todas las vistas
    * Prevención de auto-eliminación (botón oculto + validación backend)
    * Prevención de eliminar último superusuario del sistema
    * Validación de username y email únicos
    * CSRF tokens en todas las peticiones
  - **JavaScript actualizado**: `user-list.js` (618 líneas)
    * Lógica completa de modales con fetch API
    * Manejo de estados de carga con spinners
    * Formulario de edición dinámico
    * Modal de eliminación con confirmación obligatoria
    * Integración con sistema de modales personalizados
  - **Template actualizado**: `user_list.html` (121+ líneas agregadas)
    * 3 modales Bootstrap 5 agregados
    * Botones con data-attributes para interactividad
    * Integrado con filtros de zona horaria
    * Diseño responsive y profesional

- ✅ **Nuevo**: Sistema de modales personalizados
  - **Reemplazo completo de alerts y confirms nativos**:
    * Eliminados todos los `alert()` y `confirm()` de JavaScript
    * Reemplazados por modales Bootstrap 5 personalizados
    * Diseño consistente con el estilo del proyecto
    * Mejor experiencia de usuario (UX)
  - **Nuevos archivos JavaScript globales**:
    * `customModals.js` (8833 líneas de código)
      - Funciones: `showSuccess()`, `showError()`, `showWarning()`, `showInfo()`, `showConfirm()`
      - Uso de Promises para compatibilidad async/await
      - Creación y gestión dinámica de modales
      - Estilos consistentes con Bootstrap 5
    * `confirmHandlers.js` (3792 líneas de código)
      - Manejo automático de atributos `data-confirm` en forms y buttons
      - Intercepción de submits y clicks para mostrar confirmaciones
      - Sistema de confirmación unificado para toda la aplicación
  - **Templates actualizados con data-confirm**:
    * `active_sessions.html` - Confirmaciones para cerrar sesiones
    * `cart.html` - Confirmación para eliminar productos del carrito
    * `edit_review.html` - Confirmación para eliminar reseñas
    * `my_reviews.html` - Confirmación para eliminar reseñas propias
  - **JavaScript actualizado con modales personalizados**:
    * `register.js` - Reemplazado `alert()` con `showWarning()`
    * `delete_account.js` - Reemplazados `alert()` y `confirm()` con modales
    * `change_password.js` - Reemplazado `confirm()` con `showConfirm()`
  - **Integración en base.html**:
    * Scripts incluidos globalmente para uso en toda la aplicación
    * Disponibles en cualquier página sin importar módulos adicionales

- ✅ **Nuevo**: Sistema completo de zona horaria
  - **Filtros personalizados de Django**:
    * Nuevo paquete: `kitty_glow/templatetags/`
    * Archivo: `timezone_filters.py` (184 líneas)
    * **6 filtros de conversión**:
      - `|localtime` - Convierte datetime UTC a zona horaria local
      - `|local_datetime` - Fecha y hora formateada en zona local
      - `|local_date` - Solo fecha formateada en zona local
      - `|local_time` - Solo hora formateada en zona local
      - `|timezone_name` - Nombre de la zona horaria
      - `|timezone_offset` - Offset de la zona horaria
    * **2 template tags**:
      - `{% current_timezone %}` - Muestra zona horaria actual
      - `{% now_local %}` - Fecha/hora actual en zona local
  - **Configuración de zona horaria**:
    * `TIME_ZONE = 'America/Bogota'` (UTC-5)
    * `USE_TZ = True` (timezone-aware)
    * Conversión automática UTC → Hora local
  - **15 templates actualizados**:
    * **Emails (6 archivos)**: login_notification, password_changed_notification, account_deactivation_notification, account_deleted_notification, password_reset_email, verification_email
    * **Interfaz gráfica (8 archivos)**: active_sessions, my_reviews, producto_detail, productos_por_categoria, my_favorites, lista_productos, my_activity, notifications
    * Todos muestran fechas en hora de Colombia (UTC-5)
    * Formatos consistentes: "dd/mm/YYYY HH:MM:SS AM/PM" o "dd/mm/YYYY"
  - **Beneficios implementados**:
    * Usuarios ven hora de su ubicación (Colombia)
    * Sin confusión con UTC
    * Fechas legibles en español
    * Formato 12 horas familiar en Colombia
    * Conversión automática en todos los templates

- ✅ **Corregido**: Múltiples errores críticos en producción (Railway)
  - **Error 1**: `'timezone_filters' is not a registered tag library`
    * Causa: kitty_glow no estaba en INSTALLED_APPS
    * Solución: Agregado 'kitty_glow' a INSTALLED_APPS en settings.py
    * Django ahora reconoce los template tags personalizados
  - **Error 2**: `ModuleNotFoundError: No module named 'pytz'`
    * Causa: pytz no estaba en requirements.txt
    * Solución: Agregado `pytz==2024.2` a requirements.txt
    * Dependencia necesaria para conversión de zonas horarias
  - **Error 3**: `Cannot resolve keyword 'is_active' into field` (LoginHistory)
    * Causa: LoginHistory no tiene campo 'is_active'
    * Solución: Usar `logout_time__isnull=True` para sesiones activas
    * Lógica correcta: sesión activa = sin logout_time
  - **Error 4**: `'str' object has no attribute 'utcoffset'`
    * Causa: Funciones de notificación pasaban strings en lugar de datetime
    * Solución: Pasar objetos datetime y dejar que templates formateen
    * 4 funciones corregidas: send_login_notification, send_password_changed_notification, send_account_deactivation_notification, send_account_deletion_notification
  - **Error 5**: Advertencias de archivos duplicados en collectstatic
    * Causa: kitty_glow/static en STATICFILES_DIRS y en INSTALLED_APPS
    * Solución: Eliminado de STATICFILES_DIRS (Django lo encuentra automáticamente)
    * collectstatic ahora sin advertencias: "146 static files copied"
  - **Error 6**: FieldError en user_view_ajax con campos None
    * Causa: No se manejaban campos opcionales (role, first_name, etc.)
    * Solución: Manejo explícito de None con valores default
    * Uso de `localtime()` para conversión correcta de fechas
    * Logging mejorado con stack traces completos

- ✅ **Mejorado**: Configuración y organización del proyecto
  - **INSTALLED_APPS actualizado**:
    * Agregado 'kitty_glow' para reconocer templatetags personalizados
    * Ordenado lógicamente con comentarios explicativos
  - **STATICFILES_DIRS limpio**:
    * Lista vacía (Django encuentra static/ de apps automáticamente)
    * Sin duplicados en collectstatic
    * Mejor rendimiento y logs más limpios
  - **Separación de responsabilidades**:
    * Python: Pasa datos sin formatear
    * Templates: Formateo con filtros personalizados
    * JavaScript: Lógica de interacción en archivos externos
  - **Mejoras de seguridad**:
    * Validaciones backend y frontend en todas las operaciones AJAX
    * Logging detallado de errores para debugging
    * Manejo robusto de casos edge (usuarios sin rol, campos None, etc.)

- ✅ **Documentación**:
  - README.md completamente actualizado con todas las nuevas características
  - Commits detallados siguiendo guías de estilo de Git
  - Mensajes de commit en español con descripciones completas
  - Total de commits en esta versión: 7
    1. `6452df8`: fix(settings) - Agregado kitty_glow a INSTALLED_APPS
    2. `97c9ea6`: feat(admin) - Sistema de gestión de usuarios con modales
    3. `b57faf6`: fix(deps) - Agregado pytz a requirements.txt
    4. `022a115`: fix(admin) - Corregida vista user_view_ajax
    5. `80877d3`: fix(settings) - Eliminados duplicados en collectstatic
    6. `6f64497`: fix(admin) - Corregido filtro de sesiones activas
    7. `d480d7d`: fix(emails) - Corregido paso de datetime a templates

### Versión 1.0.7 (4 de noviembre de 2025)
- ✅ **Mejorado**: Separación de CSS y JavaScript de templates HTML
  - **Organización de archivos estáticos mejorada**
    * CSS y JavaScript movidos a archivos externos
    * Mejor cacheo por parte de los navegadores
    * Código más mantenible y reutilizable
  - **Archivos CSS creados** (5 nuevos):
    * `active_sessions.css` - Estilos para gestión de sesiones activas
    * `change_password.css` - Estilos para cambio de contraseña
    * `delete_account.css` - Estilos para eliminación de cuenta
    * `password_reset.css` - Estilos para solicitud de restablecimiento
    * `password_reset_confirm.css` - Estilos para confirmación de nueva contraseña
  - **Archivos JavaScript creados** (4 nuevos):
    * `active_sessions.js` - Auto-actualización de sesiones cada 30s
    * `change_password.js` - Toggle de contraseñas y validación
    * `delete_account.js` - Validación de formulario y confirmaciones
    * `password_reset_confirm.js` - Validación en tiempo real de 8 requisitos
  - **Templates actualizados** (5 archivos):
    * `password_reset_request.html` - Referencias CSS externas
    * `password_reset_confirm.html` - Referencias CSS/JS externas
    * `delete_account.html` - Referencias CSS/JS externas
    * `change_password.html` - Referencias CSS/JS externas
    * `active_sessions.html` - Referencias CSS/JS externas
  - **Beneficios obtenidos**:
    * ~584 líneas de código reorganizadas
    * Separación clara de responsabilidades (HTML/CSS/JS)
    * Archivos estáticos cacheables
    * Templates HTML más limpios y legibles
    * Preparado para minificación y compresión
  - **Comando ejecutado**: `collectstatic` (9 nuevos archivos recolectados)
  - **Documentación**: `SEPARACION_CSS_JS.md` con detalles completos
  - **Nota**: Templates de email mantienen CSS inline (requerido por clientes de correo)

### Versión 1.0.6 (4 de noviembre de 2025)
- ✅ **Mejorado**: Sistema de validación de contraseñas ampliado a 8 requisitos
  - **Nuevo requisito 1.8**: Detección de caracteres consecutivos
    * Detecta caracteres idénticos: `aaa`, `111`, `AAA`
    * Detecta secuencias alfabéticas: `abc`, `xyz`, `ABC`
    * Detecta secuencias numéricas: `123`, `789`, `456`
  - Actualizado `CustomPasswordValidator` en `accounts/validators.py`
  - Nuevas funciones de validación:
    * `_has_identical_consecutive()` - Regex para caracteres idénticos
    * `_has_alphabetic_sequence()` - Loop para secuencias alfabéticas
    * `_has_numeric_sequence()` - Loop para secuencias numéricas
  - Normalización de texto con `unicodedata` (insensible a acentos)
  - **Templates actualizados** con lista completa de requisitos:
    * `register.html` - 7 requisitos (1-5, 7-8)
    * `change_password.html` - 8 requisitos completos (1-8)
    * `password_reset_confirm.html` - 9 items (8 requisitos + confirmación)
  - **Validación JavaScript** en tiempo real para password_reset_confirm.html
    * Función `hasConsecutiveChars()` replica lógica del backend
    * Indicadores visuales (verde/rojo) para cada requisito
    * Detección instantánea de patrones consecutivos
  - **Testing exhaustivo**:
    * Nuevo script: `test_consecutive_chars.py` (27 tests, 100% pass)
    * Script de demostración: `demo_validacion_pre_logout.py` (6 casos)
  - **Documentación completa**:
    * `ACTUALIZACION_TEMPLATES_PASSWORDS.md` - Cambios en templates
    * `VERIFICACION_CAMBIO_PASSWORD_COMPLETA.md` - Flujo técnico
    * `CONFIRMACION_VALIDACION_PRE_LOGOUT.md` - Verificación final
  - **Verificado**: Validación ocurre ANTES de logout en cambio de contraseña
    * Doble capa: formulario + vista
    * logout() solo se ejecuta tras validación exitosa
    * 6 casos de prueba demuestran comportamiento correcto
  - **Configuración de archivos estáticos** corregida
    * Eliminadas rutas duplicadas de `STATICFILES_DIRS`
    * Django auto-descubre carpetas static de las apps
    * Sin warnings en `collectstatic`

### Versión 1.0.5 (4 de noviembre de 2025)
- ✅ **Nuevo**: Sistema de gestión de sesiones activas
  - Nuevo modelo `ActiveSession` en `accounts/models.py`
  - Nuevo middleware `ActiveSessionMiddleware` en `accounts/middleware.py`
  - 3 nuevas vistas: `active_sessions_view()`, `close_session_view()`, `close_all_sessions_view()`
  - Template completo: `accounts/templates/accounts/active_sessions.html`
  - Admin: `ActiveSessionAdmin` registrado
  - **Detección automática** de dispositivos, navegador, OS, IP
  - **Lista visual** de todas las sesiones activas del usuario
  - **Información detallada**: IP, navegador, sistema operativo, última actividad
  - **Cierre individual** de sesiones sospechosas
  - **Cierre masivo** de todas las sesiones excepto la actual
  - **Protección**: No permite cerrar la sesión actual desde la vista
  - **Auto-actualización**: La página se recarga cada 30 segundos
  - **Limpieza automática**: Sesiones con +30 días de inactividad
  - Middleware actualiza sesiones en cada request
  - Migración: `0003_activesession.py`
  - URLs: `/accounts/active-sessions/`, `/accounts/close-session/<id>/`, `/accounts/close-all-sessions/`
  - Documento de pruebas: `PRUEBA_SESIONES_ACTIVAS.md`

### Versión 1.0.4 (4 de noviembre de 2025)
- ✅ **Nuevo**: Cambio de contraseña desde el perfil con seguridad mejorada
  - Nuevo formulario `ChangePasswordForm` en `accounts/forms.py`
  - Nueva vista `change_password_view()` en `accounts/views.py`
  - Nueva URL `/accounts/change-password/`
  - Template completo: `accounts/templates/accounts/change_password.html`
  - **Requiere contraseña actual** para autorizar el cambio
  - **Validación estricta** de nueva contraseña (7 requisitos)
  - **Cierre de sesión automático** después del cambio por seguridad
  - **Notificación por email** con detalles (fecha, hora, IP, navegador)
  - Interfaz con mostrar/ocultar contraseña
  - Validación en tiempo real (JavaScript)
  - Confirmación antes de enviar
  - Sección de seguridad agregada en perfil
  - Consejos de seguridad incluidos
  - Documento de pruebas: `PRUEBA_CAMBIO_PASSWORD.md`

### Versión 1.0.3 (4 de noviembre de 2025)
- ✅ **Verificado**: Sistema de emails en producción
  - Confirmado envío de HTML completo en producción
  - Nueva función `send_html_email()` wrapper
  - Lógica condicional basada en `IS_DEPLOYED`
  - Producción: `EmailMultiAlternatives` con HTML + texto plano
  - Desarrollo: `send_mail()` solo con texto plano
  - 6 funciones de email actualizadas con wrapper
  - Documento de verificación: `VERIFICACION_EMAIL_PRODUCCION.md`
  - Script de prueba: `test_email_production_simple.py`

### Versión 1.0.2 (4 de noviembre de 2025)
- ✅ **Mejorado**: Emails en texto plano para desarrollo
  - Nueva función `html_to_plain_text()` en `accounts/views.py`
  - Emails en consola ahora sin código HTML
  - Conversión automática: HTML → Texto limpio
  - Listas convertidas a bullets (•)
  - Mantiene HTML profesional en producción
  - 6 funciones de email actualizadas

### Versión 1.0.1 (4 de noviembre de 2025)
- ✅ **Nuevo**: Login flexible con email o nombre de usuario
  - Detección automática del tipo de credencial
  - Una sola caja de texto para mejorar UX
  - Mantiene compatibilidad con sistema existente
  - Seguridad preservada (no revela si credenciales existen)

### Versión 1.0.0 (4 de noviembre de 2025)
- ✅ Sistema de autenticación completo
- ✅ Gestión de cuentas con eliminación (gracia 30 días)
- ✅ Exportación de datos en JSON
- ✅ 6 tipos de notificaciones por email
- ✅ Sistema de productos y categorías
- ✅ Panel de administración

