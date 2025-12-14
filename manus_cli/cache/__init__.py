"""Prompt Caching for Manus CLI v5.2"""
import hashlib
import json
import time
from pathlib import Path
from typing import Optional, Dict, Any

class PromptCache:
    """Caches prompts and responses for performance."""
    
    def __init__(self, cache_dir: Optional[Path] = None, ttl: int = 3600):
        self.cache_dir = cache_dir or Path.home() / ".manus" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl
    
    def _get_cache_key(self, prompt: str, params: Dict[str, Any]) -> str:
        """Generates cache key from prompt and parameters."""
        data = f"{prompt}:{json.dumps(params, sort_keys=True)}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def get(self, prompt: str, params: Dict[str, Any]) -> Optional[str]:
        """Retrieves cached response if available and not expired."""
        key = self._get_cache_key(prompt, params)
        cache_file = self.cache_dir / f"{key}.json"
        
        if not cache_file.exists():
            return None
        
        data = json.loads(cache_file.read_text())
        if time.time() - data["timestamp"] > self.ttl:
            cache_file.unlink()
            return None
        
        return data["response"]
    
    def set(self, prompt: str, params: Dict[str, Any], response: str):
        """Caches response."""
        key = self._get_cache_key(prompt, params)
        cache_file = self.cache_dir / f"{key}.json"
        cache_file.write_text(json.dumps({
            "prompt": prompt,
            "params": params,
            "response": response,
            "timestamp": time.time()
        }))
    
    def clear(self):
        """Clears all cached entries."""
        for file in self.cache_dir.glob("*.json"):
            file.unlink()
