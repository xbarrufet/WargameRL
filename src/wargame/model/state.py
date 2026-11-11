"""Estat global de la partida i conversió des de la configuració YAML."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from wargame.io.yaml_reader import GameConfig, RulesConfig

from .coordinates import HexCoordinate
from .entities import Board, Objective, Robot, Team
from .enums import Direction, GameResult, Phase


class ModelError(ValueError):
    """Indica que no es pot construir o restaurar un estat vàlid."""


@dataclass
class GameState:
    board: Board
    objectives: dict[str, Objective]
    teams: dict[str, Team]
    active_team_id: str
    round_number: int = 1
    turn_number: int = 1
    phase: Phase = Phase.MOVEMENT
    scores: dict[str, int] = field(default_factory=dict)
    result: GameResult = GameResult.PENDING
    seed: int | None = None
    rules: RulesConfig | None = None
    shots_fired: set[str] = field(default_factory=set)
    movement_kinds: dict[str, str] = field(default_factory=dict)
    shot_sequence: int = 0
    victory_pending_team_id: str | None = None

    def occupied_by(self, position: HexCoordinate) -> str | None:
        """Retorna l'identificador del robot actiu que ocupa una casella."""
        for team in self.teams.values():
            for robot in team.robots.values():
                if not robot.destroyed and robot.position == position:
                    return robot.id
        return None

    @classmethod
    def from_config(cls, config: GameConfig, seed: int | None = None) -> "GameState":
        if not isinstance(config, GameConfig):
            raise ModelError("config: s'esperava una GameConfig validada")
        if len(config.teams) != 2:
            raise ModelError("config.teams: calen exactament dos equips")
        team_ids = [team.id for team in config.teams]
        if len(set(team_ids)) != len(team_ids):
            raise ModelError("config.teams: els identificadors han de ser únics")
        teams: dict[str, Team] = {}
        robot_ids: set[str] = set()
        occupied: dict[HexCoordinate, str] = {}
        for team_config in config.teams:
            robots: dict[str, Robot] = {}
            for robot_config in team_config.robots:
                if robot_config.id in robot_ids:
                    raise ModelError(f"robot duplicat: {robot_config.id}")
                position = HexCoordinate(robot_config.position.q, robot_config.position.r)
                if position in occupied:
                    raise ModelError(f"posició ocupada: {position}")
                robot_ids.add(robot_config.id)
                occupied[position] = robot_config.id
                robots[robot_config.id] = Robot(
                    id=robot_config.id,
                    team_id=team_config.id,
                    movement=robot_config.movement,
                    jump=robot_config.jump,
                    range=robot_config.range,
                    damage=robot_config.damage,
                    hit_target=robot_config.hit_target,
                    position=position,
                    orientation=Direction(robot_config.orientation),
                )
            teams[team_config.id] = Team(team_config.id, team_config.sprite, robots)

        objectives: dict[str, Objective] = {}
        for objective_config in config.objectives:
            position = HexCoordinate(objective_config.position.q, objective_config.position.r)
            objectives[objective_config.id] = Objective(
                objective_config.id, position, objective_config.zone
            )

        state = cls(
            board=Board(config.map.width, config.map.height, config.map.elevations),
            objectives=objectives,
            teams=teams,
            active_team_id=team_ids[0],
            scores={team_id: 0 for team_id in team_ids},
            seed=seed,
            rules=config.rules,
            shots_fired=set(),
            movement_kinds={},
            shot_sequence=0,
            victory_pending_team_id=None,
        )
        state.validate()
        return state

    def validate(self) -> None:
        if self.active_team_id not in self.teams:
            raise ModelError(f"active_team_id desconegut: {self.active_team_id}")
        if self.round_number < 1 or self.turn_number < 1:
            raise ModelError("round_number i turn_number han de ser positius")
        if set(self.scores) != set(self.teams):
            raise ModelError("scores ha de contenir exactament els equips")
        if any(score < 0 for score in self.scores.values()):
            raise ModelError("les puntuacions no poden ser negatives")
        if self.shot_sequence < 0:
            raise ModelError("shot_sequence no pot ser negatiu")
        known_robot_ids = {
            robot.id for team in self.teams.values() for robot in team.robots.values()
        }
        if not self.shots_fired <= known_robot_ids:
            raise ModelError("shots_fired conté robots desconeguts")
        if not set(self.movement_kinds) <= known_robot_ids:
            raise ModelError("movement_kinds conté robots desconeguts")
        if self.victory_pending_team_id is not None and self.victory_pending_team_id not in self.teams:
            raise ModelError("victory_pending_team_id desconegut")
        if len(self.teams) != 2:
            raise ModelError("calen exactament dos equips")
        if not isinstance(self.rules, RulesConfig):
            raise ModelError("rules ha de contenir un RulesConfig immutable")
        positions: set[HexCoordinate] = set()
        for team in self.teams.values():
            for robot in team.robots.values():
                if robot.team_id != team.id:
                    raise ModelError(f"robot {robot.id}: equip inconsistent")
                if robot.position in positions:
                    raise ModelError(f"posició ocupada: {robot.position}")
                positions.add(robot.position)
                if robot.impacts < 0:
                    raise ModelError(f"robot {robot.id}: impactes negatius")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "board": {
                "width": self.board.width,
                "height": self.board.height,
                "elevations": [list(row) for row in self.board.elevations],
            },
            "objectives": [
                {
                    "id": objective.id,
                    "position": _position_to_dict(objective.position),
                    "zone": objective.zone,
                }
                for objective in self.objectives.values()
            ],
            "teams": [
                {
                    "id": team.id,
                    "sprite": str(team.sprite),
                    "robots": [_robot_to_dict(robot) for robot in team.robots.values()],
                }
                for team in self.teams.values()
            ],
            "active_team_id": self.active_team_id,
            "round_number": self.round_number,
            "turn_number": self.turn_number,
            "phase": self.phase.value,
            "scores": dict(self.scores),
            "result": self.result.value,
            "seed": self.seed,
            "shots_fired": sorted(self.shots_fired),
            "movement_kinds": dict(self.movement_kinds),
            "shot_sequence": self.shot_sequence,
            "victory_pending_team_id": self.victory_pending_team_id,
            "rules": _rules_to_dict(self.rules),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GameState":
        try:
            board_data = data["board"]
            board = Board(
                board_data["width"],
                board_data["height"],
                tuple(tuple(row) for row in board_data["elevations"]),
            )
            objectives = {
                item["id"]: Objective(
                    item["id"], _position_from_dict(item["position"]), item["zone"]
                )
                for item in data["objectives"]
            }
            teams: dict[str, Team] = {}
            for team_data in data["teams"]:
                robots = {
                    item["id"]: _robot_from_dict(item, team_data["id"])
                    for item in team_data["robots"]
                }
                teams[team_data["id"]] = Team(team_data["id"], Path(team_data["sprite"]), robots)
            state = cls(
                board=board,
                objectives=objectives,
                teams=teams,
                active_team_id=data["active_team_id"],
                round_number=data["round_number"],
                turn_number=data["turn_number"],
                phase=Phase(data["phase"]),
                scores=dict(data["scores"]),
                result=GameResult(data["result"]),
                seed=data.get("seed"),
                rules=_rules_from_dict(data["rules"]),
                shots_fired=set(data.get("shots_fired", [])),
                movement_kinds=dict(data.get("movement_kinds", {})),
                shot_sequence=data.get("shot_sequence", 0),
                victory_pending_team_id=data.get("victory_pending_team_id"),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ModelError(f"estat invàlid: {exc}") from exc
        state.validate()
        return state


def _position_to_dict(position: HexCoordinate) -> dict[str, int]:
    return {"q": position.q, "r": position.r}


def _position_from_dict(data: dict[str, int]) -> HexCoordinate:
    return HexCoordinate(data["q"], data["r"])


def _robot_to_dict(robot: Robot) -> dict[str, Any]:
    return {
        "id": robot.id,
        "team_id": robot.team_id,
        "movement": robot.movement,
        "jump": robot.jump,
        "range": robot.range,
        "damage": robot.damage,
        "hit_target": robot.hit_target,
        "position": _position_to_dict(robot.position),
        "orientation": robot.orientation.value,
        "impacts": robot.impacts,
        "destroyed": robot.destroyed,
    }


def _robot_from_dict(data: dict[str, Any], team_id: str) -> Robot:
    return Robot(
        id=data["id"],
        team_id=team_id,
        movement=data["movement"],
        jump=data["jump"],
        range=data["range"],
        damage=data["damage"],
        hit_target=data["hit_target"],
        position=_position_from_dict(data["position"]),
        orientation=Direction(data["orientation"]),
        impacts=data["impacts"],
        destroyed=data["destroyed"],
    )


def _rules_to_dict(rules: RulesConfig) -> dict[str, Any]:
    return {
        "objective_radius": rules.objective_radius,
        "minimum_objective_distance": rules.minimum_objective_distance,
        "victory_points": rules.victory_points,
        "robot_destruction_points": rules.robot_destruction_points,
        "objective_points": dict(rules.objective_points),
        "armor": dict(rules.armor),
        "robot_max_damage": rules.robot_max_damage,
        "orientations": list(rules.orientations),
    }


def _rules_from_dict(data: dict[str, Any]) -> RulesConfig:
    return RulesConfig(
        objective_radius=data["objective_radius"],
        minimum_objective_distance=data["minimum_objective_distance"],
        victory_points=data["victory_points"],
        robot_destruction_points=data["robot_destruction_points"],
        objective_points=dict(data["objective_points"]),
        armor=dict(data["armor"]),
        robot_max_damage=data["robot_max_damage"],
        orientations=tuple(data["orientations"]),
    )

