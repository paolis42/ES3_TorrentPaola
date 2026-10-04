# GeekMatch Trips - ES3

Proyecto desarrollado para la asignatura Programación Back End.

En la ES3, GeekMatch Trips mantiene las funcionalidades HTML desarrolladas en la ES2 y agrega una API RESTful utilizando Django REST Framework.

La API permite consultar, crear, editar y eliminar lógicamente registros de lugares turísticos mediante JSON.

---

## Tecnologías utilizadas

- Python
- Django
- Django REST Framework
- SQLite
- python-decouple
- Token Authentication
- JWT con djangorestframework-simplejwt
- drf-spectacular
- Swagger / OpenAPI

---

## Instalación

### 1. Crear entorno virtual

```powershell
py -m venv .venv
```

### 2. Activar entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 4. Configurar variables de entorno

El proyecto utiliza un archivo `.env` para almacenar variables sensibles.

Si se clona el repositorio en otro equipo, se debe crear un archivo `.env` a partir de `.env.example`.

Ejemplo:

```env
SECRET_KEY=
DEBUG=True
PASS_ADMIN=
PASS_NORMAL=
PASS_VIEWER=
```

El archivo `.env` real no debe subirse al repositorio porque contiene información sensible.

---

## Base de datos

Ejecutar las migraciones:

```powershell
python manage.py migrate
```

Para comprobar que no existen cambios pendientes:

```powershell
python manage.py makemigrations --check --dry-run
```

El resultado esperado es:

```text
No changes detected
```

---

## Usuarios y roles

La aplicación utiliza tres roles.

### viewer

Puede:

- consultar la lista de registros;
- consultar un registro individual.

No puede:

- crear;
- editar;
- eliminar.

### normal

Puede:

- consultar registros;
- crear registros.

No puede:

- editar;
- eliminar.

### admin

Puede:

- consultar;
- crear;
- editar;
- eliminar.

Los permisos se validan en el servidor mediante Django REST Framework.

---

## Crear usuarios de prueba

Después de configurar las contraseñas en `.env`, se puede ejecutar:

```powershell
python manage.py shell -c "exec(open('crear_usuarios.py', encoding='utf-8').read())"
```

Este script crea o actualiza los usuarios correspondientes a los roles:

- `admin`
- `normal`
- `viewer`

---

## Ejecutar el proyecto

Para iniciar el servidor:

```powershell
python manage.py runserver
```

El servidor queda disponible en:

```text
http://127.0.0.1:8000/
```

La ruta raíz `/` no tiene una vista asociada, por lo que puede responder 404. Esto no afecta el funcionamiento del proyecto.

El login HTML está disponible en:

```text
http://127.0.0.1:8000/login/
```

Las pantallas HTML desarrolladas en la ES2 continúan funcionando junto con la nueva API.

---

# API REST

La API se encuentra bajo:

```text
/api/
```

Las vistas HTML de la ES2 continúan funcionando en paralelo con la API REST.

---

## Autenticación

La API soporta dos mecanismos de autenticación:

1. Token Authentication de Django REST Framework.
2. JWT mediante `djangorestframework-simplejwt`.

Esto permite conservar compatibilidad con las pruebas realizadas inicialmente mediante Token Authentication y, al mismo tiempo, incorporar tokens JWT con expiración y refresco.

---

## Token Authentication

Para solicitar un token tradicional se utiliza:

```text
POST /api/token/
```

El token debe enviarse en la cabecera HTTP:

```text
Authorization: Token TOKEN_DEL_USUARIO
```

Los tokens reales no deben guardarse en el código, README ni repositorio.

---

## Autenticación JWT

Para obtener un par de tokens JWT se utiliza:

```text
POST /api/jwt/
```

La respuesta contiene:

```text
access
refresh
```

El `access token` tiene una duración de 30 minutos.

El `refresh token` tiene una duración de 1 día.

Para generar un nuevo access token se utiliza:

```text
POST /api/jwt/refresh/
```

