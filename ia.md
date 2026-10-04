# Uso de Inteligencia Artificial - GeekMatch Trips ES3

## Herramientas utilizadas

Durante el desarrollo de la ES3 de GeekMatch Trips utilicé:

- ChatGPT, para realizar consultas, comprender Django REST Framework, revisar código y apoyar las pruebas de la API.
- GitHub Copilot, como apoyo mediante sugerencias dentro de Visual Studio Code.

La inteligencia artificial fue utilizada como herramienta de apoyo. Las propuestas fueron revisadas, adaptadas y probadas antes de incorporarlas al proyecto.

---

## Consulta 1: Serializer y campos expuestos

### Qué le pedí a la IA

Pregunté cómo transformar el modelo `Registro` de GeekMatch Trips en un serializer para poder entregar y recibir información mediante JSON.

### Qué respondió la IA

La IA propuso utilizar `ModelSerializer` de Django REST Framework y enumerar los campos que serían expuestos por la API.

También recomendó marcar como `read_only` los campos que no deberían ser definidos directamente por el cliente.

### Qué revisé o corregí

No utilicé:

```python
fields = "__all__"
```

porque eso expondría automáticamente todos los campos del modelo.

Preferí enumerarlos explícitamente:

```python
fields = [
    "id",
    "nombre_lugar",
    "nivel_interes",
    "precio",
    "presupuesto",
    "resultado",
    "motivo",
    "fecha",
    "eliminado",
    "fecha_eliminacion",
]
```

Además se definieron como solo lectura:

```python
read_only_fields = [
    "resultado",
    "motivo",
    "fecha",
    "eliminado",
    "fecha_eliminacion",
]
```

### Qué hice finalmente

Creé:

```text
core/serializers.py
```

con validaciones para:

- nombre obligatorio;
- interés entre 1 y 5;
- precio no negativo;
- presupuesto no negativo.

Durante las pruebas comprobé que un nivel de interés igual a `99` fuera rechazado con:

```text
400 Bad Request
```

y un mensaje indicando el problema.

---

## Consulta 2: Cómo reutilizar decidir() desde la API

### Qué le pedí a la IA

Consulté cómo hacer que la API siguiera utilizando la regla de negocio de GeekMatch Trips sin volver a escribir los `if` y `elif` dentro del ViewSet.

### Qué respondió la IA

La IA recomendó importar la función existente:

```python
from solucion import decidir
```

y ejecutarla dentro de las operaciones de creación y actualización.

Para CREATE se propuso utilizar:

```python
perform_create()
```

y para UPDATE:

```python
perform_update()
```

### Qué revisé o corregí

Comprobé que la API no aceptara `resultado` y `motivo` enviados por el cliente.

Esos campos debían continuar siendo calculados por el proyecto.

También fue necesario considerar PATCH, porque en una actualización parcial no siempre llegan todos los campos.

Por este motivo, en `perform_update()` se utilizan los valores nuevos cuando existen y los valores anteriores cuando un campo no fue enviado.

### Qué hice finalmente

El ViewSet ejecuta nuevamente `decidir()` tanto al crear como al actualizar.

Se realizó una prueba PATCH modificando:

```text
nivel_interes = 1
```

El resultado fue recalculado automáticamente a:

```text
No recomendado por baja afinidad
```

Esto confirmó que la API sigue utilizando la misma regla de negocio de la aplicación original.

---

## Consulta 3: Autenticación y seguridad de la API

### Qué le pedí a la IA

Consulté cómo proteger los endpoints de la API para que no pudieran ser utilizados sin autenticación y cómo mantener los roles `viewer`, `normal` y `admin`.

### Qué respondió la IA

La IA recomendó utilizar:

```python
TokenAuthentication
```

junto con:

```python
IsAuthenticated
```

También se propuso crear una clase personalizada de permisos para diferenciar las operaciones permitidas según el grupo del usuario.

### Qué estaba incompleto

Utilizar únicamente:

```python
IsAuthenticated
```

