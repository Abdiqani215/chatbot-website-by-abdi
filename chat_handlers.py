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
    Determine and set the user's language preference based on the provided input.

    This function examines the user's message for recognized language identifiers.
    If a valid language is detected (e.g., English or Somali), the user's profile is updated,
    and a corresponding greeting is returned. Otherwise, the user is prompted to select
    a language.

    Args:
        user_id (str): Unique identifier for the user.
        message (str): The raw input message from the user.

    Returns:
        str: A greeting in the selected language or a prompt for language selection.
    """
    profile = context_manager.get_user_profile(user_id)
    msg = message.strip().lower()

    if msg in ['en', 'english', '1']:
        profile.update({'preferred_language': 'en', 'state': 'normal'})
        return random.choice(RESPONSES['en']['greetings'])
    elif msg in ['so', 'somali', 'soomaali', '2']:
        profile.update({'preferred_language': 'so', 'state': 'normal'})
        return random.choice(RESPONSES['so']['greetings'])
    else:
        # If the language cannot be determined, prompt the user with the default language selection message.
        return RESPONSES['en']['language_prompt']


def generate_response(user_id: str, message: str) -> str:
    """
    Generate a context-aware response based on the user's input and profile.

    The function first checks whether the user's language preference has been set.
    If not, it delegates to the language selection handler. Once the language is determined,
    the function employs NLP processing to transform the input message into a set of
    canonical tokens. Depending on these tokens, it selects the most appropriate response:
      - A greeting if the user’s message indicates salutations.
      - Booking guidance if keywords such as "book" or "room" are detected.
      - Location details if the message includes "location".
    For any unrecognized input, a fallback response is generated.

    Args:
        user_id (str): Unique identifier for the user.
        message (str): The user's input message.

    Returns:
        str: A contextually appropriate response.
    """
    profile = context_manager.get_user_profile(user_id)
    
    # Prompt for language selection if the user's preference is not set or they are in a pending state.
    if profile.get('preferred_language') is None or profile.get('state') == 'awaiting_language':
        return handle_language_selection(user_id, message)

    # Retrieve the user's preferred language; default to English if somehow unset.
    lang = profile.get('preferred_language', 'en')

    # Use the NLP processor to convert the input message into a set of canonical tokens.
    expanded_tokens = nlp_processor.expand_to_canonical_fuzzy(message)
    token_set = set(expanded_tokens)

    # If the message contains a greeting, return a greeting response.
    if "greetings" in token_set:
        return random.choice(RESPONSES[lang]["greetings"])

    # If the user's message suggests an inquiry about booking or room details,
    # provide the appropriate booking information.
    if "book" in token_set or "room" in token_set:
        # Placeholder message: In production, replace with detailed booking instructions or redirect.
        return "For room reservations, please visit our online booking portal available on our website."

    # If the message includes an inquiry about location, provide the hotel address.
    if "location" in token_set:
        return f"Jees Hotel is located at {HOTEL_INFO['address']}."

    # For any other inputs, use the fallback mechanism to generate an appropriate response.
    return handle_fallback(user_id, lang)
