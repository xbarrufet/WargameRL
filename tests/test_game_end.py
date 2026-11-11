from pathlib import Path

import pytest

from wargame.engine import EndPhaseAction, execute_end_phase
from wargame.io.yaml_reader import load_config
from wargame.model import GameResult, GameState, HexCoordinate, ModelError, Phase


ROOT = Path(__file__).parents[1]


def make_state() -> GameState:
    return GameState.from_config(load_config(ROOT / "config/example.yaml"))


def finish_movement_and_shooting(state: GameState) -> None:
    execute_end_phase(state)
    execute_end_phase(state)


def test_objective_control_scores_majority_and_ignores_destroyed_robot() -> None:
    state = make_state()
    objective = state.objectives["objective_neutral_1"]
    active = state.teams["team_a"].robots["team_a_robot_1"]
    support = state.teams["team_a"].robots["team_a_robot_2"]
    enemy = state.teams["team_b"].robots["team_b_robot_1"]
    active.position = objective.position
    support.position = objective.position
    enemy.position = objective.position
    enemy.destroyed = True
    state.phase = Phase.SCORING

    execute_end_phase(state)

    assert state.scores["team_a"] == 3
    assert state.scores["team_b"] == 0


def test_tied_objective_does_not_score_and_objective_scores_again_next_turn() -> None:
    state = make_state()
    objective = state.objectives["objective_neutral_1"]
    state.teams["team_a"].robots["team_a_robot_1"].position = objective.position
    state.teams["team_b"].robots["team_b_robot_1"].position = objective.position
    state.phase = Phase.SCORING

    execute_end_phase(state)

    assert state.scores["team_a"] == 0
    assert state.active_team_id == "team_b"

    state.active_team_id = "team_a"
    state.phase = Phase.SCORING
    state.teams["team_b"].robots["team_b_robot_1"].destroyed = True
    execute_end_phase(state)

    assert state.scores["team_a"] == 3


def test_first_team_victory_waits_for_second_team_and_survives_round_trip() -> None:
    state = make_state()
    objective = state.objectives["objective_a_1"]
    state.teams["team_a"].robots["team_a_robot_1"].position = HexCoordinate(2, 1)
    state.scores["team_a"] = state.rules.victory_points - 1
    state.phase = Phase.SCORING

    execute_end_phase(state)

    assert state.result is GameResult.PENDING
    assert state.victory_pending_team_id == "team_a"
    assert state.active_team_id == "team_b"
    restored = GameState.from_dict(state.to_dict())
    assert restored.victory_pending_team_id == "team_a"

    finish_movement_and_shooting(restored)
    execute_end_phase(restored)

    assert restored.result is GameResult.TEAM_A_WINS


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        ({"team_a": 15, "team_b": 10}, GameResult.TEAM_A_WINS),
        ({"team_a": 10, "team_b": 15}, GameResult.TEAM_B_WINS),
        ({"team_a": 10, "team_b": 10}, GameResult.DRAW),
    ],
)
def test_second_team_completion_sets_final_result(scores, expected) -> None:
    state = make_state()
    state.scores.update(scores)
    state.active_team_id = "team_b"
    state.phase = Phase.SCORING
    state.round_number = 15
    for robot in state.teams["team_a"].robots.values():
        robot.position = HexCoordinate(0, 0) if robot.id.endswith("1") else HexCoordinate(0, 1)
    for robot in state.teams["team_b"].robots.values():
        robot.position = HexCoordinate(16, 14) if robot.id.endswith("1") else HexCoordinate(16, 13)

    execute_end_phase(state)

    assert state.result is expected


def test_round_fifteen_ends_in_final_score_comparison() -> None:
    state = make_state()
    state.round_number = 15
    state.active_team_id = "team_b"
    state.phase = Phase.SCORING
    state.scores["team_a"] = 4
    state.scores["team_b"] = 2

    execute_end_phase(state)

    assert state.result is GameResult.TEAM_A_WINS
    assert state.round_number == 15


def test_finished_game_rejects_phase_transition_without_mutation() -> None:
    state = make_state()
    state.result = GameResult.DRAW
    before = state.to_dict()

    with pytest.raises(ModelError, match="ja ha acabat"):
        execute_end_phase(state, EndPhaseAction())

    assert state.to_dict() == before
