# handlers.py
from typing import Callable, Optional, List, Dict
import random
from config import HOTEL_INFO, RESPONSES
from nlp import nlp_processor
from context import context_manager

# --------------------------
# Intent Handling Framework
# --------------------------
class IntentHandler:
    """
    Advanced intent handling system with:
    - Context-aware matching
    - Priority-based execution
    - Fallback management
    """
    def __init__(self):
        self.handlers = []
        self.fallback_handler = None

    def register_handler(self, 
                        intents: List[str], 
                        handler: Callable,
                        priority: int = 0,
                        context_requirements: List[str] = None):
        """
        Register a new intent handler with:
        - intents: List of trigger phrases
        - handler: Function to execute
        - priority: Higher executes first
        - context_requirements: Required context keys
        """
        self.handlers.append({
            'patterns': [p.lower().split() for p in intents],
            'handler': handler,
            'priority': priority,
            'context_requirements': context_requirements or []
        })

    def set_fallback(self, handler: Callable):
        """Set fallback handler for unmatched intents"""
        self.fallback_handler = handler

    def match_intent(self, message: str, user_id: str) -> Optional[Callable]:
        """
        Find matching handler using:
        1. Context-aware matching
        2. Priority-based fallback
        3. Token-based pattern matching
        """
        message_tokens = message.lower().split()
        context = context_manager.get_context(user_id)

        # Check context-specific handlers first
        for handler in sorted(self.handlers, key=lambda x: -x['priority']):
            if all(context.get(req) for req in handler['context_requirements']):
                if any(all(p in message_tokens for p in pattern) 
                     for pattern in handler['patterns']):
                    return handler['handler']

        # General intent matching
        for handler in sorted(self.handlers, key=lambda x: -x['priority']):
            if any(all(p in message_tokens for p in pattern) 
                 for pattern in handler['patterns']):
                return handler['handler']

        return self.fallback_handler

import random
from config import HOTEL_INFO, RESPONSES
from context import context_manager
from nlp import nlp_processor
from handlers import IntentHandler  # Ensure this is imported from the correct module

# --------------------------
# Conversation Handlers
# --------------------------

def handle_rooms(message: str, user_id: str, lang: str) -> str:
    """
    Handle room-related queries with context tracking.
    
    This function extracts entities from the user's message and attempts to find
    a matching room from HOTEL_INFO. It updates the user's context and returns either
    detailed room information or a list of available rooms.
    
    Args:
        message (str): The user's input message.
        user_id (str): The unique identifier for the user.
        lang (str): The user's preferred language code.
    
    Returns:
        str: A response with room details or a list of available rooms.
    """
    entities = nlp_processor.extract_entities(message)
    user_context = context_manager.get_context(user_id)
    
    if entities.get('room_types'):
        room_type = entities['room_types'][0].lower()
        try:
            room = next(r for r in HOTEL_INFO["rooms"] if r["type"].lower() == room_type)
        except StopIteration:
            # If no room is found, return a default message with the room list.
            room_list = "\n".join(
                f"- {room['type']} ({room['price']})" for room in HOTEL_INFO["rooms"]
            )
            return RESPONSES[lang].get(
                "room_not_found", 
                "Sorry, we could not find that room. Here are the available options:\n{room_list}"
            ).format(room_list=room_list)
        
        # Update context: log the room viewed and reset fallback attempts.
        context_manager.update_context(user_id, {
            'last_room_viewed': room_type,
            'fallback_attempts': 0
        })
        return RESPONSES[lang]["room_details"].format(**room)
    
    # If no specific room type is mentioned, return a list of available rooms.
    room_list = "\n".join(
        f"- {room['type']} ({room['price']})" for room in HOTEL_INFO["rooms"]
    )
    return RESPONSES[lang]["room_list"].format(room_list=room_list)


def handle_fallback(user_id: str, lang: str) -> str:
    """
    Improved fallback handling to reduce unnecessary live agent escalations.
    """
    user_context = context_manager.get_context(user_id)
    attempts = user_context.get("fallback_attempts", 0) + 1
    context_manager.update_context(user_id, {"fallback_attempts": attempts})

    if attempts == 1:
        return (
            "I'm sorry, I didn't understand that. Could you try rephrasing it?\n\n"
            "Here are some topics I can help with:\n"
            "1️⃣ Room bookings\n\n"
            "2️⃣ Amenities details\n\n"
            "3️⃣ Special offers\n\n"
            "4️⃣ Hotel policies\n\n"
            "Please type a number or ask another question."
        )

    if attempts == 2:
        return (
            "I’m still having trouble understanding. Try asking about room availability, hotel services, or special discounts.\n\n"
            "Would you like to speak to a live agent instead?"
        )

    # Escalate only after 3 failed attempts
    if attempts >= 3:
        return (
            "I'm having trouble understanding. Let me connect you to a live agent. "
            "<a href='https://wa.me/252638533333' target='_blank'>Click here to chat on WhatsApp</a>"
        )

    return random.choice(RESPONSES[lang]["fallback"])

def handle_help(message: str, user_id: str, lang: str) -> str:
    """
    Provide help information to the user.
    
    This function returns a help message detailing what the user can ask or do.
    It can be further enhanced to provide context-aware help.
    
    Args:
        message (str): The user's input message.
        user_id (str): The unique identifier for the user.
        lang (str): The user's preferred language code.
    
    Returns:
        str: A help message.
    """
    help_message = (
        "Here are some things you can ask me:\n"
        "- Ask for details about a room (e.g., 'Tell me about the deluxe room')\n"
        "- Request booking information\n"
        "- Inquire about hotel amenities\n"
        "- Get contact information\n"
        "- Ask for directions or location details"
    )
    return help_message

# --------------------------
# Intent Handler Setup
# --------------------------

# Instantiate the intent handler.
intent_handler = IntentHandler()

# Register core intents.
intent_handler.register_handler(
    intents=["room", "rooms", "accommodation", "suite"],
    handler=handle_rooms,
    priority=2,
    context_requirements=["booking_stage"]  # Adjust or remove based on your context design.
)

intent_handler.register_handler(
    intents=["help", "assist", "confused"],
    handler=handle_help,
    priority=3
)

# Set the fallback handler.
intent_handler.set_fallback(
    lambda msg, uid, lang: handle_fallback(uid, lang)
)
