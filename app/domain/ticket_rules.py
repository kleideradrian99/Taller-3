"""Reglas de negocio y transiciones de tickets (Actividad 5)."""

from __future__ import annotations

from app.domain.actividad2 import TRANSICIONES
from app import models

ASSIGNABLE_ROLES = frozenset({"auxiliar", "tecnico_especializado"})


def scope_para_transicion(estado_actual: str, estado_nuevo: str) -> str | None:
    for a, b, scope in TRANSICIONES:
        if a == estado_actual and b == estado_nuevo:
            return scope
    return None


def puede_ver_ticket(usuario: models.Usuario, scopes: frozenset[str], ticket: models.Ticket) -> bool:
    if "tickets:ver_todos" in scopes:
        return True
    uid = usuario.id_usuario
    return (
        ticket.id_solicitante == uid
        or ticket.id_responsable == uid
        or ticket.id_asignado == uid
    )


def es_admin(usuario: models.Usuario) -> bool:
    return usuario.rol == "admin"


def puede_gestionar_como_responsable_del_ticket(
    usuario: models.Usuario, ticket: models.Ticket
) -> bool:
    if es_admin(usuario):
        return True
    return usuario.rol == "responsable_tecnico" and ticket.id_responsable == usuario.id_usuario


def puede_atender_ticket(usuario: models.Usuario, ticket: models.Ticket) -> bool:
    if es_admin(usuario):
        return True
    return ticket.id_asignado is not None and ticket.id_asignado == usuario.id_usuario


def puede_finalizar_ticket(usuario: models.Usuario, ticket: models.Ticket) -> bool:
    if es_admin(usuario):
        return True
    return (
        usuario.rol == "responsable_tecnico"
        and ticket.id_responsable is not None
        and ticket.id_responsable == usuario.id_usuario
    )
