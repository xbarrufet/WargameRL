"""Màquina de fases i cicle de torn de la partida."""

from __future__ import annotations

from dataclasses import dataclass

from wargame.model.enums import GameResult, Phase
from wargame.model.state import GameState, ModelError
from wargame.rules.scoring import objective_controller, objective_points_for


@dataclass(frozen=True)
class EndPhaseAction:
    """Finalitza la fase actual, opcionalment amb garanties d'estat."""

    phase: Phase | None = None
    team_id: str | None = None


def validate_robot_action(state: GameState, robot_id: str, phase: Phase) -> None:
    """Valida que un robot actua en la fase i equip correctes."""
    if state.result is not GameResult.PENDING:
        raise ModelError("game: la partida ja ha acabat")
    if state.phase is not phase:
        raise ModelError(f"phase: acció no vàlida durant {state.phase.value}")
    for team in state.teams.values():
        if robot_id in team.robots:
            if team.id != state.active_team_id:
                raise ModelError(f"team: l'equip {team.id} no és l'equip actiu")
            if team.robots[robot_id].destroyed:
                raise ModelError(f"robot destruït: {robot_id}")
            return
    raise ModelError(f"robot desconegut: {robot_id}")


def execute_end_phase(state: GameState, action: EndPhaseAction | None = None) -> Phase:
    """Aplica una transició de fase completa i atòmica."""
    if state.result is not GameResult.PENDING:
        raise ModelError("game: la partida ja ha acabat")
    action = action or EndPhaseAction()
    if not isinstance(action, EndPhaseAction):
        raise ModelError("phase: acció de finalització desconeguda")
    if action.phase is not None and action.phase is not state.phase:
        raise ModelError("phase: la fase esperada no coincideix amb l'estat")
    if action.team_id is not None and action.team_id != state.active_team_id:
        raise ModelError("team: l'equip esperat no coincideix amb l'estat")

    if state.phase is Phase.MOVEMENT:
        state.phase = Phase.SHOOTING
    elif state.phase is Phase.SHOOTING:
        state.phase = Phase.SCORING
    else:
        _score_active_team(state)
        team_ids = list(state.teams)
        active_index = team_ids.index(state.active_team_id)
        if _should_finish_after_scoring(state, active_index, len(team_ids)):
            _finish_game(state)
            return state.phase
        next_index = (active_index + 1) % len(team_ids)
        if next_index == 0:
            state.round_number += 1
        state.active_team_id = team_ids[next_index]
        state.turn_number += 1
        state.phase = Phase.MOVEMENT
        state.shots_fired.clear()
        state.movement_kinds.clear()
    return state.phase


def _score_active_team(state: GameState) -> None:
    active_team_id = state.active_team_id
    for objective in state.objectives.values():
        if objective_controller(state, objective.position) != active_team_id:
            continue
        state.scores[active_team_id] += objective_points_for(
            state.rules, objective.zone, active_team_id
        )

    if state.scores[active_team_id] >= state.rules.victory_points:
        team_ids = list(state.teams)
        if team_ids.index(active_team_id) == 0:
            state.victory_pending_team_id = active_team_id


def _should_finish_after_scoring(state: GameState, active_index: int, team_count: int) -> bool:
    """Determina si el torn actual és el darrer abans de fixar el resultat."""
    if active_index == team_count - 1 and (
        state.victory_pending_team_id is not None
        or any(score >= state.rules.victory_points for score in state.scores.values())
        or state.round_number >= 15
    ):
        return True
    return False


def _finish_game(state: GameState) -> None:
    team_ids = list(state.teams)
    first, second = team_ids[0], team_ids[1]
    if state.scores[first] > state.scores[second]:
        state.result = GameResult.TEAM_A_WINS
    elif state.scores[second] > state.scores[first]:
        state.result = GameResult.TEAM_B_WINS
    else:
        state.result = GameResult.DRAW
