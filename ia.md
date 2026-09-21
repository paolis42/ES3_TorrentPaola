# Uso de Inteligencia Artificial - GeekMatch Trips

## Herramientas utilizadas

Durante el desarrollo de GeekMatch Trips utilicé las siguientes herramientas de apoyo:

- ChatGPT, para realizar consultas, recibir explicaciones, revisar código y comprender los pasos necesarios para implementar la evaluación.
- GitHub Copilot, como apoyo dentro de Visual Studio Code mediante sugerencias de código.

La IA fue utilizada como herramienta de consulta y apoyo. Las propuestas fueron revisadas, adaptadas al proyecto y probadas manualmente antes de ser incorporadas.

---

## Trabajo realizado y comprobado durante el desarrollo

Durante la evaluación trabajé directamente desde Visual Studio Code y fui probando el funcionamiento de cada parte del proyecto.

Entre las tareas realizadas y verificadas se encuentran:

- configuración del entorno virtual;
- instalación y uso de Django;
- creación y modificación del modelo `Registro`;
- creación y ejecución de migraciones;
- uso de SQLite;
- comprobación de migraciones pendientes;
- configuración de Django Admin;
- configuración del usuario administrador;
- prueba del buscador y filtros del administrador;
- implementación del CRUD;
- creación de registros;
- edición de registros;
- recálculo del resultado después de editar;
- implementación y comprobación del borrado lógico;
- implementación de inicio y cierre de sesión;
- creación de los grupos `admin`, `normal` y `viewer`;
- creación de usuarios de prueba;
- comprobación de restricciones mediante acceso directo a las URLs;
- comprobación de respuestas `403 Forbidden`;
- validación de datos en el servidor;
- creación de pruebas automáticas;
- ejecución de `python manage.py test`;
- actualización del repositorio GitHub durante el desarrollo.

---

# Consultas realizadas a la IA

## 1. Consulta sobre el modelo y SQLite

### Pregunta realizada

> ¿Cómo adapto el modelo de la guía a GeekMatch Trips para guardar nombre del lugar, nivel de interés, precio, presupuesto, resultado y motivo en SQLite?

### Respuesta de la IA

La IA propuso crear un modelo de Django llamado `Registro` y convertir los datos que anteriormente se guardaban en `datos.json` en campos del modelo.

También sugirió utilizar tipos de campo de Django según el tipo de dato:

- `CharField` para textos;
- `IntegerField` para los valores numéricos;
- `DateTimeField` para las fechas;
- `BooleanField` para indicar si un registro fue eliminado.

Después propuso crear las tablas mediante:

`python manage.py makemigrations`

y:

`python manage.py migrate`

### Qué corregí o adapté

No utilicé directamente los nombres de campos genéricos que aparecían en algunos ejemplos.

El modelo fue adaptado específicamente a GeekMatch Trips utilizando:

- `nombre_lugar`;
- `nivel_interes`;
- `precio`;
- `presupuesto`;
- `resultado`;
- `motivo`;
- `fecha`;
- `eliminado`;
- `fecha_eliminacion`.

También incorporé borrado lógico mediante `soft_delete()` para que los registros no sean eliminados físicamente de la base de datos.

Después comprobé que las migraciones estuvieran sincronizadas ejecutando:

`python manage.py makemigrations --check --dry-run`

El resultado fue:

`No changes detected`

---

## 2. Consulta sobre la reutilización de la regla de decisión

### Pregunta realizada

> ¿Debo copiar los if y elif de la función decidir() dentro de las vistas de Django?

### Respuesta de la IA

La IA indicó que no era necesario copiar nuevamente la regla de decisión.

Propuso mantener la función `decidir()` dentro de `solucion.py` y reutilizarla desde Django mediante:

`from solucion import decidir`

### Qué corregí o adapté

Revisé que la cadena de `if`, `elif` y `else` no quedara repetida dentro de `views.py`.

La regla se mantuvo solamente en `solucion.py`.

También comprobé que `decidir()` se ejecutara nuevamente durante la edición de un registro, porque modificar:

- nivel de interés;
- precio;
- presupuesto;

puede cambiar el resultado.

Durante las pruebas se comprobó que al reducir el nivel de interés de un registro, el resultado cambiara desde `Recomendado` a `No recomendado por baja afinidad`.

---

## 3. Consulta sobre el cambio desde JSON a SQLite

### Pregunta realizada

> Mi views.py todavía tiene import json, datos.json y settings.BASE_DIR. ¿Debo mantener eso ahora que la evaluación pide SQLite?

### Respuesta de la IA

La IA explicó que `datos.json` pertenecía a la versión anterior y que las nuevas vistas debían utilizar el modelo `Registro` mediante Django ORM.

Propuso reemplazar la lectura y escritura del JSON por operaciones como:

- `Registro.objects.create()`;
- `Registro.objects.filter()`;
- `registro.save()`.

