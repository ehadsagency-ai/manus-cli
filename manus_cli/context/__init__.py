"""Multi-turn Conversation Context for Manus CLI v5.2"""
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Message:
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class ConversationContext:
    """Manages multi-turn conversation context."""
    
    def __init__(self, session_id: Optional[str] = None, max_messages: int = 20):
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.max_messages = max_messages
        self.messages: List[Message] = []
        self.context_dir = Path.home() / ".manus" / "conversations"
        self.context_dir.mkdir(parents=True, exist_ok=True)
    
    def add_message(self, role: str, content: str):
        """Adds a message to the conversation."""
        self.messages.append(Message(role=role, content=content))
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
        self.save()
    
    def get_context(self) -> List[Dict[str, str]]:
        """Returns conversation context for API calls."""
        return [{"role": msg.role, "content": msg.content} for msg in self.messages]
    
    def save(self):
        """Saves conversation to disk."""
        file_path = self.context_dir / f"{self.session_id}.json"
        file_path.write_text(json.dumps([asdict(msg) for msg in self.messages], indent=2))
    
    def load(self, session_id: str):
        """Loads conversation from disk."""
        file_path = self.context_dir / f"{session_id}.json"
        if file_path.exists():
            data = json.loads(file_path.read_text())
            self.messages = [Message(**msg) for msg in data]
            self.session_id = session_id
    
    def list_sessions(self) -> List[str]:
        """Lists all saved conversation sessions."""
        return [f.stem for f in self.context_dir.glob("*.json")]
    
    def clear(self):
        """Clears current conversation."""
        self.messages = []
        self.save()
