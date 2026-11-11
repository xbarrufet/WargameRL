"""Client gràfic Pygame del motor WargameRL.

La UI només consulta l'estat i envia accions públiques al motor.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pygame

from wargame.engine import (
    EndPhaseAction,
    Jump,
    MovementKind,
    ShootAction,
    accessible_destinations,
    execute_end_phase,
    execute_movement,
    execute_shot,
)
from wargame.model.coordinates import FlatTopProjection, HexCoordinate
from wargame.model.enums import Direction, GameResult, Phase
from wargame.model.state import GameState, ModelError
from wargame.rules.visibility import valid_targets


@dataclass
class Selection:
    robot_id: str | None = None
    cell: HexCoordinate | None = None


class GameRenderer:
    """Dibuixa l'estat actual en una superfície Pygame."""

    COLORS = {
        "background": (28, 32, 42),
        "low": (62, 91, 73),
        "high": (104, 126, 84),
        "grid": (145, 157, 166),
        "neutral": (128, 128, 128),
        "team_a": (75, 145, 235),
        "team_b": (224, 91, 81),
        "selected": (250, 218, 77),
        "option": (95, 215, 170),
        "text": (238, 241, 245),
    }

    def __init__(self, state: GameState, size: int = 24, panel_width: int = 260) -> None:
        self.state = state
        self.panel_width = panel_width
        self.projection = FlatTopProjection(size, origin_x=size + 8, origin_y=size + 8)
        self.surface: pygame.Surface | None = None
        self.font: pygame.font.Font | None = None
        self.sprites: dict[str, pygame.Surface] = {}

    @property
    def board_size(self) -> tuple[int, int]:
        width = int(self.projection.origin_x + self.projection.size * 1.5 * (self.state.board.width - 1) + self.projection.size + 16)
        height = int(self.projection.origin_y + self.projection.size * 1.732 * (self.state.board.height + self.state.board.width / 2) + 16)
        return width + self.panel_width, height

    def setup(self, surface: pygame.Surface) -> None:
        self.surface = surface
        self.font = pygame.font.Font(None, 22)
        for team in self.state.teams.values():
            try:
                image = pygame.image.load(team.sprite).convert_alpha()
                self.sprites[team.id] = pygame.transform.smoothscale(image, (int(self.projection.size * 1.5), int(self.projection.size * 1.5)))
            except (pygame.error, OSError):
                self.sprites[team.id] = pygame.Surface((int(self.projection.size * 1.5), int(self.projection.size * 1.5)), pygame.SRCALPHA)

    def hex_points(self, coordinate: HexCoordinate) -> list[tuple[int, int]]:
        center_x, center_y = self.projection.to_screen(coordinate)
        return [
            (round(center_x + self.projection.size * __import__("math").cos(__import__("math").radians(angle))),
             round(center_y + self.projection.size * __import__("math").sin(__import__("math").radians(angle))))
            for angle in range(0, 360, 60)
        ]

    def draw(self, selection: Selection | None = None) -> None:
        if self.surface is None or self.font is None:
            raise RuntimeError("renderer no inicialitzat")
        selection = selection or Selection()
        self.surface.fill(self.COLORS["background"])
        options = self.options(selection.robot_id)
        for r in range(self.state.board.height):
            for q in range(self.state.board.width):
                coordinate = HexCoordinate(q, r)
                color = self.COLORS["high" if self.state.board.elevation_at(coordinate) else "low"]
                if coordinate in options:
                    color = self.COLORS["option"]
                if coordinate == selection.cell:
                    color = self.COLORS["selected"]
                pygame.draw.polygon(self.surface, color, self.hex_points(coordinate))
                pygame.draw.polygon(self.surface, self.COLORS["grid"], self.hex_points(coordinate), 1)
        for objective in self.state.objectives.values():
            center = tuple(round(value) for value in self.projection.to_screen(objective.position))
            pygame.draw.circle(self.surface, self.COLORS.get(objective.zone, self.COLORS["neutral"]), center, max(4, int(self.projection.size / 3)), 2)
        for team in self.state.teams.values():
            for robot in team.robots.values():
                if robot.destroyed:
                    continue
                center = tuple(round(value) for value in self.projection.to_screen(robot.position))
                sprite = self.sprites.get(team.id)
                if sprite and sprite.get_bounding_rect().width:
                    self.surface.blit(sprite, sprite.get_rect(center=center))
                else:
                    pygame.draw.circle(self.surface, self.COLORS.get(team.id, self.COLORS["neutral"]), center, int(self.projection.size / 2))
                if robot.id == selection.robot_id:
                    pygame.draw.circle(self.surface, self.COLORS["selected"], center, int(self.projection.size * .7), 2)
        self._draw_panel(selection)

    def options(self, robot_id: str | None) -> frozenset[HexCoordinate] | set[HexCoordinate]:
        if not robot_id or self.state.result is not GameResult.PENDING:
            return set()
        if self.state.phase is Phase.MOVEMENT:
            return accessible_destinations(self.state, robot_id, MovementKind.JUMP)
        if self.state.phase is Phase.SHOOTING:
            return {self._robot(target.target_id).position for target in valid_targets(self.state, robot_id)}
        return set()

    def _draw_panel(self, selection: Selection) -> None:
        x = self.board_size[0] - self.panel_width + 12
        lines = [
            f"Ronda {self.state.round_number} / torn {self.state.turn_number}",
            f"Fase: {self.state.phase.value}",
            f"Actiu: {self.state.active_team_id}",
            f"Punts: {self.state.scores}",
            f"Robot: {selection.robot_id or '-'}",
            f"Casella: {selection.cell or '-'}",
            "Clic: seleccionar / actuar",
            "E: finalitzar fase",
        ]
        if self.state.result is not GameResult.PENDING:
            lines += ["", f"FINAL: {self.state.result.value}"]
        for index, line in enumerate(lines):
            self.surface.blit(self.font.render(line, True, self.COLORS["text"]), (x, 18 + index * 24))

    def _robot(self, robot_id: str):
        for team in self.state.teams.values():
            if robot_id in team.robots:
                return team.robots[robot_id]
        raise ModelError(f"robot desconegut: {robot_id}")