permite comprobar que el usuario está autenticado, pero no diferencia qué operaciones puede realizar cada rol.

Un `viewer` autenticado podría intentar utilizar las mismas rutas que un `admin` si no existiera una segunda validación.

También comprendí que ocultar botones en HTML no sirve como protección para una API, porque las peticiones se pueden enviar directamente.

### Qué hice finalmente

Creé:

```text
core/permissions.py
```

con una clase:

```python
PermisosRegistro
```

Los permisos quedaron definidos así:

### viewer

Puede:

- GET.

No puede:

- POST;
- PUT;
- PATCH;
- DELETE.

### normal

Puede:

- GET;
- POST.

No puede:

- PUT;
- PATCH;
- DELETE.

### admin

Puede realizar todas las operaciones.

Se comprobó la diferencia entre:

```text
401 Unauthorized
```

cuando no se envía autenticación,

y:

```text
403 Forbidden
```

cuando el usuario está autenticado pero no tiene permiso.

Por ejemplo, `viewer` recibió `403` al intentar hacer POST y `normal` recibió `403` al intentar hacer PATCH.

---

## Consulta 4: Uso del token desde PowerShell

### Qué le pedí a la IA

Consulté cómo obtener los tokens de los usuarios y utilizarlos para probar los endpoints desde PowerShell.

### Qué respondió la IA

La IA propuso guardar el token en una variable y crear una cabecera:

```powershell
$headers = @{
    Authorization = "Token TOKEN"
}
```

### Qué problema encontré

Al obtener el token mediante:

```text
python manage.py shell -c ...
```

la salida de Django incluía texto adicional.

Al guardar toda esa salida dentro de una variable, el token contenía espacios y Django REST Framework no lo reconocía correctamente.

### Qué corregí

Se modificó el comando para conservar solamente la última línea y eliminar espacios:

```powershell
Select-Object -Last 1
```

y:

```powershell
.Trim()
```

Después se comprobó que la longitud del token fuera la esperada antes de utilizarlo.

### Qué hice finalmente

Los tokens fueron utilizados únicamente mediante la cabecera:

```text
Authorization: Token TOKEN_DEL_USUARIO
```

No se almacenaron tokens reales en el código, README ni URLs.

---

## Consulta 5: Borrado mediante DELETE

### Qué le pedí a la IA

Consulté cómo adaptar DELETE de Django REST Framework para mantener el borrado lógico que ya tenía GeekMatch Trips.

### Qué respondió la IA

La operación DELETE estándar de un `ModelViewSet` elimina físicamente el registro.

La propuesta fue sobrescribir:

```python
destroy()
```

y ejecutar el método existente:

```python
soft_delete()
```

### Qué revisé

No quería cambiar el comportamiento que ya había sido implementado y probado en la ES2.

El registro debía desaparecer de la API, pero seguir existiendo en SQLite.

### Qué hice finalmente

La operación DELETE ejecuta:

```python
registro.soft_delete()
```

y responde:

```text
204 No Content
```

Después se verificó directamente en Django que el registro todavía existiera y tuviera:

```text
eliminado = True
```

junto con una fecha en:

```text
fecha_eliminacion
```

---

## Consulta 6: Documentación automática con Swagger

### Qué le pedí a la IA

Consulté cómo generar documentación automática para los endpoints de la API REST.

### Qué respondió la IA

La IA recomendó utilizar `drf-spectacular`, configurando un esquema OpenAPI y una interfaz Swagger.

Se agregaron las rutas:

```text
/api/schema/
/api/docs/
```

### Qué hice finalmente

Instalé:

```text
drf-spectacular
```

y configuré:

```python
"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema"
```

Después comprobé desde el navegador que Swagger mostrara correctamente los endpoints GET, POST, PUT, PATCH y DELETE de la API.

Las evidencias se encuentran en:

```text
pruebas/13_swagger_docs.png
pruebas/14_swagger.png
```

---

## Consulta 7: JWT con expiración y refresh

