"""Entitats del model de partida."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .coordinates import HexCoordinate
from .enums import Direction


@dataclass
class Robot:
    id: str
    team_id: str
    movement: int
    range: int
    damage: int
    position: HexCoordinate
    orientation: Direction
    impacts: int = 0
    destroyed: bool = False


@dataclass
class Team:
    id: str
    sprite: Path
    robots: dict[str, Robot] = field(default_factory=dict)


@dataclass(frozen=True)
class Objective:
    id: str
    position: HexCoordinate
    zone: str


@dataclass(frozen=True)
class Board:
    width: int
    height: int
    elevations: tuple[tuple[int, ...], ...]

