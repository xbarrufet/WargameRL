"""Carrega i valida la configuració YAML d'una partida."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class ConfigurationError(ValueError):
    """Indica que una configuració no compleix l'esquema del joc."""


@dataclass(frozen=True)
class Position:
    q: int
    r: int


@dataclass(frozen=True)
class RobotConfig:
    id: str
    movement: int
    jump: int
    range: int
    damage: int
    hit_target: int
    position: Position
    orientation: str


@dataclass(frozen=True)
class TeamConfig:
    id: str
    sprite: Path
    robots: tuple[RobotConfig, ...]


@dataclass(frozen=True)
class ObjectiveConfig:
    id: str
    position: Position
    zone: str


@dataclass(frozen=True)
class MapConfig:
    width: int
    height: int
    elevations: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class RulesConfig:
    objective_radius: int
    minimum_objective_distance: int
    victory_points: int
    robot_destruction_points: int
    objective_points: dict[str, int]
    armor: dict[str, int]
    robot_max_damage: int
    orientations: tuple[str, ...]


@dataclass(frozen=True)
class GameConfig:
    schema_version: int
    map: MapConfig
    objectives: tuple[ObjectiveConfig, ...]
    teams: tuple[TeamConfig, ...]
    rules: RulesConfig


_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
_TOP_LEVEL = {"schema_version", "map", "objectives", "teams", "rules"}
_MAP_FIELDS = {"width", "height", "elevations"}
_OBJECTIVE_FIELDS = {"id", "position", "zone"}
_TEAM_FIELDS = {"id", "sprite", "robots"}
_ROBOT_FIELDS = {"id", "movement", "jump", "range", "damage", "hit_target", "position", "orientation"}
_POSITION_FIELDS = {"q", "r"}
_RULE_FIELDS = {
    "objective_radius",
    "minimum_objective_distance",
    "victory_points",
    "robot_destruction_points",
    "objective_points",
    "armor",
    "robot_max_damage",
    "orientations",
}


def load_config(path: str | Path) -> GameConfig:
    """Carrega i valida una configuració des de *path*."""

    config_path = Path(path).resolve()
    try:
        with config_path.open("r", encoding="utf-8") as stream:
            raw = yaml.safe_load(stream)
    except OSError as exc:
        raise ConfigurationError(f"{config_path}: no es pot llegir ({exc})") from exc
    except yaml.YAMLError as exc:
        raise ConfigurationError(f"YAML invàlid: {exc}") from exc

    _mapping(raw, "root")
    _keys(raw, _TOP_LEVEL, "root")
    _exact_int(raw.get("schema_version"), "schema_version", 1)

    map_config = _parse_map(raw["map"], "map")
    rules = _parse_rules(raw["rules"], "rules")
    objectives = tuple(
        _parse_objective(value, f"objectives[{index}]")
        for index, value in enumerate(_sequence(raw["objectives"], "objectives"))
    )
    teams = tuple(
        _parse_team(value, f"teams[{index}]", config_path.parent, map_config, rules)
        for index, value in enumerate(_sequence(raw["teams"], "teams"))
    )
    _validate_global(map_config, objectives, teams, rules)
    return GameConfig(1, map_config, objectives, teams, rules)


def _parse_map(value: Any, field: str) -> MapConfig:
    data = _mapping(value, field)
    _keys(data, _MAP_FIELDS, field)
    width = _positive_int(data.get("width"), f"{field}.width")
    height = _positive_int(data.get("height"), f"{field}.height")
    if width != 17 or height != 15:
        raise ConfigurationError(f"{field}: les dimensions han de ser 17 x 15")
    rows = _sequence(data.get("elevations"), f"{field}.elevations")
    if len(rows) != height:
        raise ConfigurationError(f"{field}.elevations: s'esperaven {height} files")
    elevations = []
    for row_index, row in enumerate(rows):
        values = _sequence(row, f"{field}.elevations[{row_index}]")
        if len(values) != width:
            raise ConfigurationError(
                f"{field}.elevations[{row_index}]: s'esperaven {width} valors"
            )
        for column_index, elevation in enumerate(values):
            _exact_int(elevation, f"{field}.elevations[{row_index}][{column_index}]")
            if elevation not in (0, 1):
                raise ConfigurationError(
                    f"{field}.elevations[{row_index}][{column_index}]: ha de ser 0 o 1"
                )
        elevations.append(tuple(values))
    return MapConfig(width, height, tuple(elevations))


