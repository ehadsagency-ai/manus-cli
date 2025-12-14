"""Effort Parameter module for Manus CLI v5.1"""
from enum import Enum
from typing import Optional

class EffortLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class EffortManager:
    """Manages computational effort for API calls."""
    
    EFFORT_CONFIGS = {
        EffortLevel.LOW: {
            "max_tokens": 1000,
            "temperature": 0.7,
            "thinking_budget": 1000,
            "description": "Fast responses, less thorough"
        },
        EffortLevel.MEDIUM: {
            "max_tokens": 2000,
            "temperature": 0.5,
            "thinking_budget": 5000,
            "description": "Balanced speed and quality"
        },
        EffortLevel.HIGH: {
            "max_tokens": 4000,
            "temperature": 0.3,
            "thinking_budget": 10000,
            "description": "Thorough analysis, slower"
        }
    }
    
    def __init__(self, effort: EffortLevel = EffortLevel.MEDIUM):
        self.effort = effort
    
    def get_config(self) -> dict:
        return self.EFFORT_CONFIGS[self.effort]
    
    def apply_to_request(self, request_params: dict) -> dict:
        config = self.get_config()
        request_params.update({
            "max_tokens": config["max_tokens"],
            "temperature": config["temperature"]
        })
        return request_params
