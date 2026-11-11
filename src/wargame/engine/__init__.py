"""Execució i validació de les accions del joc."""
from .movement import (
    Advance,
    Jump,
    MovementKind,
    MovementResult,
    NormalMovement,
    Pivot,
    accessible_destinations,
    execute_movement,
)
from .turn import EndPhaseAction, execute_end_phase, validate_robot_action
from .combat import ShootAction, CombatResult, execute_shot

__all__ = [
    "Advance",
    "Jump",
    "MovementKind",
    "MovementResult",
    "NormalMovement",
    "Pivot",
    "accessible_destinations",
    "execute_movement",
    "EndPhaseAction",
    "execute_end_phase",
    "validate_robot_action",
    "ShootAction",
    "CombatResult",
    "execute_shot",
]
