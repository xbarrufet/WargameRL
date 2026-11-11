"""Execució atòmica i reproduïble dels dispars."""

from __future__ import annotations

from dataclasses import dataclass
import random

from wargame.model.enums import Phase
from wargame.model.state import GameState, ModelError
from wargame.rules.combat import movement_modifier
from wargame.rules.visibility import ArcRelation, assess_target, classify_arc
from .turn import validate_robot_action


@dataclass(frozen=True)
class ShootAction:
    attacker_id: str
    target_id: str


@dataclass(frozen=True)
class CombatResult:
    attacker_id: str
    target_id: str
    hit_roll: int
    hit_modifier: int
    hit_target: int
    hit: bool
    defense_relation: ArcRelation
    armor: int
    save_rolls: tuple[int, ...]
    impacts_caused: int
    target_impacts: int
    target_destroyed: bool
    destruction_points: int


def execute_shot(state: GameState, action: ShootAction) -> CombatResult:
    if not isinstance(action, ShootAction):
        raise ModelError("combat: acció de dispar desconeguda")
    validate_robot_action(state, action.attacker_id, Phase.SHOOTING)
    if action.attacker_id in state.shots_fired:
        raise ModelError(f"combat: el robot ja ha disparat: {action.attacker_id}")
    attacker = _find_robot(state, action.attacker_id)
    target = _find_robot(state, action.target_id)
    visibility = assess_target(state, action.attacker_id, action.target_id)
    if not visibility.visible:
        reason = visibility.reason.value if visibility.reason else "invalid_target"
        raise ModelError(f"combat: blanc no vàlid ({reason})")
    if attacker.team_id == target.team_id:
        raise ModelError("combat: no es pot disparar a un aliat")

    defense_relation = classify_arc(target.position, target.orientation, attacker.position)
    armor = state.rules.armor[defense_relation.value]
    modifier = movement_modifier(state.movement_kinds.get(attacker.id))
    rng = random.Random(None if state.seed is None else state.seed + state.shot_sequence)
    hit_roll = rng.randint(1, 6)
    state.shot_sequence += 1
    state.shots_fired.add(attacker.id)
    save_rolls: tuple[int, ...] = ()
    impacts_caused = 0
    destroyed = False
    destruction_points = 0
    if hit_roll + modifier >= attacker.hit_target:
        save_rolls = tuple(rng.randint(1, 6) for _ in range(attacker.damage))
        impacts_caused = sum(roll < armor for roll in save_rolls)
        target.impacts += impacts_caused
        if target.impacts >= state.rules.robot_max_damage and not target.destroyed:
            target.destroyed = True
            destroyed = True
            destruction_points = state.rules.robot_destruction_points
            state.scores[attacker.team_id] += destruction_points
    return CombatResult(
        attacker.id, target.id, hit_roll, modifier, attacker.hit_target,
        hit_roll + modifier >= attacker.hit_target, defense_relation, armor,
        save_rolls, impacts_caused, target.impacts, target.destroyed,
        destruction_points,
    )


def _find_robot(state: GameState, robot_id: str):
    for team in state.teams.values():
        if robot_id in team.robots:
            robot = team.robots[robot_id]
            if robot.destroyed:
                raise ModelError(f"combat: robot destruït: {robot_id}")
            return robot
    raise ModelError(f"combat: robot desconegut: {robot_id}")
