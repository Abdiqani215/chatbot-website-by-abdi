# nlp.py
import spacy
import spacy.cli
from typing import List, Dict, Any
from rapidfuzz import process, fuzz
from datetime import datetime
from config import HOTEL_INFO
# context.py
import os
# Attempt loading spacy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")
# ======================
# Enhanced NLP Utilities
# ======================
class NLPProcessor:
    """
    Advanced NLP processing with entity recognition and canonical synonym expansion.
    """
    def __init__(self):
        # This dictionary maps your *canonical* keyword to a list of 10 or more synonyms.
        # For example, "book" covers synonyms like "reserve", "schedule", "arrange".
        self.canonical_map = {
            
            "book": [
    "book", "reserve", "schedule", "arrange", "prebook", "secure a reservation", "fix a booking", 
    "organize a stay", "make a reservation", "plan my stay", "i qabo qol", "booking", "reserve a room"
],
"room": [
    "room", "suite", "accommodation", "bedroom", "lodging", "quarters", "living space", "chamber", 
    "hotel room", "place to stay", "deluxe", "super deluxe", "triple bed", "double bed", "vip"
],
            "thanks": [
                "thanks",
                "thank you",
                "much obliged",
                "cheers",
                "i appreciate it",
                "gracias",
                "shukran",
                "mahadsanid",
                "waad mahadsantay",
                "ad u mahadsantay",
                "thankful"
            ],
            "greetings": [
                "hello",
                "hi",
                "hey",
                "good morning",
                "good evening",
                "good afternoon",
                "good day",
                "howdy",
                "salaam",
                "hiya",
                "greetings",
                "asc",
                "asalm alaikum"
            ],
            "location": [
                "location",
                "where are you",
                "address",
                "directions",
                "place",
                "position",
                "area",
                "map location",
                "wa xage meeshu",
                "meshu xagay ku taal",
            ]
        }

    def fuzzy_match_token(self, token: str, synonyms: list, threshold=80) -> bool:
        """ Return True if the token closely matches any of the synonyms. """
        best_match, score, index = process.extractOne(token, synonyms, scorer=fuzz.WRatio)
        return score >= threshold

    def expand_to_canonical_fuzzy(self, text: str) -> List[str]:
        tokens = text.lower().split()
        expanded_tokens = []

        for token in tokens:
            matched_canonical = None
            for canonical, synonyms in self.canonical_map.items():
                if self.fuzzy_match_token(token, synonyms):
                    matched_canonical = canonical
                    break
            if matched_canonical:
                expanded_tokens.append(matched_canonical)
            else:
                expanded_tokens.append(token)

        return expanded_tokens

    def expand_synonyms(self, text: str) -> List[str]:
        """
        Convert tokens in 'text' to their canonical form if they match
        any known synonyms in self.canonical_map.
        """
        # Use spaCy to tokenize and normalize to lowercase
        doc = nlp(text.lower())
        expanded_tokens = []

        for token in doc:
            matched_canonical = None
            # Check each canonical keyword and its synonyms
            for canonical, synonyms in self.canonical_map.items():
                if token.text in synonyms:
                    matched_canonical = canonical
                    break

            # If we found a match, use the canonical form; otherwise keep the original token
            if matched_canonical:
                expanded_tokens.append(matched_canonical)
            else:
                expanded_tokens.append(token.text)

        return expanded_tokens

    def extract_entities(self, text: str) -> Dict:
        """
        Extract relevant entities (room types, dates, numbers) using spaCy.
        """
        doc = nlp(text.lower())
        entities = {
            'room_types': [],
            'dates': [],
            'numbers': []
        }

        # spaCy entity recognition for DATE and CARDINAL
        for ent in doc.ents:
            if ent.label_ == 'DATE':
                entities['dates'].append(ent.text)
            elif ent.label_ == 'CARDINAL':
                entities['numbers'].append(ent.text)

        # Check if user mentioned any known hotel room type by name
        room_types = [room["type"].lower() for room in HOTEL_INFO["rooms"]]
        entities['room_types'] = [
            token.text for token in doc 
            if token.text.lower() in room_types
        ]

        return entities
nlp_processor = NLPProcessor()  # Global instance for app.py
