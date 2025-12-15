"""
Manus API client for interacting with Manus AI services
"""

import os
import json
import requests
from typing import Optional, Dict, Any, Iterator
from pathlib import Path


class ManusAPIError(Exception):
    """Custom exception for Manus API errors"""
    pass


class ManusClient:
    """Client for interacting with Manus AI API"""
    
    API_URL = "https://api.manus.ai/v1/tasks"
    CONFIG_DIR = Path.home() / ".config" / "manus"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Manus API client
        
        Args:
            api_key: Optional API key. If not provided, will try to load from config or environment
        """
        self.api_key = api_key or self._get_api_key()
        
        if not self.api_key:
            raise ManusAPIError(
                "No API key found. Please set MANUS_API_KEY environment variable "
                "or configure it using 'manus configure'"
            )
    
    def _get_api_key(self) -> Optional[str]:
        """Get API key from config file or environment variable"""
        # First try environment variable
        api_key = os.environ.get("MANUS_API_KEY")
        if api_key:
            return api_key
        
        # Then try config file
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    return config.get("api_key")
            except (json.JSONDecodeError, IOError):
                pass
        
        return None
    
    @classmethod
    def save_api_key(cls, api_key: str) -> None:
        """Save API key to config file"""
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        config = {}
        if cls.CONFIG_FILE.exists():
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        config["api_key"] = api_key
        
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Set restrictive permissions on config file
        cls.CONFIG_FILE.chmod(0o600)
    
    def create_task(
        self, 
        prompt: str, 
        mode: str = "speed",
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new task via Manus API
        
        Args:
            prompt: The prompt/query to send to Manus
            mode: Execution mode (default: "speed")
            stream: Whether to stream the response
            
        Returns:
            Task data from API response
            
        Raises:
            ManusAPIError: If the API request fails
        """
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "API_KEY": self.api_key,
        }
        
        payload = {
            "prompt": prompt,
            "mode": mode
        }
        
        try:
            response = requests.post(
                self.API_URL, 
                headers=headers, 
                json=payload,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                return response
            else:
                return response.json()
                
        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {e}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = f"API error: {error_data.get('message', str(e))}"
                except:
                    error_msg = f"API error (HTTP {e.response.status_code}): {e.response.text}"
            
            raise ManusAPIError(error_msg)
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a task
        
        Args:
            task_id: The ID of the task to check
            
        Returns:
            Task status data
            
        Raises:
            ManusAPIError: If the API request fails
        """
        headers = {
            "accept": "application/json",
            "API_KEY": self.api_key,
        }
        
        try:
            response = requests.get(
                f"{self.API_URL}/{task_id}",
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise ManusAPIError(f"Failed to get task status: {e}")