### Qué corregí o adapté

Eliminé de las vistas el almacenamiento mediante JSON.

`datos.json` dejó de ser la fuente principal de persistencia y los registros pasaron a almacenarse en SQLite.

Se mantuvo `datos.json` únicamente como archivo de datos anteriores y se creó `cargar_datos.py` para poder importar esos registros a SQLite.

---

## 4. Consulta sobre CRUD

### Pregunta realizada

> ¿Cómo organizo CREATE, READ, UPDATE y DELETE usando el modelo Registro sin volver a escribir la función decidir()?

### Respuesta de la IA

La IA propuso separar las operaciones en cuatro vistas:

- `lista`;
- `crear`;
- `editar`;
- `eliminar`.

Para CREATE y UPDATE sugirió llamar nuevamente a `decidir()` antes de guardar.

Para DELETE sugirió utilizar el método de borrado lógico del modelo.

### Qué corregí o adapté

Implementé las cuatro operaciones y las probé manualmente.

Para CREATE comprobé que se crearan nuevos registros en SQLite.

Para READ comprobé que solo aparecieran los registros con:

`eliminado=False`

Para UPDATE comprobé que el resultado se recalculara automáticamente.

Para DELETE comprobé que el registro desapareciera de la lista normal, pero siguiera existiendo en la base de datos con:

`eliminado=True`

y una fecha en:

`fecha_eliminacion`.

Posteriormente detecté que parte de la lectura de los datos POST estaba duplicada entre `crear` y `editar`.

Para disminuir esa duplicación se creó una función compartida:

`leer_datos_formulario()`

que se utiliza en ambas vistas.

---

## 5. Consulta sobre login y roles

### Pregunta realizada

> ¿Cómo puedo utilizar los grupos de Django para tener los roles admin, normal y viewer sin crear mi propio sistema de contraseñas?

### Respuesta de la IA

La IA recomendó utilizar el sistema de autenticación que Django ya incluye y crear los grupos:

- `admin`;
- `normal`;
- `viewer`.

También indicó que los permisos no debían depender solamente de ocultar botones en las plantillas.

### Qué corregí o adapté

Inicialmente ocultar los botones según el usuario parecía suficiente.

Después comprendí que eso no representa seguridad real porque una persona puede escribir directamente una URL en el navegador.

Por ese motivo las restricciones se implementaron también dentro de las vistas del servidor.

Cuando un usuario intenta realizar una acción para la que no tiene autorización, la vista utiliza:

`raise PermissionDenied`

Las pruebas realizadas fueron:

### viewer

Puede:

- iniciar sesión;
- visualizar registros.

Recibe `403 Forbidden` al intentar:

- crear;
- editar;
- eliminar.

### normal

Puede:

- iniciar sesión;
- visualizar;
- crear.

Recibe `403 Forbidden` al intentar:

- editar;
- eliminar.

### admin

Puede:

- visualizar;
- crear;
- editar;
- eliminar.

Después de una revisión adicional también se corrigió `crear_usuarios.py`.

La primera versión agregaba al usuario al grupo `admin`, pero eso no le daba automáticamente acceso al panel administrativo de Django.

Se corrigió configurando al usuario administrador con:

- `is_staff=True`;
- `is_superuser=True`.

Después de este cambio comprobé que el usuario `admin` pudiera ingresar correctamente a:

`/admin/`

---

## 6. Consulta sobre validaciones

### Pregunta realizada

> ¿Es suficiente validar los campos con required en el formulario HTML y dejar que decidir() marque los datos inválidos?

### Respuesta de la IA

En una primera versión las validaciones principales estaban en el formulario HTML y se utilizaba `try/except` para evitar errores al convertir los valores numéricos mediante `int()`.

La función `decidir()` también podía devolver:

`Dato inválido`

si los valores estaban fuera de rango.

### Qué corregí o adapté

Posteriormente se comprobó que las validaciones HTML pueden evitarse enviando una petición directamente al servidor.

Por ejemplo, era posible enviar:

- nombre vacío;
- interés `99`;
- precio `-500`.

Aunque `decidir()` marcaba esos valores como inválidos, el registro igualmente podía guardarse.

Por ese motivo agregué validaciones directamente en `views.py` antes de realizar `Registro.objects.create()` o `save()`.

Actualmente el servidor rechaza:

- nombre vacío;
- nivel de interés menor que 1;
- nivel de interés mayor que 5;
- precio negativo;
- presupuesto negativo;
- valores numéricos que no puedan convertirse a entero.

Durante las pruebas comprobé que:

`nivel_interes=99`

mostrara:

`El nivel de interés debe estar entre 1 y 5.`

También comprobé que:

`precio=-500`

mostrara:

`El precio no puede ser negativo.`

El registro no se guarda mientras exista un error de validación.

---

## 7. Consulta sobre pruebas automáticas

### Pregunta realizada

