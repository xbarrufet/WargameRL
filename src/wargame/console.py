"""Adaptador de consola per executar partides sense Pygame."""

from __future__ import annotations

import shlex
from pathlib import Path
from typing import TextIO

from wargame.engine import EndPhaseAction, Jump, ShootAction, execute_end_phase, execute_movement, execute_shot
from wargame.io.yaml_reader import load_config
from wargame.model.coordinates import HexCoordinate
from wargame.model.enums import Direction, GameResult, Phase
from wargame.model.state import GameState, ModelError


def default_config_path() -> Path:
    return Path(__file__).resolve().parents[2] / "config" / "example.yaml"


def create_state(config_path: str | Path | None = None, seed: int | None = None) -> GameState:
    path = Path(config_path) if config_path is not None else default_config_path()
    return GameState.from_config(load_config(path), seed=seed)


def format_status(state: GameState) -> str:
    robots = "; ".join(
        f"{robot.id}@({robot.position.q},{robot.position.r})"
        f"[{robot.team_id}{':destroyed' if robot.destroyed else ''}]"
        for team in state.teams.values()
        for robot in team.robots.values()
    )
    return (
        f"STATUS round={state.round_number} turn={state.turn_number} "
        f"phase={state.phase.value} active_team={state.active_team_id} "
        f"scores={state.scores} result={state.result.value} robots={robots}"
    )


def format_initial(state: GameState, config_path: Path) -> str:
    robots = [robot.id for team in state.teams.values() for robot in team.robots.values()]
    return f"CONFIG {config_path}\nSEED {state.seed}\nROBOTS {', '.join(robots)}\n{format_status(state)}"


def run_demo(state: GameState, output: TextIO, max_rounds: int = 15) -> None:
    output.write("MODE demo\n")
    while state.result is GameResult.PENDING and state.round_number <= max_rounds:
        previous = (state.round_number, state.active_team_id, state.phase)
        execute_end_phase(state, EndPhaseAction(state.phase, state.active_team_id))
        output.write(f"TRANSITION {previous[0]} {previous[1]} {previous[2].value} -> {format_status(state)}\n")
    if any(score >= state.rules.victory_points for score in state.scores.values()):
        output.write("END_REASON victory_points\n")
    else:
        output.write("END_REASON round_limit\n")
    output.write(f"FINAL {state.result.value} scores={state.scores} round={state.round_number}\n")


def execute_command(state: GameState, line: str, output: TextIO) -> bool:
    """Executa una ordre manual. Retorna False quan cal sortir."""
    parts = shlex.split(line)
    if not parts:
        return True
    command = parts[0].lower()
    if command == "quit":
        return False
    if command == "help":
        output.write("help | status | end | move ROBOT Q R ORIENTATION | shoot ATTACKER TARGET | quit\n")
        return True
    if command == "status":
        output.write(format_status(state) + "\n")
        return True
    if command == "end" and len(parts) == 1:
        execute_end_phase(state, EndPhaseAction(state.phase, state.active_team_id))
        output.write(format_status(state) + "\n")
        return True
    if command == "move" and len(parts) == 5:
        robot_id, q, r, orientation = parts[1], int(parts[2]), int(parts[3]), Direction(parts[4].upper())
        result = execute_movement(state, robot_id, Jump(HexCoordinate(q, r), orientation))
        output.write(f"MOVE {result.robot_id} {result.origin}->{result.destination}\n")
        return True
    if command == "shoot" and len(parts) == 3:
        result = execute_shot(state, ShootAction(parts[1], parts[2]))
        output.write(f"SHOOT {result.attacker_id}->{result.target_id} hit={result.hit} impacts={result.impacts_caused}\n")
        return True
    raise ModelError("ordre desconeguda o nombre d’arguments incorrecte")


def run_manual(state: GameState, input_stream: TextIO, output: TextIO) -> None:
    output.write("MODE manual\nType 'help' for commands.\n")
    for line in input_stream:
        try:
            if not execute_command(state, line.strip(), output):
                break
        except (ModelError, ValueError, IndexError) as error:
            output.write(f"ERROR {error}\n")