### Qué le pedí a la IA

Consulté cómo agregar autenticación mediante JWT sin eliminar el sistema de Token Authentication que ya funcionaba.

### Qué respondió la IA

La IA recomendó utilizar:

```text
djangorestframework-simplejwt
```

y mantener ambos sistemas de autenticación para conservar compatibilidad con las pruebas anteriores.

### Qué revisé o corregí

Inicialmente la configuración de autenticación quedó con `TokenAuthentication` repetido dos veces.

Se corrigió para utilizar:

```python
"DEFAULT_AUTHENTICATION_CLASSES": [
    "rest_framework_simplejwt.authentication.JWTAuthentication",
    "rest_framework.authentication.TokenAuthentication",
]
```

De esta forma se mantuvo el sistema anterior y se agregó JWT.

### Qué hice finalmente

Se configuraron los tiempos de duración:

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
```

Se agregaron los endpoints:

```text
POST /api/jwt/
POST /api/jwt/refresh/
```

Durante las pruebas se comprobó que `/api/jwt/` entregara:

```text
refresh
access
```

y que el refresh token permitiera obtener posteriormente un nuevo:

```text
access
```

La evidencia final se encuentra en:

```text
pruebas/15_jwt_refresh.png
```

### Consideración de seguridad

Los tokens JWT y las contraseñas reales no se almacenaron en el código ni en las evidencias finales.

Para la evidencia final se mostró únicamente que las propiedades `access` y `refresh` fueron generadas correctamente, sin mostrar el contenido de los tokens.

---

# Pruebas realizadas con apoyo de IA

Durante el desarrollo se realizaron pruebas sobre los endpoints.

Se comprobaron los siguientes códigos:

```text
200 OK
201 Created
204 No Content
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
```

Entre las pruebas realizadas se encuentran:

- acceso sin token;
- GET autenticado;
- POST correcto;
- POST con datos inválidos;
- consulta de ID inexistente;
- DELETE;
- comprobación del borrado lógico;
- GET de detalle;
- PATCH con recálculo;
- POST prohibido para `viewer`;
- POST permitido para `normal`;
- PATCH prohibido para `normal`;
- documentación Swagger;
- generación de JWT;
- renovación del access token mediante refresh.

Las evidencias quedaron almacenadas dentro de:

```text
pruebas/
```

---

# Evaluación crítica del uso de IA

Las respuestas de inteligencia artificial no se incorporaron automáticamente.

Durante el trabajo fue necesario:

- adaptar los ejemplos genéricos al modelo real de GeekMatch Trips;
- mantener la función `decidir()` en lugar de duplicar la lógica;
- controlar explícitamente los campos expuestos por el serializer;
- evitar depender únicamente de `IsAuthenticated`;
- implementar permisos según los grupos existentes;
- corregir la forma en que PowerShell obtenía y almacenaba el token;
- comprobar manualmente los códigos HTTP;
- mantener el borrado lógico de la ES2;
- corregir la configuración inicial de JWT;
- comprobar Swagger desde el navegador;
- comprobar el funcionamiento del refresh JWT;
- evitar incluir tokens y credenciales reales en la documentación.

La IA fue útil para explicar herramientas y proponer estructuras, pero cada propuesta fue revisada mediante pruebas antes de considerarse parte de la solución final.

---

# Conclusión

La inteligencia artificial permitió apoyar la evolución de GeekMatch Trips desde una aplicación Django con vistas HTML hacia una aplicación que además ofrece una API RESTful.

La solución final mantiene las funcionalidades de la ES2 y agrega:

- Django REST Framework;
- serializers;
- ViewSet;
- router;
- JSON;
- Token Authentication;
- JWT con expiración y refresh;
- permisos diferenciados;
- validaciones;
- códigos HTTP;
- paginación;
- documentación Swagger/OpenAPI;
- pruebas mediante cliente HTTP;
- evidencias de funcionamiento.

Las decisiones finales fueron tomadas después de revisar, adaptar y probar las propuestas recibidas.