> ¿Qué pruebas automáticas mínimas puedo agregar para comprobar la regla de decisión, los permisos y el borrado lógico?

### Respuesta de la IA

La IA propuso agregar pruebas mediante `django.test.TestCase`.

Se seleccionaron tres casos diferentes:

1. comprobar una rama de `decidir()`;
2. comprobar que un usuario sin permiso reciba `403`;
3. comprobar que el borrado lógico no elimine físicamente la fila.

### Qué corregí o adapté

Hasta ese momento las pruebas estaban realizadas principalmente de forma manual y `python manage.py test` ejecutaba cero pruebas.

Por este motivo agregué tres pruebas dentro de:

`core/tests.py`

Las pruebas verifican:

### Test 1 - Regla de decisión

Comprueba que una actividad con alto interés y dentro del presupuesto obtenga:

`Recomendado`

### Test 2 - Permisos

Comprueba que un usuario perteneciente al grupo `viewer` reciba:

`HTTP 403`

al intentar acceder a la vista de creación.

### Test 3 - Borrado lógico

Comprueba que después de ejecutar `soft_delete()`:

- `eliminado` sea `True`;
- `fecha_eliminacion` tenga un valor;
- el registro siga existiendo físicamente en la base de datos.

Después ejecuté:

`python manage.py test`

El resultado fue:

`Found 3 test(s).`

`Ran 3 tests`

`OK`

---

# Otras correcciones realizadas

## Corrección de un nombre de campo

Durante el desarrollo apareció una referencia incorrecta:

`nivel_interres`

Se corrigió por:

`nivel_interes`

para que coincidiera con el nombre real del campo.

---

## Validación de números

Se utiliza `try/except` al convertir los valores enviados por el formulario.

Esto evita que la aplicación termine con un error si se intenta ingresar texto en un campo que debe ser numérico.

Además de la conversión, actualmente existen validaciones de rango en el servidor.

---

## Configuración del administrador

El modelo `Registro` fue configurado en Django Admin con:

- columnas personalizadas;
- filtro por resultado;
- filtro por eliminado;
- buscador por nombre;
- fechas de solo lectura.

También se corrigió el usuario creado mediante `crear_usuarios.py` para permitir que el usuario `admin` pueda ingresar al administrador.

---

## Seguridad de información sensible

La `SECRET_KEY` y las contraseñas utilizadas por los usuarios de prueba se almacenan dentro del archivo:

`.env`

Este archivo está excluido mediante `.gitignore`.

El archivo:

`.env.example`

solo contiene los nombres de las variables y no incluye contraseñas reales.

---

# Pruebas realizadas

## Base de datos

Se comprobó:

- creación de migraciones;
- ejecución de migraciones;
- funcionamiento sobre SQLite;
- ausencia de migraciones pendientes;
- creación de la base desde un clon limpio.

## Django Admin

Se comprobó:

- visualización del modelo `Registro`;
- columnas personalizadas;
- buscador por nombre;
- filtros;
- acceso del usuario administrador.

## CRUD

Se comprobó:

- creación;
- visualización;
- edición;
- recálculo del resultado;
- borrado lógico.

## Validaciones

Se comprobó que no se guarden:

- intereses fuera del rango 1 a 5;
- precios negativos;
- presupuestos negativos;
- nombres vacíos.

## Autenticación y autorización

Se comprobó:

- inicio de sesión;
- cierre de sesión;
- restricciones según rol;
- acceso directo mediante URL;
- respuestas `403 Forbidden`.

## Pruebas automáticas

Se ejecutó:

`python manage.py test`

Resultado:

`Ran 3 tests`

`OK`

---

# Conclusión sobre el uso de IA

La inteligencia artificial fue utilizada como herramienta de apoyo durante el desarrollo de GeekMatch Trips.

Se utilizó principalmente para:

- resolver dudas;
- comprender conceptos de Django;
- revisar estructuras de código;
- comprender migraciones;
- organizar el CRUD;
- implementar autenticación;
- comprender grupos y permisos;
- detectar duplicación;
- implementar validaciones;
- proponer pruebas automáticas.

Las respuestas no fueron incorporadas automáticamente.

Las propuestas fueron revisadas y adaptadas al proyecto, y en distintos momentos fue necesario corregirlas o complementarlas.

Entre las correcciones más importantes se encuentran:

- no depender solamente de botones ocultos para proteger acciones;
- proteger las vistas mediante permisos del servidor;
- configurar correctamente al usuario `admin` para acceder a Django Admin;
- mover las validaciones desde el navegador hacia el servidor;
- evitar duplicar la lectura del formulario entre CREATE y UPDATE;
- agregar pruebas automáticas que puedan ejecutarse mediante `manage.py test`.

El proyecto evolucionó desde una primera versión que utilizaba `datos.json` hacia una aplicación Django con SQLite, CRUD, borrado lógico, autenticación, roles, validaciones del lado del servidor y pruebas automáticas.