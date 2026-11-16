"""Interfaz interactiva y coordinación de la mesa de ayuda."""

import logging
import sys

import questionary
from colorama import Fore, Style, just_fix_windows_console
from tabulate import tabulate

from archivo import BASE, cargar_datos, guardar_tickets
from tickets import (
    PRIORIDADES, TRANSICIONES, buscar_ticket, cambiar_estado, crear_ticket,
    eliminar_ticket, filtrar_tickets, ordenar_tickets,
)

COLORES_ESTADO = {
    "abierto": Fore.YELLOW,
    "en_curso": Fore.CYAN,
    "resuelto": Fore.GREEN,
}


class RegistroArchivo(logging.FileHandler):
    """Propaga fallos de escritura para avisar sin revertir datos guardados."""

    def handleError(self, record: logging.LogRecord) -> None:
        """Propaga el fallo de emisión para que la interfaz lo informe."""
        causa = sys.exc_info()[1]
        raise OSError("No se pudo escribir helpdesk.log.") from causa


def configurar_logs() -> None:
    """Abre el registro antes de cargar o modificar los datos de la sesión."""
    try:
        manejador = RegistroArchivo(BASE / "helpdesk.log", encoding="utf-8")
    except OSError as error:
        raise OSError(
            "No se pudo abrir helpdesk.log. Revisá los permisos; "
            "la sesión no se inició."
        ) from error
    registro = logging.getLogger("helpdesk")
    for anterior in registro.handlers[:]:
        registro.removeHandler(anterior)
        anterior.close()
    manejador.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S",
    ))
    registro.addHandler(manejador)
    registro.setLevel(logging.INFO)
    registro.propagate = False


def registrar_accion(mensaje: str, *argumentos: object) -> None:
    """Advierte si falla el log tras guardar, sin repetir la operación."""
    try:
        logging.getLogger("helpdesk").info(mensaje, *argumentos)
    except (OSError, UnicodeError):
        informar(
            "Los datos están guardados, pero la acción no pudo registrarse "
            "en helpdesk.log. No repitas la operación; revisá el archivo "
            "y los permisos del registro.", Fore.YELLOW,
        )


def colorear(texto: str, color: str) -> str:
    """Añade color solo cuando la salida es una terminal."""
    if not sys.stdout.isatty():
        return texto
    return f"{color}{texto}{Style.RESET_ALL}"


def informar(texto: str, color: str = Fore.CYAN) -> None:
    """Muestra un mensaje cuyo significado también queda expresado en texto."""
    print(colorear(texto, color))


def mostrar_tickets(tickets: list[dict]) -> None:
    """Presenta los seis campos sin modificar los tickets originales."""
    if not tickets:
        informar("No hay tickets registrados.")
        return
    encabezados = {
        "id": "ID", "titulo": "Título", "descripcion": "Descripción",
        "prioridad": "Prioridad", "estado": "Estado",
        "fecha_creacion": "Fecha de creación",
    }
    filas = []
    for ticket in ordenar_tickets(tickets):
        fila = dict(ticket)
        fila["estado"] = colorear(ticket["estado"],
                                  COLORES_ESTADO[ticket["estado"]])
        filas.append([fila[campo] for campo in encabezados])
    print(tabulate(
        filas, headers=list(encabezados.values()), tablefmt="grid",
        disable_numparse=True, maxcolwidths=[None, 30, 40, None, None, None],
    ))


def consultar_filtrados(tickets: list[dict]) -> None:
    """Solicita un filtro y presenta coincidencias ordenadas por prioridad."""
    if not tickets:
        informar("No hay tickets registrados.")
        return
    campo = questionary.select(
        "Filtrar por:", choices=["prioridad", "estado", "Cancelar"],
    ).ask()
    if campo is None or campo == "Cancelar":
        informar("Filtro cancelado.")
        return
    opciones = (list(PRIORIDADES) if campo == "prioridad"
                else ["abierto", "en_curso", "resuelto"])
    valor = questionary.select(
        f"Elegí {campo}:", choices=opciones + ["Cancelar"],
    ).ask()
    if valor is None or valor == "Cancelar":
        informar("Filtro cancelado.")
        return
    resultado = filtrar_tickets(tickets, campo, valor)
    if not resultado:
        informar(f"No hay tickets con {campo} {valor}.")
        return
    informar(f"Tickets con {campo} {valor}:")
    mostrar_tickets(resultado)


def seleccionar_ticket(tickets: list[dict]) -> dict | None:
    """Solicita un ID y resuelve la búsqueda sin cambiar los datos."""
    if not tickets:
        informar("No hay tickets registrados.")
        return None
    entrada = questionary.text("ID del ticket:").ask()
    if entrada is None:
        informar("Operación cancelada.")
        return None
    try:
        identificador = int(entrada.strip())
        if identificador < 1:
            raise ValueError
    except ValueError:
        informar("El ID debe ser un número entero positivo.", Fore.YELLOW)
        return None
    ticket = buscar_ticket(tickets, identificador)
    if ticket is None:
        informar(f"No existe un ticket con ID {identificador}.", Fore.YELLOW)
    return ticket


