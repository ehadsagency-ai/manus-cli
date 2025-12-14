"""
Manus CLI Spec-Kit Integration
Complete GitHub Spec-Kit methodology implementation
"""

__version__ = "4.0.0"
__spec_kit_version__ = "1.0.0"

from .core import SpecKitEngine, should_use_spec_driven, assess_complexity
from .constitution import ConstitutionPhase
from .specify import SpecificationPhase
from .plan import PlanningPhase

__all__ = [
    "SpecKitEngine",
    "should_use_spec_driven",
    "assess_complexity",
    "ConstitutionPhase",
    "SpecificationPhase",
    "PlanningPhase",
]
