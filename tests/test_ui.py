from pathlib import Path

import pytest

pygame = pytest.importorskip("pygame")

from wargame.console import create_state
from wargame.model.coordinates import HexCoordinate
from wargame.ui import PygameGame


ROOT = Path(__file__).parents[1]


def test_headless_ui_renders_configured_game(monkeypatch) -> None:
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    game = PygameGame(create_state(ROOT / "config/example.yaml", seed=3), headless=True)
    surface = game.render()
    assert surface.get_width() > 17 * 20
    assert surface.get_height() > 15 * 20
    pygame.quit()


def test_projection_and_selection_ignore_outside_click(monkeypatch) -> None:
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    game = PygameGame(create_state(seed=3), headless=True)
    game.setup()
    game.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (0, 0)}))
    assert game.selection.cell is None
    assert game.renderer.projection.from_screen((0, 0), 17, 15) is None
    pygame.quit()


def test_clicking_robot_selects_active_robot(monkeypatch) -> None:
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    state = create_state(seed=3)
    game = PygameGame(state, headless=True)
    game.setup()
    center = game.renderer.projection.to_screen(HexCoordinate(2, 0))
    game.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": tuple(round(x) for x in center)}))
    assert game.selection.robot_id == "team_a_robot_1"
    pygame.quit()
