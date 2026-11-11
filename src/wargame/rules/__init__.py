"""Regles de moviment, visibilitat, combat i puntuació."""

from .scoring import objective_controller, objective_points_for
from .visibility import (
    ArcRelation,
    VisibilityReason,
    VisibilityResult,
    assess_target,
    classify_arc,
    valid_targets,
)
from .combat import movement_modifier

__all__ = [
    "ArcRelation",
    "VisibilityReason",
    "VisibilityResult",
    "assess_target",
    "classify_arc",
    "objective_points_for",
    "objective_controller",
    "valid_targets",
    "movement_modifier",
]
