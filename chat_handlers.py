"""
chat_handlers.py

This module handles language selection and response generation for the Jees Hotel chatbot.
It leverages the global context manager, advanced NLP processing, and predefined response
templates to provide intelligent, context-aware replies for user interactions.
"""

import random
from config import RESPONSES, HOTEL_INFO
from context import context_manager
from nlp import nlp_processor
from handlers import handle_fallback


def handle_language_selection(user_id: str, message: str) -> str:
    """
    Handles user messages and determines the response based on user state.
    """
    profile = context_manager.get_user_profile(user_id)
    
    # Check if the user already has a language set
    if 'preferred_language' not in profile:
        return handle_language_selection(user_id, message)

    language = profile['preferred_language']
    msg = message.strip().lower()

    # Define possible interactions
    if msg in ['room', 'room bookings', '1']:  # Adjust according to your expected inputs
        profile.update({'state': 'booking'})
        return RESPONSES[language]['booking_prompt']

    elif profile.get('state') == 'booking':
        # Handle booking process
        return process_booking(user_id, message)  # Implement this function separately

    return RESPONSES[language]['fallback']  # A generic fallback message
def generate_response(user_id: str, message: str) -> str:
    """
    Generate a context-aware response based on the user's input and profile.
    """

    profile = context_manager.get_user_profile(user_id)
    
    # Prompt for language selection if the user's preference is not set or they are in a pending state.
    if profile.get('preferred_language') is None or profile.get('state') == 'awaiting_language':
        return handle_language_selection(user_id, message)

    # Retrieve the user's preferred language; default to English if somehow unset.
    lang = profile.get('preferred_language', 'en')

    # Use NLP to process the input message.
    expanded_tokens = nlp_processor.expand_to_canonical_fuzzy(message)
    token_set = set(expanded_tokens)
    # Handle greetings
    if "greetings" in token_set:
        return random.choice(RESPONSES[lang]["greetings"])

    # Handle room bookings
    if "book" in token_set or "room" in token_set:
        return (
            "For room reservations, please visit our online booking portal: "
            "<a href='https://live.ipms247.com/booking/book-rooms-jeeshotel' "
        )

    # Handle location inquiries
    if "location" in token_set:
        return f"Jees Hotel is located at {HOTEL_INFO['address']}."

    # Handle live chat
    if "live chat" in message.lower() or "support" in message.lower():
        return (
            "You can talk to a live agent now! "
            "<a href='https://wa.me/2526347470907'>Click here to chat on WhatsApp</a>"
        )

    # For any other inputs, use the fallback mechanism.
    return handle_fallback(user_id, lang)