def registrar_ticket(
    tickets: list[dict], ultimo_id: int,
) -> tuple[list[dict], int]:
    """Guarda la creación únicamente tras completar todas las preguntas."""
    titulo = questionary.text(
        "Título:", validate=lambda texto: bool(texto.strip())
        or "El título no puede estar vacío.",
    ).ask()
    if titulo is None:
        informar("Creación cancelada.")
        return tickets, ultimo_id
    descripcion = questionary.text("Descripción:").ask()
    if descripcion is None:
        informar("Creación cancelada.")
        return tickets, ultimo_id
    prioridad = questionary.select(
        "Prioridad:", choices=list(PRIORIDADES),
    ).ask()
    if prioridad is None:
        informar("Creación cancelada.")
        return tickets, ultimo_id
    siguiente_id = ultimo_id + 1
    ticket = crear_ticket(siguiente_id, titulo, descripcion, prioridad)
    nuevos = tickets + [ticket]
    guardar_tickets(nuevos, siguiente_id)
    registrar_accion(
        "Ticket #%s creado (prioridad %s)", siguiente_id, prioridad,
    )
    informar(f"Ticket #{siguiente_id} creado y guardado.", Fore.GREEN)
    return nuevos, siguiente_id


def actualizar_estado(tickets: list[dict], ultimo_id: int) -> list[dict]:
    """Ofrece el avance permitido y lo guarda antes de registrar la acción."""
    ticket = seleccionar_ticket(tickets)
    if ticket is None:
        return tickets
    siguiente = TRANSICIONES.get(ticket["estado"])
    if siguiente is None:
        informar("El ticket ya está resuelto; no hay otro estado permitido.")
        return tickets
    mostrar_tickets([ticket])
    estado = questionary.select(
        "Nuevo estado:", choices=[siguiente, "Cancelar"],
    ).ask()
    if estado is None or estado == "Cancelar":
        informar("Cambio de estado cancelado.")
        return tickets
    nuevos = cambiar_estado(tickets, ticket["id"], estado)
    guardar_tickets(nuevos, ultimo_id)
    registrar_accion("Ticket #%s cambió a %s", ticket["id"], estado)
    informar(f"Ticket #{ticket['id']} cambió a {estado}.", Fore.GREEN)
    return nuevos


def confirmar_eliminacion(tickets: list[dict], ultimo_id: int) -> list[dict]:
    """Confirma la eliminación y conserva el contador histórico."""
    ticket = seleccionar_ticket(tickets)
    if ticket is None:
        return tickets
    mostrar_tickets([ticket])
    confirmado = questionary.confirm(
        f"¿Eliminar el ticket #{ticket['id']}?", default=False,
    ).ask()
    if confirmado is not True:
        informar("Eliminación cancelada.")
        return tickets
    nuevos = eliminar_ticket(tickets, ticket["id"])
    guardar_tickets(nuevos, ultimo_id)
    registrar_accion("Ticket #%s eliminado", ticket["id"])
    informar(f"Ticket #{ticket['id']} eliminado.", Fore.GREEN)
    return nuevos


def main() -> int:
    """Carga los datos y coordina las operaciones elegidas en el menú."""
    just_fix_windows_console()
    try:
        configurar_logs()
        tickets, ultimo_id = cargar_datos()
        while True:
            opcion = questionary.select("Mesa de ayuda", choices=[
                "Crear ticket", "Listar tickets", "Filtrar tickets",
                "Buscar ticket por ID",
                "Cambiar estado", "Eliminar ticket", "Salir",
            ]).ask()
            if opcion is None:
                informar(
                    "Sesión cancelada. Las operaciones confirmadas "
                    "están guardadas."
                )
                return 0
            if opcion == "Salir":
                guardar_tickets(tickets, ultimo_id)
                informar("Datos guardados. Hasta luego.", Fore.GREEN)
                return 0
            if opcion == "Crear ticket":
                tickets, ultimo_id = registrar_ticket(tickets, ultimo_id)
            elif opcion == "Listar tickets":
                mostrar_tickets(tickets)
            elif opcion == "Filtrar tickets":
                consultar_filtrados(tickets)
            elif opcion == "Buscar ticket por ID":
                ticket = seleccionar_ticket(tickets)
                if ticket is not None:
                    mostrar_tickets([ticket])
            elif opcion == "Cambiar estado":
                tickets = actualizar_estado(tickets, ultimo_id)
            elif opcion == "Eliminar ticket":
                tickets = confirmar_eliminacion(tickets, ultimo_id)
    except (EOFError, KeyboardInterrupt):
        informar(
            "Sesión interrumpida. Las operaciones confirmadas están guardadas."
        )
        return 0
    except (OSError, ValueError) as error:
        informar(f"No se puede continuar: {error}", Fore.RED)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
