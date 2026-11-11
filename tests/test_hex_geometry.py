from math import sqrt
from pathlib import Path

import pytest

from wargame.io.yaml_reader import load_config
from wargame.model import FlatTopProjection, GameState, HexCoordinate, hex_distance


ROOT = Path(__file__).parents[1]


def test_neighbors_and_distance_use_axial_geometry() -> None:
    center = HexCoordinate(5, 5)
    assert len(center.neighbors()) == 6
    assert len({HexCoordinate(5, 5).distance_to(neighbor) for neighbor in center.neighbors()}) == 1
    assert hex_distance(center, HexCoordinate(7, 3)) == 2


def test_board_filters_edge_neighbors_and_reads_elevation() -> None:
    state = GameState.from_config(load_config(ROOT / "config/example.yaml"))

    assert len(state.board.neighbors(HexCoordinate(0, 0))) == 2
    assert state.board.elevation_at(HexCoordinate(8, 5)) == 1
    assert not state.board.contains(HexCoordinate(-1, 0))
    with pytest.raises(ValueError, match="fora del tauler"):
        state.board.elevation_at(HexCoordinate(-1, 0))


def test_state_reports_robot_occupancy_and_ignores_destroyed_robot() -> None:
    state = GameState.from_config(load_config(ROOT / "config/example.yaml"))
    robot = state.teams["team_a"].robots["team_a_robot_1"]

    assert state.occupied_by(robot.position) == robot.id
    assert state.occupied_by(HexCoordinate(0, 0)) is None
    robot.destroyed = True
    assert state.occupied_by(robot.position) is None


def test_flat_top_projection_round_trips_centers_and_rejects_outside_points() -> None:
    projection = FlatTopProjection(size=10, origin_x=100, origin_y=200)
    coordinate = HexCoordinate(2, 3)
    center = projection.to_screen(coordinate)

    assert center == (130.0, 200.0 + 40 * sqrt(3))
    assert projection.from_screen(center, width=17, height=15) == coordinate
    assert projection.from_screen((0, 0), width=17, height=15) is None


def test_flat_top_projection_rejects_non_positive_size() -> None:
    with pytest.raises(ValueError, match="size"):
        FlatTopProjection(size=0)
