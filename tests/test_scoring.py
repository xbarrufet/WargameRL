from pathlib import Path

from wargame.io.yaml_reader import load_config
from wargame.rules import objective_points_for


ROOT = Path(__file__).parents[1]


def test_objective_points_are_relative_to_scoring_team() -> None:
    rules = load_config(ROOT / "config/example.yaml").rules

    assert objective_points_for(rules, "team_a", "team_a") == 1
    assert objective_points_for(rules, "neutral", "team_a") == 3
    assert objective_points_for(rules, "team_b", "team_a") == 5
    assert objective_points_for(rules, "team_a", "team_b") == 5
