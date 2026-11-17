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
        raise ValueError(
            "Solo se permite avanzar de abierto a en_curso y a resuelto."
        )
    return [
        {**actual, "estado": nuevo_estado}
        if actual["id"] == identificador else actual
        for actual in tickets
    ]


def eliminar_ticket(tickets: list[dict], identificador: int) -> list[dict]:
    """Devuelve la colección sin el ticket, conservando el contador externo."""
    if buscar_ticket(tickets, identificador) is None:
        raise ValueError(f"No existe un ticket con ID {identificador}.")
    return [ticket for ticket in tickets if ticket["id"] != identificador]


def filtrar_tickets(tickets: list[dict], campo: str, valor: str) -> list[dict]:
    """Selecciona por prioridad o estado sin alterar la colección original."""
    opciones = {
        "prioridad": PRIORIDADES,
        "estado": ("abierto", "en_curso", "resuelto"),
    }
    if campo not in opciones or valor not in opciones[campo]:
        raise ValueError("Filtro de prioridad o estado inválido.")
    return [ticket for ticket in tickets if ticket[campo] == valor]


def ordenar_tickets(tickets: list[dict]) -> list[dict]:
    """Ordena alta, media y baja, conservando el orden de cada grupo."""
    orden = {prioridad: indice for indice, prioridad in enumerate(PRIORIDADES)}
    return sorted(tickets, key=lambda ticket: orden[ticket["prioridad"]])


def editar_ticket(
    tickets: list[dict], identificador: int, campo: str, valor: str,
) -> list[dict]:
    """Devuelve la colección con un campo editado sin alterar el original."""
    if campo not in ("titulo", "descripcion", "prioridad"):
        raise ValueError(
            "Solo se permite editar título, descripción o prioridad."
        )
    ticket = buscar_ticket(tickets, identificador)
    if ticket is None:
        raise ValueError(f"No existe un ticket con ID {identificador}.")
    valor = valor.strip()
    if campo == "titulo" and not valor:
        raise ValueError("El título no puede estar vacío.")
    if campo == "prioridad":
        valor = valor.lower()
        if valor not in PRIORIDADES:
            raise ValueError("La prioridad debe ser alta, media o baja.")
    return [
        {**actual, campo: valor} if actual["id"] == identificador else actual
        for actual in tickets
    ]
