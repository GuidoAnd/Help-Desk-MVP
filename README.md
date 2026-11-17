# Mesa de ayuda

Aplicación de consola para la administracion de tickets.

## Instalación y ejecución

La aplicación utiliza Python 3.13.5 y las siguientes bibliotecas externas:

- `tabulate`: presenta los tickets en tablas.
- `questionary`: menú, selección de prioridades y estados, entrada de datos y confirmaciones.
- `colorama`: colores para estados y mensajes en terminal, también en Windows.

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 main.py
```

### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Uso, datos y manejo de errores

Para su uso: seleccionar opciones con las flecha interactiva y confirmar con Enter en una terminal interactiva.

1. **Crear ticket**: ingresar título, descripción y prioridad (`alta`, `media` o `baja`).
2. **Listar tickets**: mostrar sus seis campos en tabla, ordenados por prioridad.
3. **Filtrar tickets**: elegir prioridad o estado y seleccionar su valor.
4. **Buscar ticket por ID**: ingresar un entero positivo para ver todos sus datos.
5. **Modificar ticket**: abrir el submenú de edición y cambio de estado.
   5.1 **Editar ticket**: consultar la tabla de ID y título, ingresar el ID y elegir
   título, descripción o prioridad.
   5.2 **Cambiar estado**: consultar la tabla de ID y título, ingresar el ID y elegir
   el siguiente estado permitido: `abierto → en_curso → resuelto`.
6. **Eliminar ticket**: consultar la tabla de ID y título, ingresar un ID, ver sus
   datos completos y confirmar explícitamente; por defecto se propone No.
7. **Salir**: guardar y terminar.
 

Los resultados filtrados también se ordenan por prioridad. El filtro admite
un criterio por consulta; no combina prioridad y estado. Si no hay coincidencias,
se informa en pantalla. Elegir «Cancelar» en cualquiera de las dos selecciones
vuelve al menú. Estas consultas no modifican el JSON, el contador ni los logs.

Si no hay tickets o el ID es inválido o inexistente, se informa y se vuelve al
menú desde el que se inició la operación. Cancelar una pregunta con Ctrl+C
vuelve a ese menú sin guardar cambios de esa operación.
Cancelar el menú cierra la sesión. Las operaciones ya confirmadas se conservan.

Los estados se muestran con texto y color: abierto en amarillo, en_curso en cian
y resuelto en verde. Los mensajes conservan su significado sin color; cuando la
salida está redirigida se omiten los códigos de color propios de la aplicación.

Los archivos se crean junto a `main.py`. `tickets.json` contiene el contador
histórico `ultimo_id` y la lista `tickets` en un mismo objeto JSON.
`helpdesk.log` registra creaciones, ediciones, cambios de estado y eliminaciones después
de guardar los datos. Cada modificación guarda la colección y su contador juntos
mediante un archivo temporal y reemplazo del destino. Eliminar tickets no reduce
el contador histórico.

Los IDs guardados no se reutilizan aunque se eliminen tickets. Conservar y
respaldar `tickets.json`; no reducir ni borrar su campo `ultimo_id`.
Si los datos están dañados, el programa informa el error y se detiene.

## Limitaciones

Uso local con una sola instancia; no admite acceso concurrente. El registro de
logs y el guardado de datos no forman una transacción única.
La edición modifica un campo por operación y no permite cambiar ID, fecha ni
estado directamente. No permite reaperturas. No incluye
autenticación, copias de seguridad automáticas ni exportación de datos.
El menú requiere una terminal interactiva; no ofrece una interfaz para scripts.

## Organización

- `main.py`: interacción y coordinación del menú.
- `tickets.py`: creación, búsqueda, filtrado, ordenación, edición, transiciones y
  eliminación separadas de la consola.
- `archivo.py`: lectura, validación, migración y guardado conjunto de tickets e IDs.
- `requirements.txt`: bibliotecas externas y sus versiones.
- `bin`: directorio donde se encuentran los ejecutables. 

## Versiones

| Versión | Estado | Descripción |
| --- | --- | --- |
| v0.1 | Implementada | Version base del sistema de tickets |
| v0.2 | Implementada | Filtrado, orden por prioridad, ayuda visual, submenú de modificación, edición y ejecutables|

Mejoras implementadas en v0.2:

- Filtrar por una prioridad (`alta`, `media`, `baja`) o un estado
  (`abierto`, `en_curso`, `resuelto`) en cada consulta.
- Mostrar los listados en orden `alta → media → baja`, conservando el orden
  relativo de los tickets con igual prioridad.
- Mostrar ID y título antes de eliminar, editar o cambiar de estado.
- Agrupar edición y cambio de estado en «Modificar ticket», con regreso al menú.
- Editar título, descripción o prioridad sin cambiar los datos históricos.
- Ejecutables para Linux y Windows
- Mostrar la versión de la aplicación al iniciar.
