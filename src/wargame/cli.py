"""Punt d'entrada de consola del projecte."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .console import create_state, default_config_path, format_initial, run_demo, run_manual


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador WargameRL")
    parser.add_argument(
        "--version",
        action="version",
        version=f"wargame-rl {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command")
    simulate = subparsers.add_parser("simulate", help="executa una partida per consola")
    simulate.add_argument("--config", type=Path, default=None)
    simulate.add_argument("--seed", type=int, default=None)
    simulate.add_argument("--mode", choices=("demo", "manual"), default="demo")
    play = subparsers.add_parser("play", help="juga una partida amb Pygame")
    play.add_argument("--config", type=Path, default=None)
    play.add_argument("--seed", type=int, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "play":
        try:
            from .ui import run_pygame

            run_pygame(create_state(args.config or default_config_path(), args.seed))
        except (OSError, ValueError) as error:
            print(f"ERROR {error}", file=sys.stderr)
            return 1
        return 0
    if args.command != "simulate":
        return 0
    config_path = args.config or default_config_path()
    try:
        state = create_state(config_path, args.seed)
        print(format_initial(state, config_path))
        if args.mode == "demo":
            run_demo(state, sys.stdout)
        else:
            run_manual(state, sys.stdin, sys.stdout)
    except (OSError, ValueError) as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
