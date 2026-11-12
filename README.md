# Mesa de ayuda

Aplicación de consola para crear tickets con título, descripción y prioridad.
El ID, el estado `abierto` y la fecha se asignan automáticamente.

## Instalación y ejecución

Requisito: Python 3.13.5. Este incremento usa solo la biblioteca estándar;
no requiere instalar paquetes externos.

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python main.py
```

En Windows, crear el entorno con `py -3.13 -m venv .venv` y activarlo con
`.venv\Scripts\activate` desde CMD; luego ejecutar `python main.py`.

## Uso y datos

- Opción 1: ingresar título, descripción y prioridad (`alta`, `media` o `baja`).
- Opción 2: guardar y salir.

Los archivos se crean junto a `main.py`: `tickets.json` contiene la lista de
tickets, `ultimo_id.json` conserva el último ID reservado y `helpdesk.log`
registra las creaciones. Cada creación se guarda inmediatamente.

Los IDs no se reutilizan: una reserva interrumpida puede dejar un salto.
Conservar y respaldar juntos los dos archivos JSON, incluso después de eliminar
tickets. No editar ni borrar el contador: conserva el historial de IDs.
Si los archivos están dañados, el programa informa el error y se detiene.

## Limitaciones y mejoras pendientes

Uso local con una sola instancia; no admite acceso concurrente. El registro de
logs y el guardado de datos no forman una transacción única.
Todavía no incluye listado, búsqueda, cambio de estado ni eliminación.
Estas operaciones completan el alcance pendiente de la mesa de ayuda.

## Organización

- `main.py`: interacción y coordinación del menú.
- `tickets.py`: validación y construcción de tickets separadas de la consola.
- `archivo.py`: lectura, escritura y reserva persistente de IDs.