La configuración utilizada es:

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
```

Esto permite utilizar tokens de corta duración y renovarlos sin volver a enviar las credenciales del usuario.

---

## Endpoints principales

| Método | Endpoint | Descripción | Código esperado |
|---|---|---|---|
| GET | `/api/registros/` | Lista los registros disponibles | 200 |
| POST | `/api/registros/` | Crea un registro | 201 |
| GET | `/api/registros/<id>/` | Consulta un registro individual | 200 |
| PUT | `/api/registros/<id>/` | Reemplaza un registro completo | 200 |
| PATCH | `/api/registros/<id>/` | Modifica parcialmente un registro | 200 |
| DELETE | `/api/registros/<id>/` | Realiza borrado lógico | 204 |
| POST | `/api/token/` | Obtiene un token tradicional | 200 |
| POST | `/api/jwt/` | Obtiene access y refresh JWT | 200 |
| POST | `/api/jwt/refresh/` | Genera un nuevo access token | 200 |

---

## Documentación Swagger

La API incluye documentación automática mediante `drf-spectacular`.

La interfaz Swagger se encuentra disponible en:

```text
http://127.0.0.1:8000/api/docs/
```

El esquema OpenAPI está disponible en:

```text
http://127.0.0.1:8000/api/schema/
```

Swagger permite visualizar los endpoints disponibles, sus métodos HTTP y la estructura de los datos utilizados por la API.

---

## Endpoints de documentación

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/docs/` | Interfaz Swagger |
| GET | `/api/schema/` | Esquema OpenAPI |

---

## Códigos de estado comprobados

Durante las pruebas de la API se comprobaron los siguientes códigos:

- `200 OK`: consultas y actualizaciones correctas.
- `201 Created`: creación correcta.
- `204 No Content`: eliminación correcta.
- `400 Bad Request`: datos inválidos.
- `401 Unauthorized`: petición sin autenticación.
- `403 Forbidden`: usuario autenticado sin permiso.
- `404 Not Found`: registro inexistente.

Las evidencias se encuentran en:

```text
pruebas/
```

---

## Serializer

La API utiliza:

```text
core/serializers.py
```

El serializer expone explícitamente los siguientes campos:

- `id`
- `nombre_lugar`
- `nivel_interes`
- `precio`
- `presupuesto`
- `resultado`
- `motivo`
- `fecha`
- `eliminado`
- `fecha_eliminacion`

No se utiliza:

```python
fields = "__all__"
```

porque se decidió controlar explícitamente qué campos expone la API.

---

## Campos de solo lectura

Los siguientes campos son de solo lectura:

- `resultado`
- `motivo`
- `fecha`
- `eliminado`
- `fecha_eliminacion`

`resultado` y `motivo` no pueden ser definidos libremente por el cliente.

Estos valores son calculados por la regla de negocio de GeekMatch Trips.

---

## Regla de decisión

La regla principal se mantiene en:

```text
solucion.py
```

La API reutiliza:

```python
from solucion import decidir
```

La lógica no se duplica dentro del ViewSet.

Durante CREATE y UPDATE se ejecuta nuevamente `decidir()` utilizando:

- nivel de interés;
- precio;
- presupuesto.

Durante una prueba PATCH se modificó el nivel de interés de un registro a:

```text
1
```

y el resultado fue recalculado automáticamente a:

```text
No recomendado por baja afinidad
```

Esto demuestra que la API reutiliza correctamente la misma regla de negocio de la aplicación original.

---

## Validaciones de la API

La API valida los datos antes de guardarlos.

Se comprueba que:

- el nombre del lugar no esté vacío;
- el nivel de interés esté entre 1 y 5;
- el precio no sea negativo;
- el presupuesto no sea negativo.

Cuando los datos no cumplen estas reglas, la API responde:

```text
400 Bad Request
```

y entrega un mensaje explicando el error.

Por ejemplo, durante las pruebas un nivel de interés igual a `99` fue rechazado correctamente.

---

## Borrado lógico

La operación DELETE de la API no elimina físicamente los registros de SQLite.

Cuando se ejecuta:

```text
DELETE /api/registros/<id>/
```

se utiliza:

```python
soft_delete()
```

El registro queda marcado con:

```text
eliminado = True
```

y se almacena:

```text
fecha_eliminacion
```

La API deja de mostrar estos registros porque el ViewSet consulta únicamente registros con:

```python
eliminado=False
```

Durante las pruebas se comprobó directamente desde Django que el registro continuaba existiendo en la base de datos después del DELETE.

---

## Permisos diferenciados

Los permisos de la API se encuentran en:

```text
core/permissions.py
```

Se mantienen los roles utilizados en GeekMatch Trips.

### viewer

Puede realizar:

- GET.

No puede realizar:

- POST;
- PUT;
- PATCH;
- DELETE.

Si intenta realizar una operación no permitida recibe:

```text
403 Forbidden
```

### normal

Puede realizar:

- GET;
- POST.

No puede realizar:

- PUT;
- PATCH;
- DELETE.

Si intenta modificar o eliminar recibe:

```text
403 Forbidden
```

### admin

