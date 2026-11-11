from pathlib import Path

import pytest

from wargame.engine import EndPhaseAction, execute_end_phase, execute_movement
from wargame.engine import Advance, NormalMovement
from wargame.io.yaml_reader import load_config
from wargame.model import GameState, HexCoordinate, ModelError, Phase


ROOT = Path(__file__).parents[1]


def make_state() -> GameState:
    return GameState.from_config(load_config(ROOT / "config/example.yaml"))


def test_rules_config_survives_state_round_trip() -> None:
    state = make_state()

    restored = GameState.from_dict(state.to_dict())

    assert restored.rules == state.rules


def test_end_phase_advances_in_order_and_keeps_active_team() -> None:
    state = make_state()

    assert execute_end_phase(state) is Phase.SHOOTING
    assert state.active_team_id == "team_a"
    assert execute_end_phase(state, EndPhaseAction(Phase.SHOOTING, "team_a")) is Phase.SCORING
    assert state.active_team_id == "team_a"


def test_scoring_changes_team_and_round_after_both_turns() -> None:
    state = make_state()
    robot = state.teams["team_a"].robots["team_a_robot_1"]
    robot.position = HexCoordinate(2, 0)

    execute_end_phase(state)
    execute_end_phase(state)
    execute_end_phase(state)

    assert state.scores["team_a"] == 1
    assert state.active_team_id == "team_b"
    assert state.phase is Phase.MOVEMENT
    assert state.round_number == 1

    execute_end_phase(state)
    execute_end_phase(state)
    execute_end_phase(state)

    assert state.active_team_id == "team_a"
    assert state.round_number == 2


def test_inactive_team_cannot_move() -> None:
    state = make_state()
    state.active_team_id = "team_b"

    with pytest.raises(ModelError, match="no és l'equip actiu"):
        execute_movement(
            state,
            "team_a_robot_1",
            NormalMovement((Advance(),)),
        )


def test_end_phase_rejects_stale_guards_without_mutation() -> None:
    state = make_state()

    with pytest.raises(ModelError, match="no coincideix"):
        execute_end_phase(state, EndPhaseAction(Phase.SHOOTING, "team_a"))

    assert state.phase is Phase.MOVEMENT
    assert state.active_team_id == "team_a"
