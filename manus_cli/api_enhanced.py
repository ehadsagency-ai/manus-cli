"""
Enhanced Manus API client with streaming, error handling, and retry logic
"""

import os
import json
import time
import requests
from typing import Optional, Dict, Any, Iterator, Callable
from pathlib import Path


class ManusAPIError(Exception):
    """Custom exception for Manus API errors"""
    pass


class RateLimitError(ManusAPIError):
    """Raised when rate limit is exceeded"""
    pass


class ManusClient:
    """Enhanced client for interacting with Manus AI API"""
    
    API_URL = "https://api.manus.ai/v1/tasks"
    CONFIG_DIR = Path.home() / ".config" / "manus"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    HISTORY_DIR = CONFIG_DIR / "history"
    
    def __init__(self, api_key: Optional[str] = None, session_id: Optional[str] = None):
        """
        Initialize the Manus API client
        
        Args:
            api_key: Optional API key. If not provided, will try to load from config or environment
            session_id: Optional session ID to separate CLI from Web sessions
        """
        self.api_key = api_key or self._get_api_key()
        
        if not self.api_key:
            raise ManusAPIError(
                "No API key found. Please set MANUS_API_KEY environment variable "
                "or configure it using 'manus configure'"
            )
        
        # Generate or use provided session ID
        if session_id:
            self.session_id = session_id
        else:
            import uuid
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.session_id = f"cli-{timestamp}-{uuid.uuid4().hex[:8]}"
        
        # Ensure history directory exists
        self.HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    
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
    def save_config(cls, config: Dict[str, Any]) -> None:
        """Save complete configuration to file"""
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Set restrictive permissions on config file
        cls.CONFIG_FILE.chmod(0o600)
    
    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        """Load configuration from file"""
        if cls.CONFIG_FILE.exists():
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        return {}
    
    @classmethod
    def save_api_key(cls, api_key: str) -> None:
        """Save API key to config file"""
        config = cls.load_config()
        config["api_key"] = api_key
        cls.save_config(config)
    
    def _retry_with_backoff(
        self,
        func: Callable,
        max_retries: int = 3,
        initial_delay: float = 1.0,
        backoff_factor: float = 2.0
    ) -> Any:
        """
        Retry a function with exponential backoff
        
        Args:
            func: Function to retry
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay in seconds
            backoff_factor: Multiplier for delay after each retry
            
        Returns:
            Result from successful function call
            
        Raises:
            ManusAPIError: If all retries fail
        """
        delay = initial_delay
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return func()
            except RateLimitError as e:
                last_exception = e
                if attempt < max_retries:
                    time.sleep(delay)
                    delay *= backoff_factor
                else:
                    raise
            except requests.exceptions.RequestException as e:
                last_exception = e
                if attempt < max_retries:
                    time.sleep(delay)
                    delay *= backoff_factor
                else:
                    raise ManusAPIError(f"Request failed after {max_retries} retries: {e}")
        
        raise last_exception
    
    def create_task(
        self, 
        prompt: str, 
        mode: str = "speed",
        system_prompt: Optional[str] = None,
        stream: bool = False,
        retry: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new task via Manus API
        
        Args:
            prompt: The prompt/query to send to Manus
            mode: Execution mode (default: "speed")
            system_prompt: Optional system prompt to set role/behavior
            stream: Whether to stream the response
            retry: Whether to retry on failure
            
        Returns:
            Task data from API response or response object if streaming
            
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
            "mode": mode,
            "session_id": self.session_id  # Add session ID to separate CLI from Web
        }
        
        # Add system prompt if provided
        if system_prompt:
            payload["system_prompt"] = system_prompt
        
        def make_request():
            response = requests.post(
                self.API_URL, 
                headers=headers, 
                json=payload,
                stream=stream,
                timeout=30
            )
            
            # Check for rate limiting
            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded. Please try again later.")
            
            response.raise_for_status()
            
            if stream:
                return response
            else:
                return response.json()
        
        try:
            if retry:
                return self._retry_with_backoff(make_request)
            else:
                return make_request()
                
        except RateLimitError:
            raise
        except requests.exceptions.Timeout:
            raise ManusAPIError("Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            raise ManusAPIError("Connection error. Please check your internet connection.")
        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {e}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = f"API error: {error_data.get('message', str(e))}"
                except:
                    error_msg = f"API error (HTTP {e.response.status_code}): {e.response.text}"
            
            raise ManusAPIError(error_msg)
    
    def stream_task(
        self,
        prompt: str,
        mode: str = "speed",
        system_prompt: Optional[str] = None
    ) -> Iterator[str]:
        """
        Stream task responses chunk by chunk
        
        Args:
            prompt: The prompt/query to send to Manus
            mode: Execution mode
            system_prompt: Optional system prompt
            
        Yields:
            Response chunks as they arrive
            
        Raises:
            ManusAPIError: If the API request fails
        """
        response = self.create_task(
            prompt=prompt,
            mode=mode,
            system_prompt=system_prompt,
            stream=True,
            retry=False
        )
        
        try:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    # Handle server-sent events format
                    if decoded_line.startswith('data: '):
                        data = decoded_line[6:]  # Remove 'data: ' prefix
                        if data.strip() == '[DONE]':
                            break
                        try:
                            chunk = json.loads(data)
                            if 'content' in chunk:
                                yield chunk['content']
                        except json.JSONDecodeError:
                            # If not JSON, yield the raw data
                            yield data
        finally:
            response.close()
    
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
        
        def make_request():
            response = requests.get(
                f"{self.API_URL}/{task_id}",
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        
        try:
            return self._retry_with_backoff(make_request)
        except requests.exceptions.RequestException as e:
            raise ManusAPIError(f"Failed to get task status: {e}")
    
    def save_conversation(self, conversation_id: str, messages: list) -> None:
        """Save conversation history to file"""
        history_file = self.HISTORY_DIR / f"{conversation_id}.json"
        
        with open(history_file, 'w') as f:
            json.dump({
                "id": conversation_id,
                "messages": messages,
                "timestamp": time.time()
            }, f, indent=2)
    
    def load_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Load conversation history from file"""
        history_file = self.HISTORY_DIR / f"{conversation_id}.json"
        
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        
        return None
    
    def list_conversations(self) -> list:
        """List all saved conversations"""
        conversations = []
        
        for file in self.HISTORY_DIR.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    conversations.append({
                        "id": data.get("id"),
                        "timestamp": data.get("timestamp"),
                        "message_count": len(data.get("messages", []))
                    })
            except (json.JSONDecodeError, IOError):
                pass
        
        # Sort by timestamp, newest first
        conversations.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        
        return conversations

    def chat(
        self,
        prompt: str,
        mode: str = "speed",
        system_prompt: Optional[str] = None,
        poll_interval: float = 2.0,
        max_wait: int = 300
    ) -> str:
        """
        Send a chat message and wait for the response (synchronous).
        
        This method creates a task and polls until completion.
        
        Args:
            prompt: The message to send
            mode: Execution mode (speed/balanced/quality)
            system_prompt: Optional system prompt
            poll_interval: Seconds between status checks
            max_wait: Maximum seconds to wait for completion
            
        Returns:
            The response text
            
        Raises:
            ManusAPIError: If the request fails or times out
        """
        # Create the task
        task_data = self.create_task(
            prompt=prompt,
            mode=mode,
            system_prompt=system_prompt,
            stream=False
        )
        
        task_id = task_data.get("task_id")
        if not task_id:
            raise ManusAPIError("No task_id in response")
        
        # Poll for completion
        elapsed = 0
        while elapsed < max_wait:
            status_data = self.get_task_status(task_id)
            
            # Check status
            status = status_data.get("status")
            
            if status == "completed":
                # Extract result from output array
                output_array = status_data.get("output", [])
                
                # Find the last assistant message with content
                for item in reversed(output_array):
                    if item.get("role") == "assistant" and "content" in item:
                        content = item.get("content", [])
                        if content and len(content) > 0:
                            text = content[0].get("text", "")
                            if text:
                                return text
                
                # Fallback: return empty if no content found
                return ""
            
            elif status == "failed":
                error = status_data.get("error", "Unknown error")
                raise ManusAPIError(f"Task failed: {error}")
            
            elif status in ["pending", "running"]:
                # Still processing, wait and retry
                time.sleep(poll_interval)
                elapsed += poll_interval
            
            else:
                # Unknown status
                raise ManusAPIError(f"Unknown task status: {status}")
        
        raise ManusAPIError(f"Task timed out after {max_wait} seconds")
