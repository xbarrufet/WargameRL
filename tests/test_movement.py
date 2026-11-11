from pathlib import Path

import pytest

from wargame.engine import (
    Advance,
    Jump,
    MovementKind,
    NormalMovement,
    Pivot,
    accessible_destinations,
    execute_movement,
)
from wargame.io.yaml_reader import load_config
from wargame.model import Board, Direction, GameState, HexCoordinate, ModelError


ROOT = Path(__file__).parents[1]


def make_state() -> GameState:
    state = GameState.from_config(load_config(ROOT / "config/example.yaml"))
    robot = state.teams["team_a"].robots["team_a_robot_1"]
    robot.position = HexCoordinate(4, 4)
    robot.orientation = Direction.N
    return state


def test_normal_movement_combines_pivot_and_advance() -> None:
    state = make_state()

    result = execute_movement(
        state,
        "team_a_robot_1",
        NormalMovement((Pivot(1), Advance(), Advance())),
    )

    assert result.kind is MovementKind.NORMAL
    assert result.cost == 3
    assert result.destination == HexCoordinate(6, 2)
    assert result.orientation is Direction.NE


def test_normal_movement_can_go_around_robot_but_pivots_cost_movement() -> None:
    state = make_state()
    robot = state.teams["team_a"].robots["team_a_robot_1"]
    blocker = state.teams["team_a"].robots["team_a_robot_2"]
    robot.movement = 4
    blocker.position = HexCoordinate(4, 3)

    result = execute_movement(
        state,
        robot.id,
        NormalMovement((Pivot(1), Advance(), Pivot(-1), Advance())),
    )

    assert result.destination == HexCoordinate(5, 2)
    assert result.cost == 4

    with pytest.raises(ModelError, match="pressupost normal"):
        execute_movement(
            state,
            robot.id,
            NormalMovement((Pivot(1), Advance(), Pivot(-1), Advance(), Advance())),
        )


def test_normal_movement_is_atomic_when_a_later_step_fails() -> None:
    state = make_state()
    elevations = [list(row) for row in state.board.elevations]
    elevations[2][4] = 1
    state.board = Board(state.board.width, state.board.height, tuple(map(tuple, elevations)))
    robot = state.teams["team_a"].robots["team_a_robot_1"]
    original = (robot.position, robot.orientation)

    with pytest.raises(ModelError, match="elevació superior"):
        execute_movement(
            state,
            robot.id,
            NormalMovement((Advance(), Advance(), Advance())),
        )

    assert (robot.position, robot.orientation) == original


def test_jump_crosses_elevation_and_robots_but_not_occupied_destination() -> None:
    state = make_state()
    state.teams["team_a"].robots["team_a_robot_2"].position = HexCoordinate(5, 5)
    robot = state.teams["team_a"].robots["team_a_robot_1"]
    elevations = [list(row) for row in state.board.elevations]
    elevations[4][5] = 1
    state.board = Board(state.board.width, state.board.height, tuple(map(tuple, elevations)))

    result = execute_movement(
        state,
        robot.id,
        Jump(HexCoordinate(6, 6), Direction.S),
    )

    assert result.kind is MovementKind.JUMP
    assert robot.position == HexCoordinate(6, 6)
    assert robot.orientation is Direction.S

    with pytest.raises(ModelError, match="ocupat"):
        execute_movement(state, robot.id, Jump(HexCoordinate(5, 5), Direction.N))


def test_destroyed_robots_do_not_block_and_objectives_do_not_block() -> None:
    state = make_state()
    blocker = state.teams["team_a"].robots["team_a_robot_2"]
    blocker.position = HexCoordinate(4, 3)
    blocker.destroyed = True

    destinations = accessible_destinations(
        state, "team_a_robot_1", MovementKind.NORMAL
    )

    assert HexCoordinate(4, 3) in destinations
    assert HexCoordinate(2, 2) in accessible_destinations(
        state, "team_a_robot_1", MovementKind.JUMP
    )


def test_accessible_destinations_respect_jump_limit() -> None:
    state = make_state()
    destinations = accessible_destinations(
        state, "team_a_robot_1", MovementKind.JUMP
    )

    assert HexCoordinate(8, 4) in destinations
    assert HexCoordinate(9, 4) not in destinations
