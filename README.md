# Mesa de ayuda

Aplicación de consola para crear, listar y buscar tickets por ID.
El ID, el estado `abierto` y la fecha se asignan automáticamente.

## Instalación y ejecución

La aplicación utiliza Python 3.13.5 y `tabulate` para presentar los tickets
en tablas legibles. La versión está fijada en `requirements.txt`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 main.py
```

```Powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Uso, datos y manejo de errores

- Opción 1: ingresar título, descripción y prioridad (`alta`, `media` o `baja`).
- Opción 2: listar todos los tickets en una tabla con sus seis campos.
- Opción 3: buscar un ticket por su ID y mostrar todos sus datos.
- Opción 4: guardar y salir.

Si no hay tickets se informa en pantalla. La búsqueda requiere un ID entero
positivo; si el ID no existe, se informa y se vuelve al menú.

Los archivos se crean junto a `main.py`. `tickets.json` contiene el contador
histórico `ultimo_id` y la lista `tickets` en un mismo objeto JSON.
`helpdesk.log` registra las creaciones. Cada creación guarda la colección y su
contador juntos mediante un archivo temporal y reemplazo del destino.

Los IDs guardados no se reutilizan aunque se eliminen tickets. Conservar y
respaldar `tickets.json`; no reducir ni borrar su campo `ultimo_id`.
Si los datos están dañados, el programa informa el error y se detiene.

## Limitaciones y mejoras

Uso local con una sola instancia; no admite acceso concurrente. El registro de
logs y el guardado de datos no forman una transacción única.
Todavía no incluye cambio de estado ni eliminación.

## Organización

- `main.py`: interacción y coordinación del menú.
- `tickets.py`: creación y búsqueda de tickets separadas de la consola.
- `archivo.py`: lectura, validación, migración y guardado conjunto de tickets e IDs.