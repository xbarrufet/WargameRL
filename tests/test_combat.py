from pathlib import Path

import pytest

from wargame.engine import (
    EndPhaseAction,
    ShootAction,
    execute_end_phase,
    execute_shot,
)
from wargame.io.yaml_reader import load_config
from wargame.model import GameState, HexCoordinate, ModelError, Phase
from wargame.rules import ArcRelation


ROOT = Path(__file__).parents[1]


def make_state(seed: int = 0) -> GameState:
    state = GameState.from_config(load_config(ROOT / "config/example.yaml"), seed=seed)
    attacker = state.teams["team_a"].robots["team_a_robot_1"]
    target = state.teams["team_b"].robots["team_b_robot_1"]
    other_a = state.teams["team_a"].robots["team_a_robot_2"]
    other_b = state.teams["team_b"].robots["team_b_robot_2"]
    attacker.position = HexCoordinate(8, 7)
    target.position = HexCoordinate(8, 4)
    other_a.position = HexCoordinate(0, 0)
    other_b.position = HexCoordinate(16, 14)
    state.phase = Phase.SHOOTING
    return state


def test_new_state_has_no_shots_and_round_trip_preserves_shot_tracking() -> None:
    state = make_state()
    assert state.shots_fired == set()
    execute_shot(state, ShootAction("team_a_robot_1", "team_b_robot_1"))

    restored = GameState.from_dict(state.to_dict())

    assert restored.shots_fired == {"team_a_robot_1"}
    assert restored.shot_sequence == state.shot_sequence
    assert restored.to_dict() == state.to_dict()


def test_same_seed_reproduces_hit_and_save_rolls() -> None:
    first = execute_shot(make_state(5), ShootAction("team_a_robot_1", "team_b_robot_1"))
    second = execute_shot(make_state(5), ShootAction("team_a_robot_1", "team_b_robot_1"))

    assert first == second
    assert first.hit_roll == 5
    assert len(first.save_rolls) == 2


@pytest.mark.parametrize(("kind", "expected"), [(None, 1), ("normal", 0), ("jump", -2)])
def test_movement_modifiers_are_reported(kind, expected) -> None:
    state = make_state(0)
    if kind is not None:
        state.movement_kinds["team_a_robot_1"] = kind

    result = execute_shot(state, ShootAction("team_a_robot_1", "team_b_robot_1"))

    assert result.hit_modifier == expected


def test_defensive_arc_selects_lateral_armor_and_failed_saves_cause_damage() -> None:
    state = make_state(5)
    target = state.teams["team_b"].robots["team_b_robot_1"]
    target.orientation = target.orientation.NE
    target.position = HexCoordinate(8, 4)
    attacker = state.teams["team_a"].robots["team_a_robot_1"]
    attacker.position = HexCoordinate(10, 6)

    result = execute_shot(state, ShootAction(attacker.id, target.id))

    assert result.defense_relation is ArcRelation.SIDE
    assert result.armor == state.rules.armor["side"]
    assert result.impacts_caused == sum(roll < result.armor for roll in result.save_rolls)
    assert target.impacts == result.impacts_caused


def test_destroying_robot_awards_points_once_and_blocks_follow_up_actions() -> None:
    state = make_state(0)
    target = state.teams["team_b"].robots["team_b_robot_1"]
    target.impacts = state.rules.robot_max_damage - 1

    result = execute_shot(state, ShootAction("team_a_robot_1", target.id))

    assert result.target_destroyed
    assert target.destroyed
    assert state.scores["team_a"] == state.rules.robot_destruction_points
    assert state.occupied_by(target.position) is None
    with pytest.raises(ModelError, match="robot destruït"):
        execute_shot(state, ShootAction("team_a_robot_2", target.id))


def test_shot_validation_is_atomic_and_shot_resets_on_next_turn() -> None:
    state = make_state()
    state.active_team_id = "team_b"
    with pytest.raises(ModelError, match="no és l'equip actiu"):
        execute_shot(state, ShootAction("team_a_robot_1", "team_b_robot_1"))
    assert not state.shots_fired

    state.active_team_id = "team_a"
    execute_shot(state, ShootAction("team_a_robot_1", "team_b_robot_1"))
    with pytest.raises(ModelError, match="ja ha disparat"):
        execute_shot(state, ShootAction("team_a_robot_1", "team_b_robot_1"))

    execute_end_phase(state, EndPhaseAction(Phase.SHOOTING, "team_a"))
    execute_end_phase(state, EndPhaseAction(Phase.SCORING, "team_a"))
    assert state.phase is Phase.MOVEMENT
    assert not state.shots_fired
