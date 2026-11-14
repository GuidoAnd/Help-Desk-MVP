"""Gestiona tickets sin depender de la interfaz de consola."""

from datetime import datetime

PRIORIDADES = ("alta", "media", "baja")
TRANSICIONES = {"abierto": "en_curso", "en_curso": "resuelto"}


def crear_ticket(identificador: int, titulo: str, descripcion: str,
                 prioridad: str) -> dict:
    """Valida los datos y devuelve un ticket con sus seis campos."""
    titulo = titulo.strip()
    prioridad = prioridad.strip().lower()
    if not titulo:
        raise ValueError("El título no puede estar vacío.")
    if prioridad not in PRIORIDADES:
        raise ValueError("La prioridad debe ser alta, media o baja.")
    return {
        "id": identificador,
        "titulo": titulo,
        "descripcion": descripcion.strip(),
        "prioridad": prioridad,
        "estado": "abierto",
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }


def buscar_ticket(tickets: list[dict], identificador: int) -> dict | None:
    """Devuelve el ticket con el ID indicado o None si no existe."""
    for ticket in tickets:
        if ticket["id"] == identificador:
            return ticket
    return None


def cambiar_estado(tickets: list[dict], identificador: int,
                   nuevo_estado: str) -> list[dict]:
    """Devuelve una colección nueva con el avance permitido del ticket."""
    ticket = buscar_ticket(tickets, identificador)
    if ticket is None:
        raise ValueError(f"No existe un ticket con ID {identificador}.")
    if TRANSICIONES.get(ticket["estado"]) != nuevo_estado:
        raise ValueError("Solo se permite avanzar de abierto a en_curso y a resuelto.")
    return [
        {**actual, "estado": nuevo_estado}
        if actual["id"] == identificador else actual
        for actual in tickets
    ]


def eliminar_ticket(tickets: list[dict], identificador: int) -> list[dict]:
    """Devuelve la colección sin el ticket indicado, sin alterar el contador."""
    if buscar_ticket(tickets, identificador) is None:
        raise ValueError(f"No existe un ticket con ID {identificador}.")
    return [ticket for ticket in tickets if ticket["id"] != identificador]
