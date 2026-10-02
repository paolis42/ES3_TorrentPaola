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

Las pantallas HTML desarrolladas en la ES2 continúan funcionando junto con la nueva API.

El login HTML está disponible en:

```text
http://127.0.0.1:8000/login/
```

---

# API REST

La API se encuentra bajo:

```text
/api/
```

Las pantallas HTML de la ES2 continúan funcionando en paralelo con la API.

---

## Autenticación

La API utiliza autenticación mediante token.

Para solicitar un token se utiliza:

```text
POST /api/token/
```

Después, el token debe enviarse en la cabecera de cada petición:

```text
Authorization: Token TOKEN_DEL_USUARIO
```

Los tokens reales no deben guardarse en el código, README ni repositorio.

---

## Endpoints

| Método | Endpoint | Descripción | Código esperado |
|---|---|---|---|
| GET | `/api/registros/` | Lista los registros | 200 |
| POST | `/api/registros/` | Crea un registro | 201 |
| GET | `/api/registros/<id>/` | Consulta un registro individual | 200 |
| PUT | `/api/registros/<id>/` | Reemplaza un registro completo | 200 |
| PATCH | `/api/registros/<id>/` | Modifica parcialmente un registro | 200 |
| DELETE | `/api/registros/<id>/` | Realiza borrado lógico | 204 |
| POST | `/api/token/` | Obtiene un token de autenticación | 200 |

---

## Códigos de estado comprobados

Durante las pruebas de la API se comprobaron los siguientes códigos:

- `200 OK`: consultas y actualizaciones correctas.
- `201 Created`: creación correcta.
- `204 No Content`: eliminación correcta.
- `400 Bad Request`: datos inválidos.
- `401 Unauthorized`: petición sin token.
- `403 Forbidden`: usuario autenticado sin permiso.
- `404 Not Found`: registro inexistente.

Las capturas de evidencia se encuentran dentro de:

```text
pruebas/
```

---

## Serializer

La API utiliza el archivo:

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

`resultado` y `motivo` no pueden ser enviados ni modificados libremente por el cliente.

Estos valores son calculados por la regla de negocio de GeekMatch Trips.

---

## Regla de decisión

La regla principal se mantiene en:

```text
solucion.py
```

La API reutiliza la función:

```python
from solucion import decidir
```

La lógica no se copia dentro del ViewSet.

Durante CREATE y UPDATE se ejecuta nuevamente `decidir()` utilizando:

- nivel de interés;
- precio;
- presupuesto.

Durante una prueba se cambió el nivel de interés de un registro desde un valor alto a `1`.

El resultado fue recalculado automáticamente a:

```text
No recomendado por baja afinidad
```

---

## Validaciones de la API

La API valida los datos antes de guardarlos.

Se comprueba que:

- el nombre del lugar no esté vacío;
- el nivel de interés esté entre 1 y 5;
- el precio no sea negativo;
- el presupuesto no sea negativo.

Cuando los datos no cumplen estas reglas, la API responde con:

```text
400 Bad Request
```

y entrega un mensaje indicando el error.

Por ejemplo, un nivel de interés igual a `99` fue rechazado correctamente.

---

## Borrado lógico

La operación DELETE de la API no elimina físicamente los registros de la base de datos.

Cuando se ejecuta:

```text
DELETE /api/registros/<id>/
```

se utiliza el método:

```python
soft_delete()
```

El registro queda marcado con:

```text
eliminado = True
```

y se guarda una fecha en:

```text
fecha_eliminacion
```

La API deja de mostrar estos registros porque el ViewSet consulta solamente los registros con:

```python
eliminado=False
```

Durante las pruebas se comprobó que el registro continuaba existiendo en SQLite después del DELETE.

---

## Permisos diferenciados

Los permisos de la API están definidos en:

```text
core/permissions.py
```

Se utilizan los mismos roles definidos para GeekMatch Trips.

### viewer

Puede realizar operaciones de lectura mediante GET.

Si intenta crear, editar o eliminar recibe:

```text
403 Forbidden
```

### normal

Puede realizar:

- GET
- POST

Si intenta modificar o eliminar mediante PATCH, PUT o DELETE recibe:

```text
403 Forbidden
```

### admin

Puede realizar todas las operaciones disponibles en la API.

Esto permite distinguir entre:

```text
401 Unauthorized
```

cuando no se proporciona un token válido,

y:

```text
403 Forbidden
```

cuando el usuario está autenticado pero no tiene permiso para realizar la operación.

---

## Configuración de Django REST Framework

La configuración principal se encuentra en:

```text
geekmatch/settings.py
```

Se utiliza:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "PAGE_SIZE": 10,
}
```

### Justificación de la autenticación

Se utiliza `TokenAuthentication` porque la API está diseñada para ser consumida por otros programas.

Cada petición debe identificarse mediante una credencial enviada en la cabecera HTTP.

Esto permite proteger los endpoints sin depender de la sesión HTML utilizada en la ES2.

### Justificación de IsAuthenticated

Se utiliza `IsAuthenticated` como permiso por defecto para evitar que los endpoints queden abiertos accidentalmente.

Después se aplican permisos diferenciados según el rol del usuario.

### Justificación de la paginación

La paginación evita devolver todos los registros en una única respuesta cuando aumenta la cantidad de datos.

Se utiliza:

```text
PAGE_SIZE = 10
```

para entregar los registros en grupos pequeños y mantener controlado el tamaño de las respuestas JSON.

---

## Evidencias de pruebas

Las evidencias se encuentran dentro de:

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
- permisos diferenciados.

---

## Seguridad

Se aplicaron las siguientes medidas:

- `.env` no se almacena en Git.
- `db.sqlite3` no se almacena en Git.
- `.venv` no se almacena en Git.
- los tokens reales no se escriben dentro del código;
- los tokens no se incluyen dentro de las URLs;
- la API requiere autenticación;
- los permisos se validan en el servidor;
- los campos calculados son de solo lectura;
- el serializer valida los datos recibidos.

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

La ES3 mantiene además los modelos, migraciones, Django Admin, templates y vistas HTML desarrollados anteriormente.

---

## Estado del proyecto

Se comprobó que:

- las pantallas HTML de la ES2 continúan funcionando;
- Django REST Framework está instalado;
- las migraciones están aplicadas;
- no existen migraciones pendientes;
- `/api/registros/` exige autenticación;
- los endpoints CRUD funcionan;
- las validaciones devuelven errores comprensibles;
- los códigos HTTP esperados fueron comprobados;
- los permisos `viewer`, `normal` y `admin` están diferenciados;
- el borrado continúa siendo lógico;
- la regla `decidir()` se reutiliza desde `solucion.py`.
