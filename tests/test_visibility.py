from pathlib import Path

import pytest

from wargame.io.yaml_reader import load_config
from wargame.model import Board, Direction, GameState, HexCoordinate
from wargame.rules import ArcRelation, VisibilityReason, assess_target, classify_arc, valid_targets


ROOT = Path(__file__).parents[1]


def make_state() -> GameState:
    state = GameState.from_config(load_config(ROOT / "config/example.yaml"))
    attacker = state.teams["team_a"].robots["team_a_robot_1"]
    attacker.position = HexCoordinate(8, 7)
    return state


@pytest.mark.parametrize(
    ("orientation", "front", "rear"),
    [
        (Direction.N, (0, -1), (0, 1)),
        (Direction.NE, (1, -1), (-1, 1)),
        (Direction.SE, (1, 0), (-1, 0)),
        (Direction.S, (0, 1), (0, -1)),
        (Direction.SW, (-1, 1), (1, -1)),
        (Direction.NW, (-1, 0), (1, 0)),
    ],
)
def test_flat_top_arc_classifies_all_orientations(orientation, front, rear) -> None:
    origin = HexCoordinate(8, 7)

    assert classify_arc(origin, orientation, HexCoordinate(origin.q + front[0], origin.r + front[1])) is ArcRelation.FRONT
    assert classify_arc(origin, orientation, HexCoordinate(origin.q + rear[0], origin.r + rear[1])) is ArcRelation.REAR


def test_arc_has_lateral_sector() -> None:
    assert classify_arc(HexCoordinate(8, 7), Direction.N, HexCoordinate(10, 6)) is ArcRelation.SIDE


def test_visibility_rejects_out_of_range_and_returns_valid_targets() -> None:
    state = make_state()
    target = state.teams["team_b"].robots["team_b_robot_1"]
    target.position = HexCoordinate(8, 4)

    result = assess_target(state, "team_a_robot_1", target.id)
    assert result.visible
    assert target.id in {item.target_id for item in valid_targets(state, "team_a_robot_1")}

    target.position = HexCoordinate(8, 1)
    result = assess_target(state, "team_a_robot_1", target.id)
    assert result.reason is VisibilityReason.OUT_OF_RANGE


def test_high_intermediate_elevation_blocks_low_line() -> None:
    state = make_state()
    target = state.teams["team_b"].robots["team_b_robot_1"]
    target.position = HexCoordinate(8, 4)
    elevations = [list(row) for row in state.board.elevations]
    elevations[7][8] = 0
    elevations[4][8] = 0
    elevations[6][8] = 1
    state.board = Board(state.board.width, state.board.height, tuple(map(tuple, elevations)))

    result = assess_target(state, "team_a_robot_1", target.id)
    assert result.reason is VisibilityReason.ELEVATION_BLOCKED


def test_elevated_attacker_and_interposed_robot_do_not_block_visibility() -> None:
    state = make_state()
    attacker = state.teams["team_a"].robots["team_a_robot_1"]
    target = state.teams["team_b"].robots["team_b_robot_1"]
    attacker.position = HexCoordinate(8, 7)
    target.position = HexCoordinate(8, 4)
    blocker = state.teams["team_a"].robots["team_a_robot_2"]
    blocker.position = HexCoordinate(8, 6)
    elevations = [list(row) for row in state.board.elevations]
    elevations[7][8] = 1
    elevations[6][8] = 1
    state.board = Board(state.board.width, state.board.height, tuple(map(tuple, elevations)))

    before = (attacker.position, attacker.orientation, target.position)
    result = assess_target(state, attacker.id, target.id)

    assert result.visible
    assert (attacker.position, attacker.orientation, target.position) == before
