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

En PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Uso y datos

- Opción 1: ingresar título, descripción y prioridad (`alta`, `media` o `baja`).
- Opción 2: listar todos los tickets en una tabla con sus seis campos.
- Opción 3: buscar un ticket por su ID y mostrar todos sus datos.
- Opción 4: guardar y salir.

Si no hay tickets se informa en pantalla. La búsqueda requiere un ID entero
positivo; si el ID no existe, se informa y se vuelve al menú.

Los archivos se crean junto a `main.py`: `tickets.json` contiene la lista de
tickets, `ultimo_id.json` conserva el último ID reservado y `helpdesk.log`
registra las creaciones. Cada creación se guarda inmediatamente.

Los IDs no se reutilizan: una reserva interrumpida puede dejar un salto.
Conservar y respaldar juntos los dos archivos JSON, incluso después de eliminar
tickets. No editar ni borrar el contador: conserva el historial de IDs.
Si los archivos están dañados, el programa informa el error y se detiene.

## Limitaciones y mejoras

Uso local con una sola instancia; no admite acceso concurrente. El registro de
logs y el guardado de datos no forman una transacción única.
Todavía no incluye cambio de estado ni eliminación.

## Organización

- `main.py`: interacción y coordinación del menú.
- `tickets.py`: creación y búsqueda de tickets separadas de la consola.
- `archivo.py`: lectura, escritura y reserva persistente de IDs.
