"""Output validators."""
from typing import Dict, Any, List
from .schemas import ValidationSchema

class ValidationError(Exception):
    """Raised when validation fails."""
    pass

class OutputValidator:
    """Validates output against schemas."""
    
    def __init__(self, schema: ValidationSchema):
        self.schema = schema
    
    def validate(self, output: Dict[str, Any]) -> List[str]:
        """Validates output and returns list of errors."""
        errors = []
        
        # Check required fields
        for field in self.schema.required_fields:
            if field not in output:
                errors.append(f"Missing required field: {field}")
        
        # Check field types
        for field, expected_type in self.schema.field_types.items():
            if field in output and not isinstance(output[field], expected_type):
                errors.append(f"Field '{field}' has wrong type")
        
        # Run custom validators
        for field, validator in self.schema.custom_validators.items():
            if field in output:
                try:
                    validator(output[field])
                except Exception as e:
                    errors.append(f"Validation failed for '{field}': {str(e)}")
        
        return errors
    
    def validate_or_raise(self, output: Dict[str, Any]):
        """Validates and raises exception if invalid."""
        errors = self.validate(output)
        if errors:
            raise ValidationError("\n".join(errors))
