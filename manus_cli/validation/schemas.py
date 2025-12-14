"""Validation schemas for different output types."""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class ValidationSchema:
    """Defines expected output structure."""
    name: str
    required_fields: List[str]
    optional_fields: List[str] = None
    field_types: Dict[str, type] = None
    custom_validators: Dict[str, callable] = None
    
    def __post_init__(self):
        if self.optional_fields is None:
            self.optional_fields = []
        if self.field_types is None:
            self.field_types = {}
        if self.custom_validators is None:
            self.custom_validators = {}

# Common schemas
CODE_SCHEMA = ValidationSchema(
    name="code",
    required_fields=["language", "code"],
    optional_fields=["explanation", "tests"],
    field_types={"language": str, "code": str}
)

SPEC_SCHEMA = ValidationSchema(
    name="specification",
    required_fields=["feature_name", "requirements"],
    optional_fields=["assumptions", "constraints"],
    field_types={"feature_name": str, "requirements": list}
)
