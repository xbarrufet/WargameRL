"""Regles pures auxiliars per a la resolució de combat."""

from wargame.model import ModelError


def movement_modifier(kind: str | None) -> int:
    if kind == "jump":
        return -2
    if kind == "normal":
        return 0
    if kind is None:
        return 1
    raise ModelError(f"combat: tipus de moviment desconegut: {kind}")
