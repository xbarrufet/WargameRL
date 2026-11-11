from __future__ import annotations

from io import StringIO

from wargame.console import create_state, default_config_path, execute_command, format_initial, run_demo


def test_demo_is_terminal_and_reports_reason() -> None:
    output = StringIO()
    state = create_state(seed=7)
    run_demo(state, output)
    text = output.getvalue()
    assert "MODE demo" in text
    assert "END_REASON victory_points" in text
    assert "FINAL DRAW" in text


def test_manual_commands_report_help_and_status() -> None:
    state = create_state(seed=7)
    output = StringIO()
    assert execute_command(state, "help", output)
    assert execute_command(state, "status", output)
    assert "move ROBOT Q R ORIENTATION" in output.getvalue()
    assert "phase=MOVEMENT" in output.getvalue()
    assert "team_a_robot_1@(2,0)[team_a]" in output.getvalue()


def test_initial_output_contains_seed_and_configuration() -> None:
    state = create_state(seed=7)
    text = format_initial(state, default_config_path())
    assert "SEED 7" in text
    assert "config/example.yaml" in text