class PygameGame:
    """Controlador d'entrada i delegació d'accions al motor."""

    def __init__(self, state: GameState, *, headless: bool = False) -> None:
        self.state = state
        self.selection = Selection()
        self.message = ""
        self.headless = headless
        self.renderer = GameRenderer(state)
        self.surface: pygame.Surface | None = None

    def setup(self) -> None:
        if not pygame.get_init():
            pygame.init()
        flags = 0
        self.surface = pygame.Surface(self.renderer.board_size) if self.headless else pygame.display.set_mode(self.renderer.board_size)
        self.renderer.setup(self.surface)

    def handle_event(self, event: pygame.event.Event) -> None:
        try:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                execute_end_phase(self.state, EndPhaseAction(self.state.phase, self.state.active_team_id))
                self.selection = Selection()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._click(event.pos)
        except (ModelError, ValueError) as error:
            self.message = str(error)

    def _click(self, point: tuple[int, int]) -> None:
        cell = self.renderer.projection.from_screen(point, self.state.board.width, self.state.board.height)
        if cell is None:
            return
        self.selection.cell = cell
        robot = self.state.occupied_by(cell)
        if robot and self._robot(robot).team_id == self.state.active_team_id:
            self.selection.robot_id = robot
            return
        if not self.selection.robot_id or cell not in self.renderer.options(self.selection.robot_id):
            return
        if self.state.phase is Phase.MOVEMENT:
            current = self._robot(self.selection.robot_id)
            execute_movement(self.state, self.selection.robot_id, Jump(cell, current.orientation))
        elif self.state.phase is Phase.SHOOTING:
            target = next((item.target_id for item in valid_targets(self.state, self.selection.robot_id) if self._robot(item.target_id).position == cell), None)
            if target:
                execute_shot(self.state, ShootAction(self.selection.robot_id, target))
        self.message = ""

    def _robot(self, robot_id: str):
        for team in self.state.teams.values():
            if robot_id in team.robots:
                return team.robots[robot_id]
        raise ModelError(f"robot desconegut: {robot_id}")

    def render(self) -> pygame.Surface:
        if self.surface is None:
            self.setup()
        self.renderer.draw(self.selection)
        if self.message and self.renderer.font:
            self.surface.blit(self.renderer.font.render(self.message, True, (255, 130, 100)), (12, self.renderer.board_size[1] - 28))
        return self.surface

    def run(self) -> None:
        self.setup()
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_event(event)
            self.render()
            if not self.headless:
                pygame.display.flip()
            clock.tick(30)
        pygame.quit()


def run_pygame(state: GameState, *, headless: bool = False) -> PygameGame:
    """Executa la UI i retorna el controlador (útil per a proves headless)."""
    game = PygameGame(state, headless=headless)
    if not headless:
        game.run()
    else:
        game.render()
    return game
