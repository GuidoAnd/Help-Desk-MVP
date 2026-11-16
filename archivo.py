"""Gestiona la persistencia local y el historial de IDs."""

import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATOS = BASE / "tickets.json"
CONTADOR = BASE / "ultimo_id.json"


def guardar_json(ruta: Path, datos: object) -> None:
    """Reemplaza el destino después de escribir el JSON completo."""
    temporal = ruta.with_suffix(ruta.suffix + ".tmp")
    try:
        with temporal.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
            archivo.write("\n")
        temporal.replace(ruta)
    except (OSError, UnicodeError) as error:
        raise OSError(
            f"No se pudo guardar {ruta.name}. "
            "Revisá permisos y espacio libre. "
            "El destino no se reemplazó; puede quedar un archivo temporal."
        ) from error


def leer_json(ruta: Path) -> object:
    """Distingue errores de acceso, codificación y sintaxis del documento."""
    try:
        with ruta.open(encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError as error:
        raise ValueError(
            f"JSON inválido en {ruta.name}, línea {error.lineno}, "
            f"columna {error.colno}. Restaurá una copia válida."
        ) from error
    except UnicodeError as error:
        raise ValueError(
            f"{ruta.name} debe estar codificado en UTF-8."
        ) from error
    except OSError as error:
        raise OSError(
            f"No se pudo leer {ruta.name}. Revisá su existencia y permisos."
        ) from error


def validar_tickets(tickets: list[dict]) -> None:
    """Rechaza tickets inválidos antes de utilizar o guardar sus datos."""
    if not isinstance(tickets, list):
        raise ValueError("El campo tickets debe contener una lista.")
    campos = {"id", "titulo", "descripcion", "prioridad", "estado",
              "fecha_creacion"}
    ids = set()
    for ticket in tickets:
        if not isinstance(ticket, dict) or set(ticket) != campos:
            raise ValueError("Hay un ticket con campos inválidos.")
        identificador = ticket["id"]
        if type(identificador) is not int or identificador < 1:
            raise ValueError("Los IDs deben ser enteros positivos.")
        if identificador in ids:
            raise ValueError("Hay IDs duplicados.")
        ids.add(identificador)
        if any(
            not isinstance(ticket[campo], str) for campo in campos - {"id"}
        ):
            raise ValueError("Los campos de texto deben ser cadenas.")
        if not all(ticket[campo].strip()
                   for campo in ("titulo", "fecha_creacion")):
            raise ValueError("El título y la fecha no pueden estar vacíos.")
        try:
            datetime.strptime(ticket["fecha_creacion"], "%Y-%m-%d %H:%M")
        except ValueError as error:
            raise ValueError(
                "La fecha debe ser válida y tener formato AAAA-MM-DD HH:MM."
            ) from error
        if ticket["prioridad"] not in ("alta", "media", "baja"):
            raise ValueError("Prioridad inválida en tickets.json.")
        if ticket["estado"] not in ("abierto", "en_curso", "resuelto"):
            raise ValueError("Estado inválido en tickets.json.")


def validar_datos(tickets: list[dict], ultimo_id: int) -> None:
    """Comprueba la colección y la continuidad del contador histórico."""
    validar_tickets(tickets)
    if type(ultimo_id) is not int or ultimo_id < 0:
        raise ValueError("El contador de IDs es inválido.")
    if ultimo_id < max((ticket["id"] for ticket in tickets), default=0):
        raise ValueError("El contador es menor que un ID existente.")


def cargar_datos() -> tuple[list[dict], int]:
    """Carga o migra el documento conservando el contador histórico."""
    if not DATOS.exists():
        if CONTADOR.exists():
            raise ValueError(
                "Falta tickets.json; restaurá los datos existentes."
            )
        guardar_tickets([], 0)
    datos = leer_json(DATOS)
    if isinstance(datos, list):
        if not CONTADOR.exists():
            raise ValueError(
                "Falta el contador histórico para migrar los datos."
            )
        ultimo_id = leer_json(CONTADOR)
        guardar_tickets(datos, ultimo_id)
        return datos, ultimo_id
    if not isinstance(datos, dict) or set(datos) != {"ultimo_id", "tickets"}:
        raise ValueError("tickets.json debe contener ultimo_id y tickets.")
    validar_datos(datos["tickets"], datos["ultimo_id"])
    return datos["tickets"], datos["ultimo_id"]


def guardar_tickets(tickets: list[dict], ultimo_id: int) -> None:
    """Guarda tickets y contador juntos mediante un único reemplazo."""
    validar_datos(tickets, ultimo_id)
    guardar_json(DATOS, {"ultimo_id": ultimo_id, "tickets": tickets})
