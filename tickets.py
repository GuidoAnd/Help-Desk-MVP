"""Crea y busca tickets sin depender de la interfaz de consola."""

from datetime import datetime

PRIORIDADES = ("alta", "media", "baja")


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
