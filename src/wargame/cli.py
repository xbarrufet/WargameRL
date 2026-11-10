"""Punt d'entrada de consola del projecte."""

from __future__ import annotations

import argparse

from . import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simulador WargameRL")
    parser.add_argument(
        "--version",
        action="version",
        version=f"wargame-rl {__version__}",
    )
    return parser


def main() -> int:
    build_parser().parse_args()
    print("WargameRL: motor pendent d'implementar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