def _parse_rules(value: Any, field: str) -> RulesConfig:
    data = _mapping(value, field)
    _keys(data, _RULE_FIELDS, field)
    armor = _mapping(data.get("armor"), f"{field}.armor")
    _keys(armor, {"front", "side", "rear"}, f"{field}.armor")
    armor_values = {
        name: _positive_int(value, f"{field}.armor.{name}")
        for name, value in armor.items()
    }
    objective_points = _mapping(data.get("objective_points"), f"{field}.objective_points")
    _keys(objective_points, {"friendly", "neutral", "enemy"}, f"{field}.objective_points")
    objective_point_values = {
        name: _nonnegative_int(point, f"{field}.objective_points.{name}")
        for name, point in objective_points.items()
    }
    orientations = tuple(_sequence(data.get("orientations"), f"{field}.orientations"))
    if not orientations or any(not isinstance(item, str) or not item for item in orientations):
        raise ConfigurationError(f"{field}.orientations: ha de contenir textos no buits")
    if len(set(orientations)) != len(orientations):
        raise ConfigurationError(f"{field}.orientations: no pot contenir duplicats")
    return RulesConfig(
        _positive_int(data.get("objective_radius"), f"{field}.objective_radius"),
        _positive_int(data.get("minimum_objective_distance"), f"{field}.minimum_objective_distance"),
        _positive_int(data.get("victory_points"), f"{field}.victory_points"),
        _positive_int(data.get("robot_destruction_points"), f"{field}.robot_destruction_points"),
        objective_point_values,
        armor_values,
        _positive_int(data.get("robot_max_damage"), f"{field}.robot_max_damage"),
        orientations,
    )


def _parse_objective(value: Any, field: str) -> ObjectiveConfig:
    data = _mapping(value, field)
    _keys(data, _OBJECTIVE_FIELDS, field)
    objective_id = _text(data.get("id"), f"{field}.id")
    position = _parse_position(data.get("position"), f"{field}.position")
    zone = _text(data.get("zone"), f"{field}.zone")
    if zone not in {"team_a", "neutral", "team_b"}:
        raise ConfigurationError(f"{field}.zone: zona desconeguda {zone!r}")
    return ObjectiveConfig(objective_id, position, zone)


def _parse_team(value: Any, field: str, base: Path, map_config: MapConfig, rules: RulesConfig) -> TeamConfig:
    data = _mapping(value, field)
    _keys(data, _TEAM_FIELDS, field)
    sprite_name = _text(data.get("sprite"), f"{field}.sprite")
    sprite = (base / sprite_name).resolve()
    if sprite.suffix.lower() != ".png":
        raise ConfigurationError(f"{field}.sprite: ha de ser un fitxer PNG")
    try:
        signature = sprite.read_bytes()[:8]
    except OSError as exc:
        raise ConfigurationError(f"{field}.sprite: fitxer inexistent o inaccessible") from exc
    if signature != _PNG_SIGNATURE:
        raise ConfigurationError(f"{field}.sprite: no és un PNG vàlid")
    robots = tuple(
        _parse_robot(item, f"{field}.robots[{index}]", map_config, rules)
        for index, item in enumerate(_sequence(data.get("robots"), f"{field}.robots"))
    )
    if not robots:
        raise ConfigurationError(f"{field}.robots: ha de contenir almenys un robot")
    return TeamConfig(_text(data.get("id"), f"{field}.id"), sprite, robots)


