# context.py
import os
from typing import Dict, Any
from datetime import datetime

class ContextManager:
    def __init__(self):
        # 'contexts' holds arbitrary context data per user
        self.contexts: Dict[str, Dict[str, Any]] = {}
        # 'user_profiles' holds richer data per user
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
        # 'rate_limits' to avoid spamming
        self.rate_limits: Dict[str, datetime] = {}
    
    def get_context(self, user_id: str) -> Dict[str, Any]:
        return self.contexts.get(user_id, {})
    
    def update_context(self, user_id: str, updates: Dict[str, Any]):
        self.contexts.setdefault(user_id, {}).update(updates)
    
    def clear_context(self, user_id: str):
        self.contexts.pop(user_id, None)
    
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        # Extended profile with additional fields for increased context "density"
        return self.user_profiles.setdefault(user_id, {
            'preferred_language': None,    # e.g., 'en', 'so'
            'state': 'awaiting_language',    # or 'normal', etc.
            'last_interaction': datetime.now(),
            'conversation_history': [],
            'preferred_room_type': None,
            'booking_history': [],
            'message_count': 0,            # Count of messages exchanged
            'fallback_attempts': 0,        # How many times fallback has been used
            'current_topic': None          # Could be used to track conversation topics
        })
    
    def log_interaction(self, user_id: str, message: str, intent: str):
        profile = self.get_user_profile(user_id)
        # Log message details with timestamp
        profile['conversation_history'].append({
            'timestamp': datetime.now(),
            'message': message,
            'intent': intent
        })
        profile['last_interaction'] = datetime.now()
        profile['message_count'] += 1  # Increase message count with every interaction
    
    def check_rate_limit(self, user_id: str) -> bool:
        last_req = self.rate_limits.get(user_id)
        if last_req and (datetime.now() - last_req).seconds < 2:
            return True
        self.rate_limits[user_id] = datetime.now()
        return False

# Create a single global instance to be imported by other modules
context_manager = ContextManager()