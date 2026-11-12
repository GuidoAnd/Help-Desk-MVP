"""Punto de entrada del menú de la mesa de ayuda."""

import logging

from archivo import (
    BASE, cargar_tickets, cargar_ultimo_id, guardar_tickets, reservar_id,
)
from tickets import PRIORIDADES, crear_ticket


def pedir_titulo() -> str:
    """Solicita un título hasta recibir texto no vacío."""
    while True:
        titulo = input("Título: ").strip()
        if titulo:
            return titulo
        print("El título no puede estar vacío.")


def pedir_prioridad() -> str:
    """Limita la entrada a las prioridades admitidas."""
    while True:
        prioridad = input("Prioridad (alta/media/baja): ").strip().lower()
        if prioridad in PRIORIDADES:
            return prioridad
        print("Elegí alta, media o baja.")


def main() -> int:
    """Carga los datos y repite el menú hasta salir o encontrar un error."""
    try:
        logging.basicConfig(
            filename=BASE / "helpdesk.log", encoding="utf-8",
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        tickets = cargar_tickets()
        ultimo_id = cargar_ultimo_id(tickets)
        while True:
            print("\nMesa de ayuda\n1. Crear ticket\n2. Salir")
            opcion = input("Opción: ").strip()
            if opcion == "1":
                titulo = pedir_titulo()
                descripcion = input("Descripción: ")
                prioridad = pedir_prioridad()
                ultimo_id = reservar_id(ultimo_id)
                ticket = crear_ticket(ultimo_id, titulo, descripcion, prioridad)
                guardar_tickets(tickets + [ticket])
                tickets.append(ticket)
                logging.info("Ticket #%s creado (prioridad %s)",
                             ticket["id"], ticket["prioridad"])
                print(f"Ticket #{ticket['id']} creado y guardado.")
            elif opcion == "2":
                guardar_tickets(tickets)
                print("Datos guardados. Hasta luego.")
                return 0
            else:
                print("Opción inválida. Elegí 1 o 2.")
    except (EOFError, KeyboardInterrupt):
        print("\nSesión interrumpida. Las creaciones confirmadas están guardadas.")
        return 0
    except (OSError, ValueError) as error:
        print(f"No se puede continuar: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