def _parse_robot(value: Any, field: str, map_config: MapConfig, rules: RulesConfig) -> RobotConfig:
    data = _mapping(value, field)
    _keys(data, _ROBOT_FIELDS, field)
    orientation = _text(data.get("orientation"), f"{field}.orientation")
    if orientation not in rules.orientations:
        raise ConfigurationError(f"{field}.orientation: valor no permès {orientation!r}")
    position = _parse_position(data.get("position"), f"{field}.position")
    _validate_position(position, map_config, f"{field}.position")
    return RobotConfig(
        _text(data.get("id"), f"{field}.id"),
        _positive_int(data.get("movement"), f"{field}.movement"),
        _positive_int(data.get("jump"), f"{field}.jump"),
        _positive_int(data.get("range"), f"{field}.range"),
        _positive_int(data.get("damage"), f"{field}.damage"),
        _positive_int(data.get("hit_target"), f"{field}.hit_target"),
        position,
        orientation,
    )


def _validate_global(map_config: MapConfig, objectives: tuple[ObjectiveConfig, ...], teams: tuple[TeamConfig, ...], rules: RulesConfig) -> None:
    if len(teams) != 2:
        raise ConfigurationError("teams: la configuració ha de contenir exactament dos equips")
    _unique((item.id for item in objectives), "objectives")
    _unique((item.id for item in teams), "teams")
    robot_ids = [robot.id for team in teams for robot in team.robots]
    _unique(robot_ids, "teams[].robots[].id")
    objective_positions: dict[Position, str] = {}
    for item in objectives:
        _validate_position(item.position, map_config, f"objective {item.id}.position")
        if item.position in objective_positions:
            raise ConfigurationError(f"objectives: posició duplicada a {item.position}")
        objective_positions[item.position] = item.id
    for index, first in enumerate(objectives):
        for second in objectives[index + 1 :]:
            if _hex_distance(first.position, second.position) < rules.minimum_objective_distance:
                raise ConfigurationError(
                    f"objectives: {first.id} i {second.id} estan a menys de "
                    f"{rules.minimum_objective_distance} hexàgons"
                )
    robot_positions: dict[Position, str] = {}
    for team in teams:
        for robot in team.robots:
            if robot.position in robot_positions:
                raise ConfigurationError(f"{robot.id}.position: posició duplicada")
            robot_positions[robot.position] = robot.id


def _mapping(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigurationError(f"{field}: s'esperava un objecte YAML")
    return value


def _sequence(value: Any, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise ConfigurationError(f"{field}: s'esperava una llista YAML")
    return value


def _keys(data: dict[str, Any], expected: set[str], field: str) -> None:
    missing = expected - data.keys()
    unknown = data.keys() - expected
    if missing:
        raise ConfigurationError(f"{field}: falten camps {sorted(missing)}")
    if unknown:
        raise ConfigurationError(f"{field}: camps desconeguts {sorted(unknown)}")


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConfigurationError(f"{field}: s'esperava un text no buit")
    return value


def _exact_int(value: Any, field: str, expected: int | None = None) -> int:
    if type(value) is not int or (expected is not None and value != expected):
        suffix = f" igual a {expected}" if expected is not None else ""
        raise ConfigurationError(f"{field}: s'esperava un enter{suffix}")
    return value


def _positive_int(value: Any, field: str) -> int:
    number = _exact_int(value, field)
    if number <= 0:
        raise ConfigurationError(f"{field}: ha de ser positiu")
    return number


def _nonnegative_int(value: Any, field: str) -> int:
    number = _exact_int(value, field)
    if number < 0:
        raise ConfigurationError(f"{field}: no pot ser negatiu")
    return number


def _parse_position(value: Any, field: str) -> Position:
    data = _mapping(value, field)
    _keys(data, _POSITION_FIELDS, field)
    return Position(_exact_int(data.get("q"), f"{field}.q"), _exact_int(data.get("r"), f"{field}.r"))


def _validate_position(position: Position, map_config: MapConfig, field: str) -> None:
    if not (0 <= position.q < map_config.width and 0 <= position.r < map_config.height):
        raise ConfigurationError(f"{field}: coordenada fora del mapa ({position.q}, {position.r})")


def _hex_distance(first: Position, second: Position) -> int:
    dq = first.q - second.q
    dr = first.r - second.r
    return max(abs(dq), abs(dr), abs(dq + dr))


def _unique(values: Any, field: str) -> None:
    values = list(values)
    if len(values) != len(set(values)):
        raise ConfigurationError(f"{field}: els identificadors han de ser únics")
