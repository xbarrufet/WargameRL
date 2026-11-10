import json
from pathlib import Path

import pytest

from wargame.io.yaml_reader import ConfigurationError, load_config
from wargame.model import Direction, GameResult, GameState, HexCoordinate, ModelError, Phase


ROOT = Path(__file__).parents[1]


def test_model_types_and_initial_state() -> None:
    config = load_config(ROOT / "config/example.yaml")
    state = GameState.from_config(config, seed=42)

    assert HexCoordinate(2, 0) < HexCoordinate(3, 0)
    assert list(Direction) == [Direction.N, Direction.NE, Direction.SE, Direction.S, Direction.SW, Direction.NW]
    assert state.phase is Phase.MOVEMENT
    assert state.result is GameResult.PENDING
    assert state.active_team_id == "team_a"
    assert state.round_number == state.turn_number == 1
    assert state.scores == {"team_a": 0, "team_b": 0}
    assert state.seed == 42


def test_entities_preserve_yaml_values_without_mutating_config() -> None:
    config = load_config(ROOT / "config/example.yaml")
    state = GameState.from_config(config)

    robot = state.teams["team_a"].robots["team_a_robot_1"]
    assert robot.position == HexCoordinate(2, 0)
    assert robot.orientation is Direction.N
    assert robot.movement == 3
    assert robot.impacts == 0
    assert not robot.destroyed
    assert state.objectives["objective_neutral_1"].position == HexCoordinate(7, 7)
    assert config.teams[0].robots[0].position.q == 2


def test_json_compatible_round_trip() -> None:
    state = GameState.from_config(load_config(ROOT / "config/example.yaml"), seed=123)
    encoded = state.to_dict()
    json.dumps(encoded)

    restored = GameState.from_dict(encoded)
    assert restored.to_dict() == encoded


def test_invalid_model_state_is_rejected() -> None:
    state = GameState.from_config(load_config(ROOT / "config/example.yaml"))
    state.active_team_id = "missing"

    with pytest.raises(ModelError, match="active_team_id"):
        state.to_dict()


def test_from_config_requires_validated_game_config() -> None:
    with pytest.raises(ModelError, match="GameConfig"):
        GameState.from_config(object())  # type: ignore[arg-type]
