"""Gestiona la persistencia local y el historial de IDs."""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATOS = BASE / "tickets.json"
CONTADOR = BASE / "ultimo_id.json"


def guardar_json(ruta: Path, datos: object) -> None:
    """Reemplaza el destino después de escribir el JSON completo."""
    temporal = ruta.with_suffix(ruta.suffix + ".tmp")
    with temporal.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=2)
        archivo.write("\n")
    temporal.replace(ruta)


def cargar_tickets() -> list[dict]:
    """Carga y valida la lista sin sobrescribir datos inválidos."""
    if not DATOS.exists():
        guardar_json(DATOS, [])
    with DATOS.open(encoding="utf-8") as archivo:
        tickets = json.load(archivo)
    if not isinstance(tickets, list):
        raise ValueError("tickets.json debe contener una lista.")
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
        if any(not isinstance(ticket[campo], str) for campo in campos - {"id"}):
            raise ValueError("Los campos de texto deben ser cadenas.")
        if not ticket["titulo"].strip() or not ticket["fecha_creacion"].strip():
            raise ValueError("El título y la fecha no pueden estar vacíos.")
        if ticket["prioridad"] not in ("alta", "media", "baja"):
            raise ValueError("Prioridad inválida en tickets.json.")
        if ticket["estado"] not in ("abierto", "en_curso", "resuelto"):
            raise ValueError("Estado inválido en tickets.json.")
    return tickets


def cargar_ultimo_id(tickets: list[dict]) -> int:
    """Carga el contador que debe conservarse incluso al eliminar tickets."""
    if not CONTADOR.exists():
        if tickets:
            raise ValueError("Falta ultimo_id.json; restaurá el contador histórico.")
        guardar_json(CONTADOR, 0)
    with CONTADOR.open(encoding="utf-8") as archivo:
        ultimo_id = json.load(archivo)
    if type(ultimo_id) is not int or ultimo_id < 0:
        raise ValueError("El contador de IDs es inválido.")
    if ultimo_id < max((ticket["id"] for ticket in tickets), default=0):
        raise ValueError("El contador es menor que un ID existente.")
    return ultimo_id


def reservar_id(ultimo_id: int) -> int:
    """Persiste el siguiente ID antes de usarlo para no reutilizarlo."""
    siguiente = ultimo_id + 1
    guardar_json(CONTADOR, siguiente)
    return siguiente


def guardar_tickets(tickets: list[dict]) -> None:
    """Guarda los tickets conservando su estructura de lista."""
    guardar_json(DATOS, tickets)
