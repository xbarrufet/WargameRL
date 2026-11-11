from pathlib import Path

import pytest

from wargame.io.yaml_reader import ConfigurationError, load_config


ROOT = Path(__file__).parents[1]


def test_example_config_loads() -> None:
    config = load_config(ROOT / "config/example.yaml")

    assert config.schema_version == 1
    assert (config.map.width, config.map.height) == (17, 15)
    assert len(config.teams) == 2
    assert config.rules.objective_points == {"friendly": 1, "neutral": 3, "enemy": 5}
    assert config.teams[0].sprite == (ROOT / "config/imgs/robot_team1.png").resolve()
    assert config.teams[0].robots[0].position.q == 2


def test_unknown_field_is_rejected(tmp_path: Path) -> None:
    path = _copy_example(tmp_path)
    text = path.read_text(encoding="utf-8").replace("schema_version: 1", "schema_version: 1\nunknown: true")
    path.write_text(text, encoding="utf-8")

    with pytest.raises(ConfigurationError, match="camps desconeguts"):
        load_config(path)


def test_out_of_bounds_position_reports_field(tmp_path: Path) -> None:
    path = _copy_example(tmp_path)
    text = path.read_text(encoding="utf-8").replace("position: {q: 2, r: 0}", "position: {q: 17, r: 0}", 1)
    path.write_text(text, encoding="utf-8")

    with pytest.raises(ConfigurationError, match=r"teams\[0\]\.robots\[0\]\.position"):
        load_config(path)


def test_invalid_sprite_is_rejected(tmp_path: Path) -> None:
    path = _copy_example(tmp_path)
    sprite = path.parent / "imgs/robot_team1.png"
    sprite.write_bytes(b"not png")
    text = path.read_text(encoding="utf-8").replace("imgs/robot_team1.png", "imgs/robot_team1.png")
    path.write_text(text, encoding="utf-8")

    with pytest.raises(ConfigurationError, match="no és un PNG vàlid"):
        load_config(path)


@pytest.mark.parametrize("replacement", [
    "objective_points: {friendly: 1, neutral: 3}",
    "objective_points: {friendly: 1, neutral: text, enemy: 5}",
    "objective_points: {friendly: 1.5, neutral: 3, enemy: 5}",
    "objective_points: {friendly: -1, neutral: 3, enemy: 5}",
])
def test_invalid_objective_points_are_rejected(tmp_path: Path, replacement: str) -> None:
    path = _copy_example(tmp_path)
    text = path.read_text(encoding="utf-8").replace(
        "objective_points: {friendly: 1, neutral: 3, enemy: 5}", replacement
    )
    path.write_text(text, encoding="utf-8")

    with pytest.raises(ConfigurationError, match="objective_points"):
        load_config(path)


def test_custom_objective_points_are_loaded(tmp_path: Path) -> None:
    path = _copy_example(tmp_path)
    text = path.read_text(encoding="utf-8").replace(
        "objective_points: {friendly: 1, neutral: 3, enemy: 5}",
        "objective_points: {friendly: 2, neutral: 6, enemy: 9}",
    )
    path.write_text(text, encoding="utf-8")

    assert load_config(path).rules.objective_points == {"friendly": 2, "neutral": 6, "enemy": 9}


@pytest.mark.parametrize(
    "replacement",
    [
        "        range: 5\n        damage: 2\n        hit_target: 4",
        "        jump: 0",
        "        jump: invalid",
        "        hit_target: 0",
        "        hit_target: invalid",
    ],
)
def test_invalid_robot_movement_or_hit_values_are_rejected(
    tmp_path: Path, replacement: str
) -> None:
    path = _copy_example(tmp_path)
    text = path.read_text(encoding="utf-8")
    if replacement.startswith("        range"):
        text = text.replace("        jump: 4\n        range: 5\n        damage: 2\n        hit_target: 4", replacement, 1)
    elif replacement.startswith("        jump"):
        text = text.replace("        jump: 4", replacement, 1)
    else:
        text = text.replace("        hit_target: 4", replacement, 1)
    path.write_text(text, encoding="utf-8")

    with pytest.raises(ConfigurationError, match=r"teams\[0\]\.robots\[0\]"):
        load_config(path)


def _copy_example(tmp_path: Path) -> Path:
    source = ROOT / "config/example.yaml"
    path = tmp_path / "example.yaml"
    path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    sprite_dir = tmp_path / "imgs"
    sprite_dir.mkdir()
    for name in ("robot_team1.png", "robot_team2.png"):
        (sprite_dir / name).write_bytes((ROOT / "config/imgs" / name).read_bytes())
    return path