Puede realizar todas las operaciones disponibles en la API.

Esto permite distinguir:

```text
401 Unauthorized
```

cuando no existe autenticación válida,

de:

```text
403 Forbidden
```

cuando el usuario está autenticado pero no posee autorización para realizar la operación.

---

## Configuración de Django REST Framework

La configuración principal se encuentra en:

```text
geekmatch/settings.py
```

Actualmente se utiliza:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
```

### Justificación de la autenticación

Se utilizan mecanismos de autenticación porque la API debe identificar quién realiza cada petición.

Token Authentication se mantiene para conservar compatibilidad con las pruebas originales.

JWT agrega tokens con expiración y refresco, mejorando el control de las credenciales.

### Justificación de IsAuthenticated

Se utiliza:

```text
IsAuthenticated
```

como permiso por defecto para evitar que los endpoints queden abiertos accidentalmente.

Después se aplican permisos específicos según el rol del usuario.

### Justificación de la paginación

La paginación evita devolver todos los registros en una única respuesta cuando aumenta la cantidad de información.

Se utiliza:

```text
PAGE_SIZE = 10
```

para entregar los registros en grupos pequeños y mantener controlado el tamaño de las respuestas JSON.

### Justificación de AutoSchema

Se utiliza:

```text
drf_spectacular.openapi.AutoSchema
```

para generar automáticamente el esquema OpenAPI utilizado por Swagger.

---

## Evidencias de pruebas

Las evidencias se encuentran en:

```text
pruebas/
```

Las principales pruebas realizadas son:

```text
01_sin_token_401.png
02_get_con_token_200.png
03_post_201.png
04_post_invalido_400.png
05_id_inexistente_404.png
06_delete_204.png
07_borrado_logico_verificado.png
08_get_detalle_200.png
09_patch_recalculo_200.png
10_viewer_post_403.png
11_normal_post_201.png
12_normal_patch_403.png
13_swagger_docs.png
14_swagger.png
15_jwt_refresh.png
```

Estas pruebas permiten comprobar:

- autenticación;
- lectura;
- creación;
- actualización;
- eliminación;
- validaciones;
- manejo de errores;
- borrado lógico;
- permisos diferenciados;
- documentación Swagger;
- generación de JWT;
- refresh de JWT.

---

## Seguridad

Se aplicaron las siguientes medidas:

- `.env` no se almacena en Git;
- `db.sqlite3` no se almacena en Git;
- `.venv` no se almacena en Git;
- las contraseñas reales no se escriben en README;
- los tokens reales no se escriben en el código;
- los tokens no se incluyen dentro de las URLs;
- la API requiere autenticación;
- los permisos se validan en el servidor;
- los campos calculados son de solo lectura;
- el serializer valida los datos recibidos;
- JWT utiliza access tokens con expiración;
- el refresh token permite renovar el acceso sin volver a enviar la contraseña.

---

## Estructura principal de la ES3

```text
core/
    api_views.py
    permissions.py
    serializers.py
    models.py
    views.py
    tests.py

geekmatch/
    settings.py
    urls.py

pruebas/

solucion.py
README.md
ia.md
requirements.txt
manage.py
```

La ES3 mantiene además:

- modelos;
- migraciones;
- Django Admin;
- templates;
- vistas HTML;
- autenticación de la ES2.

---

## Pruebas automáticas

Para ejecutar las pruebas:

```powershell
python manage.py test
```

El proyecto cuenta actualmente con 3 pruebas automáticas.

El resultado esperado es:

```text
Ran 3 tests
OK
```

Para comprobar que los modelos y migraciones se encuentran sincronizados:

```powershell
python manage.py makemigrations --check --dry-run
```

Resultado esperado:

```text
No changes detected
```

---

## Estado final del proyecto

Se comprobó que:

- las pantallas HTML de la ES2 continúan funcionando;
- Django REST Framework está instalado;
- SQLite continúa siendo la base de datos;
- las migraciones están aplicadas;
- no existen migraciones pendientes;
- `/api/registros/` exige autenticación;
- los endpoints CRUD funcionan;
- las validaciones devuelven errores comprensibles;
- los códigos HTTP esperados fueron comprobados;
- los permisos `viewer`, `normal` y `admin` están diferenciados;
- el borrado continúa siendo lógico;
- la regla `decidir()` se reutiliza desde `solucion.py`;
- Swagger documenta automáticamente la API;
- JWT genera access y refresh tokens;
- el refresh token genera correctamente un nuevo access token;
- las pruebas automáticas continúan funcionando después de agregar la API.