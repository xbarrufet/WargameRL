"""Accions i resolució del moviment dels robots."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from wargame.model.coordinates import HexCoordinate, in_bounds
from wargame.model.enums import Direction, Phase
from wargame.model.state import GameState, ModelError
from .turn import validate_robot_action


class MovementKind(str, Enum):
    NORMAL = "normal"
    JUMP = "jump"


@dataclass(frozen=True)
class Advance:
    """Avança una casella en la direcció actual."""


@dataclass(frozen=True)
class Pivot:
    """Gira 60 graus en sentit horari o antihorari."""

    steps: int = 1

    def __post_init__(self) -> None:
        if self.steps not in (-1, 1):
            raise ValueError("steps ha de ser 1 o -1")


@dataclass(frozen=True)
class NormalMovement:
    steps: tuple[Advance | Pivot, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.steps, tuple):
            raise TypeError("steps ha de ser una tupla")


@dataclass(frozen=True)
class Jump:
    destination: HexCoordinate
    orientation: Direction

    def __post_init__(self) -> None:
        if not isinstance(self.destination, HexCoordinate):
            raise TypeError("destination ha de ser una HexCoordinate")
        if not isinstance(self.orientation, Direction):
            raise TypeError("orientation ha de ser una Direction")


@dataclass(frozen=True)
class MovementResult:
    robot_id: str
    kind: MovementKind
    origin: HexCoordinate
    destination: HexCoordinate
    orientation: Direction
    cost: int


_DIRECTION_ORDER = (
    Direction.N,
    Direction.NE,
    Direction.SE,
    Direction.S,
    Direction.SW,
    Direction.NW,
)
_DIRECTION_VECTORS = {
    Direction.N: (0, -1),
    Direction.NE: (1, -1),
    Direction.SE: (1, 0),
    Direction.S: (0, 1),
    Direction.SW: (-1, 1),
    Direction.NW: (-1, 0),
}


def execute_movement(
    state: GameState,
    robot_id: str,
    action: NormalMovement | Jump,
) -> MovementResult:
    """Valida i aplica una acció completa de moviment de forma atòmica."""
    robot = _find_robot(state, robot_id)
    validate_robot_action(state, robot_id, Phase.MOVEMENT)
    if isinstance(action, NormalMovement):
        result = _plan_normal(state, robot, action)
    elif isinstance(action, Jump):
        result = _plan_jump(state, robot, action)
    else:
        raise ModelError("movement: acció desconeguda")

    robot.position = result.destination
    robot.orientation = result.orientation
    state.movement_kinds[robot.id] = result.kind.value
    return result


def accessible_destinations(
    state: GameState,
    robot_id: str,
    kind: MovementKind,
) -> frozenset[HexCoordinate]:
    """Retorna les destinacions legals per al tipus de moviment indicat."""
    robot = _find_robot(state, robot_id)
    occupied = _occupied_positions(state, robot_id)
    if kind is MovementKind.JUMP:
        return frozenset(
            position
            for q in range(state.board.width)
            for r in range(state.board.height)
            for position in (HexCoordinate(q, r),)
            if position not in occupied
            and robot.position.distance_to(position) <= robot.jump
            and position != robot.position
        )

    destinations: set[HexCoordinate] = set()
    frontier = {(robot.position, robot.orientation, 0)}
    while frontier:
        position, orientation, cost = frontier.pop()
        destinations.add(position)
        if cost == robot.movement:
            continue
        for next_action in (Pivot(1), Pivot(-1), Advance()):
            try:
                next_position, next_orientation = _step_normal(
                    state, robot_id, position, orientation, next_action, occupied
                )
            except ModelError:
                continue
            frontier.add((next_position, next_orientation, cost + 1))
    return frozenset(destinations)


def _plan_normal(state: GameState, robot, action: NormalMovement) -> MovementResult:
    occupied = _occupied_positions(state, robot.id)
    position, orientation = robot.position, robot.orientation
    if len(action.steps) > robot.movement:
        raise ModelError("movement: se supera el pressupost normal")
    for step in action.steps:
        position, orientation = _step_normal(
            state, robot.id, position, orientation, step, occupied
        )
    return MovementResult(
        robot.id, MovementKind.NORMAL, robot.position, position, orientation, len(action.steps)
    )


def _plan_jump(state: GameState, robot, action: Jump) -> MovementResult:
    if not state.board.contains(action.destination):
        raise ModelError("jump: destí fora del tauler")
    if action.destination in _occupied_positions(state, robot.id):
        raise ModelError("jump: el destí està ocupat")
    if robot.position.distance_to(action.destination) > robot.jump:
        raise ModelError("jump: se supera la distància màxima")
    return MovementResult(
        robot.id,
        MovementKind.JUMP,
        robot.position,
        action.destination,
        action.orientation,
        robot.position.distance_to(action.destination),
    )


def _step_normal(state, robot_id, position, orientation, action, occupied):
    if isinstance(action, Pivot):
        index = _DIRECTION_ORDER.index(orientation)
        return position, _DIRECTION_ORDER[(index + action.steps) % len(_DIRECTION_ORDER)]
    if not isinstance(action, Advance):
        raise ModelError("movement: pas desconegut")
    dq, dr = _DIRECTION_VECTORS[orientation]
    destination = HexCoordinate(position.q + dq, position.r + dr)
    if not state.board.contains(destination):
        raise ModelError("movement: destí fora del tauler")
    if destination in occupied:
        raise ModelError("movement: el destí està ocupat")
    if state.board.elevation_at(destination) > state.board.elevation_at(position):
        raise ModelError("movement: no es pot pujar a una elevació superior")
    return destination, orientation


def _find_robot(state: GameState, robot_id: str):
    for team in state.teams.values():
        if robot_id in team.robots:
            robot = team.robots[robot_id]
            if robot.destroyed:
                raise ModelError(f"movement: robot destruït: {robot_id}")
            return robot
    raise ModelError(f"movement: robot desconegut: {robot_id}")


def _occupied_positions(state: GameState, moving_robot_id: str):
    return {
        robot.position
        for team in state.teams.values()
        for robot in team.robots.values()
        if not robot.destroyed and robot.id != moving_robot_id
    }
