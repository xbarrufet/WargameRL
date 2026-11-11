"""Valors de coordenades del tauler hexagonal."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True, order=True)
class HexCoordinate:
    q: int
    r: int

    def neighbors(self) -> tuple["HexCoordinate", ...]:
        return tuple(HexCoordinate(self.q + dq, self.r + dr) for dq, dr in AXIAL_DIRECTIONS)

    def distance_to(self, other: "HexCoordinate") -> int:
        dq = self.q - other.q
        dr = self.r - other.r
        return max(abs(dq), abs(dr), abs(dq + dr))


AXIAL_DIRECTIONS: tuple[tuple[int, int], ...] = (
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
)


def hex_distance(first: HexCoordinate, second: HexCoordinate) -> int:
    """Retorna la distància entre dues coordenades axials."""
    return first.distance_to(second)


@dataclass(frozen=True)
class FlatTopProjection:
    """Conversió entre coordenades axials i centres de píxels flat-top."""

    size: float
    origin_x: float = 0.0
    origin_y: float = 0.0

    def __post_init__(self) -> None:
        if self.size <= 0:
            raise ValueError("size ha de ser positiu")

    def to_screen(self, coordinate: HexCoordinate) -> tuple[float, float]:
        return (
            self.origin_x + self.size * 1.5 * coordinate.q,
            self.origin_y + self.size * sqrt(3) * (coordinate.r + coordinate.q / 2),
        )

    def from_screen(
        self,
        point: tuple[float, float],
        width: int,
        height: int,
    ) -> HexCoordinate | None:
        x, y = point
        px = (x - self.origin_x) / self.size
        py = (y - self.origin_y) / self.size
        q_float = 2 / 3 * px
        r_float = -1 / 3 * px + sqrt(3) / 3 * py
        candidate = _round_axial(q_float, r_float)
        if not (0 <= candidate.q < width and 0 <= candidate.r < height):
            return None

        center_x, center_y = self.to_screen(candidate)
        local_x = abs(x - center_x)
        local_y = abs(y - center_y)
        if local_x > self.size or local_y > sqrt(3) * (self.size - local_x) / 2:
            return None
        return candidate


def _round_axial(q_float: float, r_float: float) -> HexCoordinate:
    x = q_float
    z = r_float
    y = -x - z
    rounded_x = round(x)
    rounded_y = round(y)
    rounded_z = round(z)
    x_difference = abs(rounded_x - x)
    y_difference = abs(rounded_y - y)
    z_difference = abs(rounded_z - z)
    if x_difference > y_difference and x_difference > z_difference:
        rounded_x = -rounded_y - rounded_z
    elif y_difference > z_difference:
        rounded_y = -rounded_x - rounded_z
    else:
        rounded_z = -rounded_x - rounded_y
    return HexCoordinate(rounded_x, rounded_z)


def in_bounds(coordinate: HexCoordinate, width: int, height: int) -> bool:
    return 0 <= coordinate.q < width and 0 <= coordinate.r < height


def bounded_neighbors(coordinate: HexCoordinate, width: int, height: int) -> tuple[HexCoordinate, ...]:
    return tuple(neighbor for neighbor in coordinate.neighbors() if in_bounds(neighbor, width, height))

