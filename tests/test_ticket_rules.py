"""Unit tests for ticket authorization helpers (no database connection required)."""

from __future__ import annotations

import unittest
from types import SimpleNamespace

from app.domain import ticket_rules


def user(uid: int, rol: str) -> SimpleNamespace:
    return SimpleNamespace(id_usuario=uid, rol=rol)


def ticket(
    *,
    solicitante: int,
    responsable: int | None = None,
    asignado: int | None = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        id_solicitante=solicitante,
        id_responsable=responsable,
        id_asignado=asignado,
    )


class ScopeParaTransicionTests(unittest.TestCase):
    def test_flujo_principal(self) -> None:
        self.assertEqual(ticket_rules.scope_para_transicion("solicitado", "recibido"), "tickets:recibir")
        self.assertEqual(ticket_rules.scope_para_transicion("recibido", "asignado"), "tickets:asignar")
        self.assertEqual(ticket_rules.scope_para_transicion("asignado", "en_proceso"), "tickets:atender")

    def test_transicion_invalida(self) -> None:
        self.assertIsNone(ticket_rules.scope_para_transicion("solicitado", "terminado"))
        self.assertIsNone(ticket_rules.scope_para_transicion("en_revision", "solicitado"))


class VisibilidadTests(unittest.TestCase):
    def test_admin_ve_con_scope_ver_todos(self) -> None:
        t = ticket(solicitante=99)
        u = user(1, "admin")
        self.assertTrue(ticket_rules.puede_ver_ticket(u, frozenset({"tickets:ver_todos"}), t))

    def test_solicitante_ve_propio(self) -> None:
        t = ticket(solicitante=5)
        self.assertTrue(ticket_rules.puede_ver_ticket(user(5, "solicitante"), frozenset({"tickets:ver_propios"}), t))

    def test_solicitante_no_ve_ajeno(self) -> None:
        t = ticket(solicitante=5)
        self.assertFalse(ticket_rules.puede_ver_ticket(user(6, "solicitante"), frozenset({"tickets:ver_propios"}), t))


class AtenderFinalizarTests(unittest.TestCase):
    def test_auxiliar_asignado_puede_atender(self) -> None:
        t = ticket(solicitante=1, responsable=2, asignado=10)
        self.assertTrue(ticket_rules.puede_atender_ticket(user(10, "auxiliar"), t))

    def test_auxiliar_no_asignado_no_atiende(self) -> None:
        t = ticket(solicitante=1, responsable=2, asignado=10)
        self.assertFalse(ticket_rules.puede_atender_ticket(user(11, "auxiliar"), t))

    def test_auxiliar_no_puede_finalizar(self) -> None:
        t = ticket(solicitante=1, responsable=2, asignado=10)
        self.assertFalse(ticket_rules.puede_finalizar_ticket(user(10, "auxiliar"), t))

    def test_responsable_registrado_finaliza(self) -> None:
        t = ticket(solicitante=1, responsable=7, asignado=10)
        self.assertTrue(ticket_rules.puede_finalizar_ticket(user(7, "responsable_tecnico"), t))


class ResponsableTicketTests(unittest.TestCase):
    def test_responsable_del_ticket_asigna(self) -> None:
        t = ticket(solicitante=1, responsable=3)
        self.assertTrue(ticket_rules.puede_gestionar_como_responsable_del_ticket(user(3, "responsable_tecnico"), t))

    def test_otro_responsable_no_asigna_este_ticket(self) -> None:
        t = ticket(solicitante=1, responsable=3)
        self.assertFalse(ticket_rules.puede_gestionar_como_responsable_del_ticket(user(4, "responsable_tecnico"), t))


if __name__ == "__main__":
    unittest.main()
