"""Punto de entrada del menú de la mesa de ayuda."""

import logging

from tabulate import tabulate

from archivo import BASE, cargar_datos, guardar_tickets
from tickets import PRIORIDADES, buscar_ticket, crear_ticket


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


def mostrar_tickets(tickets: list[dict]) -> None:
    """Presenta todos los tickets en una tabla sin alterar sus datos."""
    if not tickets:
        print("No hay tickets registrados.")
        return
    encabezados = {
        "id": "ID", "titulo": "Título", "descripcion": "Descripción",
        "prioridad": "Prioridad", "estado": "Estado",
        "fecha_creacion": "Fecha de creación",
    }
    filas = [[ticket[campo] for campo in encabezados] for ticket in tickets]
    print(tabulate(
        filas, headers=list(encabezados.values()), tablefmt="grid",
        disable_numparse=True, maxcolwidths=[None, 30, 40, None, None, None],
    ))


def consultar_ticket(tickets: list[dict]) -> None:
    """Valida el ID ingresado y muestra todos los datos del ticket encontrado."""
    if not tickets:
        print("No hay tickets registrados.")
        return
    try:
        identificador = int(input("ID del ticket: ").strip())
    except ValueError:
        print("El ID debe ser un número entero positivo.")
        return
    if identificador < 1:
        print("El ID debe ser un número entero positivo.")
        return
    ticket = buscar_ticket(tickets, identificador)
    if ticket is None:
        print(f"No existe un ticket con ID {identificador}.")
        return
    mostrar_tickets([ticket])


def main() -> int:
    """Carga los datos y repite el menú hasta salir o encontrar un error."""
    try:
        logging.basicConfig(
            filename=BASE / "helpdesk.log", encoding="utf-8",
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        tickets, ultimo_id = cargar_datos()
        while True:
            print("\nMesa de ayuda\n1. Crear ticket\n2. Listar tickets"
                  "\n3. Buscar ticket por ID\n4. Salir")
            opcion = input("Opción: ").strip()
            if opcion == "1":
                titulo = pedir_titulo()
                descripcion = input("Descripción: ")
                prioridad = pedir_prioridad()
                siguiente_id = ultimo_id + 1
                ticket = crear_ticket(siguiente_id, titulo, descripcion, prioridad)
                guardar_tickets(tickets + [ticket], siguiente_id)
                ultimo_id = siguiente_id
                tickets.append(ticket)
                logging.info("Ticket #%s creado (prioridad %s)",
                             ticket["id"], ticket["prioridad"])
                print(f"Ticket #{ticket['id']} creado y guardado.")
            elif opcion == "2":
                mostrar_tickets(tickets)
            elif opcion == "3":
                consultar_ticket(tickets)
            elif opcion == "4":
                guardar_tickets(tickets, ultimo_id)
                print("Datos guardados. Hasta luego.")
                return 0
            else:
                print("Opción inválida. Elegí 1, 2, 3 o 4.")
    except (EOFError, KeyboardInterrupt):
        print("\nSesión interrumpida. Las creaciones confirmadas están guardadas.")
        return 0
    except (OSError, ValueError) as error:
        print(f"No se puede continuar: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
