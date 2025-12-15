"""
Session management for Manus CLI
Ensures CLI and Web sessions are completely separate
"""

import uuid
import json
from pathlib import Path
from datetime import datetime
from typing import Optional


class SessionManager:
    """Manages CLI session IDs to separate from Web interface"""
    
    SESSION_FILE = Path.home() / ".config" / "manus" / "cli_session.json"
    
    def __init__(self):
        """Initialize session manager"""
        self.SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    def get_or_create_session(self) -> str:
        """
        Get existing session ID or create a new one.
        
        Sessions are persistent across CLI invocations to maintain conversation context,
        but are completely separate from Web interface sessions.
        
        Returns:
            Session ID string
        """
        # Try to load existing session
        if self.SESSION_FILE.exists():
            try:
                with open(self.SESSION_FILE, "r") as f:
                    data = json.load(f)
                    session_id = data.get("session_id")
                    created_at = data.get("created_at")
                    
                    # Return existing session if found
                    if session_id:
                        return session_id
            except (json.JSONDecodeError, KeyError):
                pass
        
        # Create new session
        session_id = self._generate_session_id()
        self._save_session(session_id)
        return session_id
    
    def create_new_session(self) -> str:
        """
        Force create a new session (useful for 'manus chat --new-session')
        
        Returns:
            New session ID
        """
        session_id = self._generate_session_id()
        self._save_session(session_id)
        return session_id
    
    def get_current_session(self) -> Optional[str]:
        """
        Get current session ID without creating a new one.
        
        Returns:
            Session ID or None if no session exists
        """
        if not self.SESSION_FILE.exists():
            return None
        
        try:
            with open(self.SESSION_FILE, "r") as f:
                data = json.load(f)
                return data.get("session_id")
        except (json.JSONDecodeError, KeyError):
            return None
    
    def clear_session(self):
        """Clear current session"""
        if self.SESSION_FILE.exists():
            self.SESSION_FILE.unlink()
    
    def _generate_session_id(self) -> str:
        """
        Generate a unique CLI session ID.
        
        Format: cli-YYYYMMDD_HHMMSS-{random}
        
        Returns:
            Session ID string
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_part = uuid.uuid4().hex[:8]
        return f"cli-{timestamp}-{random_part}"
    
    def _save_session(self, session_id: str):
        """
        Save session to file.
        
        Args:
            session_id: Session ID to save
        """
        data = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "source": "cli"
        }
        
        with open(self.SESSION_FILE, "w") as f:
            json.dump(data, f, indent=2)
    
    def get_session_info(self) -> Optional[dict]:
        """
        Get session information.
        
        Returns:
            Dictionary with session info or None
        """
        if not self.SESSION_FILE.exists():
            return None
        
        try:
            with open(self.SESSION_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, KeyError):
            return None


# Global session manager instance
session_manager = SessionManager()


# Convenience functions
def get_cli_session_id() -> str:
    """Get or create CLI session ID"""
    return session_manager.get_or_create_session()


def new_cli_session() -> str:
    """Create a new CLI session"""
    return session_manager.create_new_session()


def clear_cli_session():
    """Clear current CLI session"""
    session_manager.clear_session()


# Example usage
if __name__ == "__main__":
    # Test session management
    print("Current session:", session_manager.get_current_session())
    print("Get or create session:", session_manager.get_or_create_session())
    print("Session info:", session_manager.get_session_info())
    print("Create new session:", session_manager.create_new_session())
    print("Clear session...")
    session_manager.clear_session()
    print("Current session after clear:", session_manager.get_current_session())
