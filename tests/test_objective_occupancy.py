from pathlib import Path

from wargame.io.yaml_reader import load_config
from wargame.model import GameState, HexCoordinate


ROOT = Path(__file__).parents[1]


def test_robot_can_occupy_objective_cell(tmp_path: Path) -> None:
    source = (ROOT / "config/example.yaml").read_text(encoding="utf-8")
    source = source.replace("position: {q: 2, r: 0}", "position: {q: 7, r: 7}", 1)
    source = source.replace("imgs/robot_team1.png", str(ROOT / "config/imgs/robot_team1.png"))
    source = source.replace("imgs/robot_team2.png", str(ROOT / "config/imgs/robot_team2.png"))
    path = tmp_path / "robot-on-objective.yaml"
    path.write_text(source, encoding="utf-8")

    state = GameState.from_config(load_config(path))

    assert state.teams["team_a"].robots["team_a_robot_1"].position == HexCoordinate(7, 7)
    assert state.objectives["objective_neutral_1"].position == HexCoordinate(7, 7)
