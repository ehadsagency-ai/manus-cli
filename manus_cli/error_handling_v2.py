"""Enhanced Error Handling module for Manus CLI v5.0"""
import time
import random
from typing import Callable, Any, Optional
from functools import wraps
from rich.console import Console
from rich.panel import Panel

console = Console()

class APIError(Exception):
    """Base exception for API errors."""
    pass

class RateLimitError(APIError):
    """Raised when rate limit is exceeded."""
    pass

class AuthenticationError(APIError):
    """Raised when authentication fails."""
    pass

class ServerError(APIError):
    """Raised when server returns 5xx error."""
    pass

class RetryStrategy:
    """Implements exponential backoff with jitter."""
    def __init__(self, max_retries=3, base_delay=1.0, max_delay=60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    def get_delay(self, attempt):
        delay = min(self.base_delay * (2 ** attempt), self.max_delay)
        return delay * (0.75 + random.random() * 0.5)
    
    def should_retry(self, error, attempt):
        if attempt >= self.max_retries:
            return False
        return isinstance(error, (RateLimitError, ServerError, ConnectionError))

def with_retry(max_retries=3, base_delay=1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            strategy = RetryStrategy(max_retries=max_retries, base_delay=base_delay)
            last_error = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if not strategy.should_retry(e, attempt):
                        raise
                    delay = strategy.get_delay(attempt)
                    console.print(f"[yellow]Retry {attempt + 1}/{max_retries} after {delay:.1f}s[/yellow]")
                    time.sleep(delay)
            raise last_error
        return wrapper
    return decorator
