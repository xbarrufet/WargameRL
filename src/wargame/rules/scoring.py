"""Regles de puntuació configurables."""

from __future__ import annotations

from wargame.io.yaml_reader import RulesConfig


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

