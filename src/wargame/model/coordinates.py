"""Valors de coordenades del tauler hexagonal."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class HexCoordinate:
    q: int
    r: int

