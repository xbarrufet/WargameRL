"""Enumeracions del domini de la partida."""

from enum import Enum


class Direction(str, Enum):
    N = "N"
    NE = "NE"
    SE = "SE"
    S = "S"
    SW = "SW"
    NW = "NW"


class Phase(str, Enum):
    MOVEMENT = "MOVEMENT"
    SHOOTING = "SHOOTING"
    SCORING = "SCORING"


class GameResult(str, Enum):
    PENDING = "PENDING"
    TEAM_A_WINS = "TEAM_A_WINS"
    TEAM_B_WINS = "TEAM_B_WINS"
    DRAW = "DRAW"

