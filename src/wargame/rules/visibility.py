"""Regles de línia de visió i classificació d'arcs."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import atan2, degrees

from wargame.model.coordinates import HexCoordinate
from wargame.model.enums import Direction
from wargame.model.state import GameState


class ArcRelation(str, Enum):
    FRONT = "front"
    SIDE = "side"
    REAR = "rear"


class VisibilityReason(str, Enum):
    UNKNOWN_ATTACKER = "unknown_attacker"
    UNKNOWN_TARGET = "unknown_target"
    DESTROYED = "destroyed"
    SAME_TEAM = "same_team"
    OUT_OF_ARC = "out_of_arc"
    OUT_OF_RANGE = "out_of_range"
    ELEVATION_BLOCKED = "elevation_blocked"


@dataclass(frozen=True)
class VisibilityResult:
    attacker_id: str
    target_id: str
    relation: ArcRelation | None
    visible: bool
    reason: VisibilityReason | None = None


_ORIENTATION_ANGLES = {
    Direction.N: -90.0,
    Direction.NE: -30.0,
    Direction.SE: 30.0,
    Direction.S: 90.0,
    Direction.SW: 150.0,
    Direction.NW: 210.0,
}


def classify_arc(origin: HexCoordinate, orientation: Direction, target: HexCoordinate) -> ArcRelation:
    """Classifica el blanc en l'arc frontal de 120°, lateral o posterior."""
    dq = target.q - origin.q
    dr = target.r - origin.r
    if dq == 0 and dr == 0:
        return ArcRelation.FRONT
    screen_x = 1.5 * dq
    screen_y = 3**0.5 * (dr + dq / 2)
    target_angle = degrees(atan2(screen_y, screen_x))
    difference = _angle_difference(target_angle, _ORIENTATION_ANGLES[orientation])
    if difference <= 60:
        return ArcRelation.FRONT
    if abs(difference - 180) <= 60:
        return ArcRelation.REAR
    return ArcRelation.SIDE


def assess_target(state: GameState, attacker_id: str, target_id: str) -> VisibilityResult:
    """Avalua un blanc sense modificar l'estat."""
    attacker = _find_robot(state, attacker_id)
    if attacker is None:
        return VisibilityResult(attacker_id, target_id, None, False, VisibilityReason.UNKNOWN_ATTACKER)
    target = _find_robot(state, target_id)
    if target is None:
        return VisibilityResult(attacker_id, target_id, None, False, VisibilityReason.UNKNOWN_TARGET)
    if attacker.destroyed or target.destroyed:
        return VisibilityResult(attacker_id, target_id, None, False, VisibilityReason.DESTROYED)
    if attacker.team_id == target.team_id:
        return VisibilityResult(attacker_id, target_id, None, False, VisibilityReason.SAME_TEAM)

    relation = classify_arc(attacker.position, attacker.orientation, target.position)
    if relation is not ArcRelation.FRONT:
        return VisibilityResult(attacker_id, target_id, relation, False, VisibilityReason.OUT_OF_ARC)
    distance = attacker.position.distance_to(target.position)
    if distance > attacker.range:
        return VisibilityResult(attacker_id, target_id, relation, False, VisibilityReason.OUT_OF_RANGE)
    if _elevation_blocks(state, attacker.position, target.position):
        return VisibilityResult(
            attacker_id, target_id, relation, False, VisibilityReason.ELEVATION_BLOCKED
        )
    return VisibilityResult(attacker_id, target_id, relation, True)


def valid_targets(state: GameState, attacker_id: str) -> tuple[VisibilityResult, ...]:
    """Retorna tots els blancs enemics vàlids en ordre determinista."""
    targets = [
        robot.id
        for team in state.teams.values()
        for robot in team.robots.values()
        if robot.id != attacker_id
    ]
    return tuple(
        result
        for target_id in sorted(targets)
        for result in (assess_target(state, attacker_id, target_id),)
        if result.visible
    )


def _find_robot(state: GameState, robot_id: str):
    for team in state.teams.values():
        if robot_id in team.robots:
            return team.robots[robot_id]
    return None


def _angle_difference(first: float, second: float) -> float:
    return abs((first - second + 180) % 360 - 180)


def _elevation_blocks(state: GameState, origin: HexCoordinate, target: HexCoordinate) -> bool:
    if state.board.elevation_at(origin) == 1 or state.board.elevation_at(target) == 1:
        return False
    for position in _intermediate_line(origin, target):
        if state.board.elevation_at(position) == 1:
            return True
    return False


def _intermediate_line(origin: HexCoordinate, target: HexCoordinate) -> tuple[HexCoordinate, ...]:
    distance = origin.distance_to(target)
    if distance <= 1:
        return ()
    origin_cube = (origin.q, -origin.q - origin.r, origin.r)
    target_cube = (target.q, -target.q - target.r, target.r)
    positions = []
    for step in range(1, distance):
        factor = step / distance
        cube = tuple(
            origin_cube[index] + (target_cube[index] - origin_cube[index]) * factor
            for index in range(3)
        )
        positions.append(_round_cube(cube))
    return tuple(positions)


def _round_cube(cube: tuple[float, float, float]) -> HexCoordinate:
    x, y, z = cube
    rx, ry, rz = round(x), round(y), round(z)
    differences = (abs(rx - x), abs(ry - y), abs(rz - z))
    largest = differences.index(max(differences))
    if largest == 0:
        rx = -ry - rz
    elif largest == 1:
        ry = -rx - rz
    else:
        rz = -rx - ry
    return HexCoordinate(rx, rz)
