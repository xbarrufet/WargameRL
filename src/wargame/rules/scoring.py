"""Regles de puntuació configurables."""

from __future__ import annotations

from wargame.io.yaml_reader import RulesConfig
from wargame.model.coordinates import HexCoordinate
from wargame.model.state import GameState


def objective_points_for(
    rules: RulesConfig, objective_zone: str, scoring_team_id: str
) -> int:
    """Retorna els punts d'un objectiu segons la relació amb l'equip actiu."""

    if objective_zone == "neutral":
        relation = "neutral"
    elif objective_zone == scoring_team_id:
        relation = "friendly"
    elif objective_zone in {"team_a", "team_b"}:
        relation = "enemy"
    else:
        raise ValueError(f"zona d'objectiu desconeguda: {objective_zone!r}")
    return rules.objective_points[relation]


def objective_controller(
    state: GameState, objective_position: HexCoordinate
) -> str | None:
    """Retorna l'equip amb majoria estricta de robots dins del radi."""
    counts = {
        team_id: sum(
            not robot.destroyed
            and robot.position.distance_to(objective_position) <= state.rules.objective_radius
            for robot in team.robots.values()
        )
        for team_id, team in state.teams.items()
    }
    ordered = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    if not ordered or ordered[0][1] == 0:
        return None
    if len(ordered) > 1 and ordered[0][1] == ordered[1][1]:
        return None
    return ordered[0][0]

