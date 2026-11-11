"""Entitats del model de partida."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .coordinates import HexCoordinate, bounded_neighbors, in_bounds
from .enums import Direction


@dataclass
class Robot:
    id: str
    team_id: str
    movement: int
    jump: int
    range: int
    damage: int
    hit_target: int
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

    def contains(self, position: HexCoordinate) -> bool:
        return in_bounds(position, self.width, self.height)

    def neighbors(self, position: HexCoordinate) -> tuple[HexCoordinate, ...]:
        if not self.contains(position):
            raise ValueError(f"coordenada fora del tauler: {position}")
        return bounded_neighbors(position, self.width, self.height)

    def elevation_at(self, position: HexCoordinate) -> int:
        if not self.contains(position):
            raise ValueError(f"coordenada fora del tauler: {position}")
        return self.elevations[position.r][position.q]

