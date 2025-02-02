from typing import Dict, List, Tuple, Callable, Optional
from flask import Flask, request, jsonify
import random
import spacy
import requests
from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime
import spacy.cli

app = Flask(__name__)

# Ensure the spaCy model is downloaded and loaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading language model for the first time...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

#hupshup_api_key
GUPSHUP_API_KEY = "odv18op3iqkeo4r6a4ntr3z176bvc4y3"
GUPSHUP_WHATSAPP_NUMBER = "+252634747907"

# ====================
# Enhanced Core System
# ====================
class ContextManager:
    """Advanced context management with user profiling"""
    def __init__(self):
        self.contexts: Dict[str, Dict] = {}
        self.user_profiles: Dict[str, Dict] = {}
        self.rate_limits: Dict[str, datetime] = {}

    def get_context(self, user_id: str) -> Dict:
        return self.contexts.get(user_id, {})
    
    def update_context(self, user_id: str, updates: Dict):
        self.contexts.setdefault(user_id, {}).update(updates)
    
    def clear_context(self, user_id: str):
        self.contexts.pop(user_id, None)
    
    def get_user_profile(self, user_id: str) -> Dict:
        return self.user_profiles.setdefault(user_id, {
            'preferred_language': 'en',
            'last_interaction': datetime.now(),
            'conversation_history': [],
            'preferred_room_type': None,
            'booking_history': []
        })
    
    def log_interaction(self, user_id: str, message: str, intent: str):
        profile = self.get_user_profile(user_id)
        profile['conversation_history'].append({
            'timestamp': datetime.now(),
            'message': message,
            'intent': intent
        })
        profile['last_interaction'] = datetime.now()
    
    def check_rate_limit(self, user_id: str) -> bool:
        last_req = self.rate_limits.get(user_id)
        if last_req and (datetime.now() - last_req).seconds < 2:
            return True
        self.rate_limits[user_id] = datetime.now()
        return False

context_manager = ContextManager()

# ======================
# Enhanced NLP Utilities
# ======================

class NLPProcessor:
    """Advanced NLP processing with entity recognition"""
    def __init__(self):
        self.synonyms = {
            'book': ['reserve', 'schedule', 'arrange'],
            'room': ['suite', 'accommodation', 'bedroom'],
            'thanks': ['mahadsanid', 'shukran']
        }
    
    def expand_synonyms(self, tokens: list) -> list:
        expanded = []
        for token in tokens:
            expanded.extend(self.synonyms.get(token, [token]))
        return list(set(expanded))
    
    def extract_entities(self, text: str) -> Dict:
        doc = nlp(text.lower())
        entities = {
            'room_types': [],
            'dates': [],
            'numbers': []
        }
        
        for ent in doc.ents:
            if ent.label_ == 'DATE':
                entities['dates'].append(ent.text)
            elif ent.label_ == 'CARDINAL':
                entities['numbers'].append(ent.text)
        
        room_types = [room["type"].lower() for room in HOTEL_INFO["rooms"]]
        entities['room_types'] = [token.text for token in doc if token.text.lower() in room_types]
        
        return entities

nlp_processor = NLPProcessor()

# ======================
# Enhanced Intent System
# ======================

class IntentHandler:
    """Priority-based intent matching with context awareness"""
    def __init__(self):
        self.handlers = []
        self.fallback_handler = None
    
    def register_handler(self, intents: list, handler: Callable, 
                       priority: int = 0, context_requirements: list = None):
        self.handlers.append({
            'patterns': [p.lower().split() for p in intents],
            'handler': handler,
            'priority': priority,
            'context_requirements': context_requirements or []
        })
    
    def set_fallback(self, handler: Callable):
        self.fallback_handler = handler
    
    def match_intent(self, message: str, user_id: str) -> Optional[Callable]:
        message_tokens = message.lower().split()
        context = context_manager.get_context(user_id)
        
        # Check context-aware handlers first
        for handler in sorted(self.handlers, key=lambda x: -x['priority']):
            if all(context.get(req) for req in handler['context_requirements']):
                if any(all(p in message_tokens for p in pattern) 
                      for pattern in handler['patterns']):
                    return handler['handler']
        
        # Check general matches
        for handler in sorted(self.handlers, key=lambda x: -x['priority']):
            if any(all(p in message_tokens for p in pattern) 
                  for pattern in handler['patterns']):
                return handler['handler']
        
        return self.fallback_handler
# ==================
# Hotel Configuration
# ==================

HOTEL_INFO = {
    "name": "Jees Hotel",
    "address": "Sha'ab Area, Hargeisa, Somaliland",
    "phone": "+252 63 8533333",
    "email": "info@jeeshotel.com",
    "whatsapp": "https://wa.me/252638533333",
    "rooms": [
        {"type": "Deluxe Room", "price": "$49/night", "size": "24.20 m²", "beds": 1, "bathrooms": 1},
        {"type": "Super Deluxe Room", "price": "$59/night", "size": "26.30 m²", "beds": 1, "bathrooms": 1},
        {"type": "Twin/Double Room", "price": "$79/night", "size": "26.30 m²", "beds": 2, "bathrooms": 1},
        {"type": "Triple Room", "price": "$105/night", "size": "50 m²", "beds": 3, "bathrooms": 1},
        {"type": "VIP/Suite Room", "price": "$83/night", "size": "50 m²", "beds": 1, "bathrooms": 1}
    ],
    "amenities": [
        "Complimentary Wi-Fi",
        "Free Parking",
        "Fitness Center",
        "Rooftop Restaurant",
        "Complimentary Airport Transfer",
        "Laundry Service",
        "On-site ATMs"
    ],
    "check_in": "1:00 PM",
    "check_out": "12:00 PM",
    "special_offers": [
        "Free airport transfer for ALL rooms."
    ],
    "policies": [
        "Pets are not allowed."
    ]
}

RESPONSES = {
    "en": {
        "greetings": [
            "Hello! Welcome to Jees Hotel. How can I assist you today?",
            "Hi there! How may I help you with your stay at Jees Hotel?",
            "Greetings! What can I do for you today?"
        ],
        "farewells": [
            "Thank you for chatting with us! Have a great day!",
            "We're here if you need anything else. Have a wonderful day!",
            "It was a pleasure assisting you. See you soon!"
        ],
        "fallback": [
            "I'm sorry, I didn't understand that. Could you please rephrase or choose from the following options?\n\n"
            "1️⃣ Room bookings\n2️⃣ Amenities info\n3️⃣ Special offers\n4️⃣ Hotel policies\n\n"
            "Or chat with a live agent: {whatsapp}",
            "I'm here to help with questions about:\n• Room availability\n• Check-in times\n• Special packages\n• Payment methods\n\n"
            "You can also contact us directly: {phone}"
        ],
        "room_list": "Here are our room options:\n{room_list}\n\nWould you like more details about any specific room type?",
        "room_details": (
            "Here are the details for the {room_type}:\n"
            "- Price: {price}\n"
            "- Size: {size}\n"
            "- Beds: {beds}\n"
            "- Bathrooms: {bathrooms}\n\n"
            "If you want to book this room, please visit our booking website: [👉 Book Here](https://live.ipms247.com/booking/book-rooms-jeeshotel)."
        ),
        "amenities": "We offer the following amenities:\n{amenities}\n\nIs there anything specific you'd like to know more about?",
        "check_times": "Our check-in time is {check_in} and check-out is {check_out}.\nWould you like assistance with your booking schedule or any other details?",
        "contact": "You can reach us at:\n📞 Call: {phone}\n📧 Email: {email}\n💬 WhatsApp: {whatsapp}\n\nWe are available 24/7 to assist you.",
        "address": "We are located at {address}.\nWould you like directions or transportation information?",
        "whatsapp": {
            "message": "Click the WhatsApp icon below to chat with us directly!",
            "whatsapp_url": "{whatsapp}",
            "icon_suggestion": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
        },
        "booking": "We no longer take bookings via chatbot. Please book your room online: [👉 Book Now](https://live.ipms247.com/booking/book-rooms-jeeshotel).",
        "special_offers": "We currently have the following special offers:\n{offers}\n\nWould you like to take advantage of any of these?",
        "policies": "Here are our hotel policies:\n{policies}\n\nDo you have any questions or need further clarification on these?",
        "feedback": "Thank you for chatting with us! How would you rate your experience today on a scale of 1-5?",
        "thank_you": "Thank you for your feedback! We look forward to welcoming you again.",
        "language_prompt": "🌍 *Please select your language:*\n\n"
                           "--------------------\n"
                           "1️⃣ *English 🇬🇧*\n"
                           "2️⃣ *Somali 🇸🇴*\n"
                           "--------------------\n"
                           "👉 Type '1' for English or '2' for Somali.",
        "booking_date_prompt": "Bookings cannot be made via chatbot. Please visit our website: [👉 Book Here](https://live.ipms247.com/booking/book-rooms-jeeshotel).",
        "booking_confirm": "Our chatbot does not handle bookings. Please visit our website for reservations: [👉 Click Here](https://live.ipms247.com/booking/book-rooms-jeeshotel).",
        "booking_success": "Bookings can only be made through our official website: [👉 Visit Here](https://live.ipms247.com/booking/book-rooms-jeeshotel).",
        "booking_cancel": "Booking changes cannot be handled via chatbot. Please contact the hotel management for assistance.",
        "room_selection_retry": "Please select a valid room type from the list.",
        "thanks": "You're welcome! Is there anything else I can assist you with?",
        "more_info": "Could you please provide more details or clarify your request?",
        "general": "I'm here to help with any questions you have about our hotel services. Feel free to ask!",
        "promotion": "Don't miss our exclusive deals and seasonal promotions! Check out our website for more details.",
        "reservation_status": "If you have a reservation and need to check its status, please contact the hotel management directly."
    },

    "so": {
    "greetings": [
        "Asalaamu calaykum! Ku soo dhawoow Jees Hotel. Sideen kuu caawin karnaa maanta?",
        "Asalaamu calaykum! Ku soo dhawoow Jees Hotel. Maxaan kuu qabaa?",
        "Salaan diiran! Ma u baahan tahay caawimaad ku saabsan adeegyada Jees Hotel?"
    ],
    "farewells": [
        "Mahadsanid inaad nala soo xiriirtay. Maalin wanaagsan!",
        "Haddii aad wax su'aalo ah qabto, waxaan joognaa 24/7. Maalin wanaagsan!",
        "Waxaan ku faraxsanahay inaan kaa caawinay. Nabad gelyo! Waxaan rajaynaynaa inaan kugu aragno mar kale."
    ],
    "fallback": [
        "Waan ka xumahay, ma fahmin su'aashaada. Fadlan isku day mar kale ama dooro mid ka mid ah xulashooyinkan:\n\n"
        "1️⃣ Qolalka\n2️⃣ Adeegyada\n3️⃣ Dalacsiinta\n4️⃣ Qaanuunnada hotelka\n\n"
        "Ama si toos ah ula xiriir shaqaalaha: {whatsapp}",
        "Waxaan kaa caawin karaa su'aalaha ku saabsan:\n• Qolalka la heli karo\n• Waqtiga check-in\n• Xawaariiq gaar ah\n• Hababka lacag bixinta\n\n"
        "Waxaad sidoo kale nagala soo xiriiri kartaa: {phone}"
    ],
    "room_list": "Kuwani waa qolalka aanu bixino:\n{room_list}\n\nMa rabtaa faahfaahin dheeraad ah oo ku saabsan qol gaar ah?",
    "room_details": (
        "Waa kuwan faahfaahinta qolka {room_type}:\n"
        "- Qiimaha: {price}\n"
        "- Cabbirka: {size}\n"
        "- Sariiro: {beds}\n"
        "- Musqul: {bathrooms}\n\n"
        "Ma rabtaa inaan kuu qabto qolkan, mise su'aalo kale ayaad qabtaa?"
    ),
    "amenities": "Waxaan bixinaa adeegyada soo socda:\n{amenities}\n\nMa jirtaa wax gaar ah oo aad rabto inaad wax badan ka ogaato?",
    "check_times": "Waqtiga check-in waa {check_in} iyo check-out waa {check_out}.\nMa u baahan tahay caawimaad ku saabsan jadwalka buugista ama faahfaahin kale?",
    "contact": "Waxaad nagala soo xiriiri kartaa:\n📞 Wac: {phone}\n📧 Iimeyl: {email}\n💬 WhatsApp: {whatsapp}\n\nWaxaan nahay 24/7 si aan kuu caawinno.",
    "address": "Waxaan ku yaallaa {address}.\nMa u baahan tahay tilmaamo ama macluumaad gaadiid?",
    "whatsapp": {
        "message": "Guji sumadda WhatsApp ee hoose si aad si toos ah nala ula xiriirto!",
        "whatsapp_url": "{whatsapp}",
        "icon_suggestion": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
    },
    "wifi": "Haa, waxaan bixinaa internet xawaare sare leh (200 Mbps). Wi-Fi-gu waa bilaash!",
    "laundry": "Haa, waxaan bixinaa adeeg dhar dhaqis, laakiin qiimaha wuu kala duwan yahay iyadoo ku xiran dharka aad rabto in la dhaqo.",
    "family": "Waxaan nahay hotel ku habboon qoysaska, laakiin kama bixino sariiraha ilmaha ama sariiro dheeraad ah. Hase yeeshee, waxaad ka heli kartaa qolalka qoyska boggayaga.",
    "gym": "Haa, jimicsigayagu waa furan yahay, waana xor loogu isticmaali karaa martida hotelka.",
    "restaurant": "Waxaan haynaa hal maqaaxi oo leh 7 meelood oo kala duwan oo fadhiga, sida dhismaha sare (rooftop), kafateeriyada, hoolka iyo maqaaxida caadiga ah.",
    "taxi": "Haa, waxaan kuu dalban karnaa taksi, balse waa adeeg lacag leh.",
    "airport": "Haa, waxaan bixinaa gaadiid bilaash ah oo lagaa soo qaado garoonka diyaaradaha.",
    "rooms": "Waxaad ka heli kartaa qolalka kala duwan ee aan bixino halkan: [Book Now](https://live.ipms247.com/booking/book-rooms-jeeshotel)",
    "booking": "Haddii aad rabto inaad buug sameyso, fadlan booqo boggayaga: [Book Now](https://live.ipms247.com/booking/book-rooms-jeeshotel)",
    "policies": "Kuwani waa qaanuunnada hotelka:\n{policies}\n\nMa jirtaa wax su'aalo ah oo aad qabto ku saabsan?",
    "special_offers": "Waxaan haynaa dalacsiimo gaar ah:\n{offers}\n\nMa rabtaa inaad ka faa'iideysato mid ka mid ah?",
    "feedback": "Mahadsanid inaad nala soo xiriirtay! Sidee ayaad u qiimeyn lahayd adeeggeena maanta? (1-5)",
    "thank_you": "Waad ku mahadsan tahay jawaabtaada! Waxaan rajaynaynaa inaan mar kale ku aragno.",
    "language_prompt": (
        "🌍 *Fadlan dooro luqadda:* / *Please select your language:*\n\n"
        "--------------------\n"
        "1️⃣ *English 🇬🇧*\n"
        "2️⃣ *Soomaali 🇸🇴*\n"
        "--------------------\n"
        "👉 *Qor '1' si aad u doorato Ingiriis, ama '2' si aad u doorato Soomaali.*\n"
        "👉 *Type '1' for English or '2' for Somali.*"
    ),
    "booking": "Haddii aad rabto inaad qol qabsato , fadlan isticmaal: [👉 Halkan qol ka qabso ](https://live.ipms247.com/booking/book-rooms-jeeshotel)",
    "booking_confirm": "qol hadad rabto inad qabsato halkan taabo. [👉 Guji halkan](https://live.ipms247.com/booking/book-rooms-jeeshotel)",
    "booking_success": "qol qabsasho waxa lagaa qabsan karaa kaliya halkan: [👉 taabo halkan](https://live.ipms247.com/booking/book-rooms-jeeshotel)",
    "booking_cancel": "booking si toos ah loogama joojin karo chatbot-ka. Haddii aad rabto inaad wax ka bedesho ama cancel to, fadlan la xiriir maamulka hotelka.",
    "room_selection_retry": "Fadlan dooro nooc qol oo sax ah oo ka mid ah liiska.",
    "thanks": "Adigaa mudan! Ma jirtaa wax kale oo aan ku caawin karo?",
    "more_info": "Fadlan faahfaahin dheeraad ah bixiso si aan u fahamno baahidaada.",
    "general": "Waxaan kuu joognaa inaan kaa caawino su'aalaha ku saabsan adeegyada hotelka. Naweydii wixii aad qabto!",
    "promotion": "la xiriir mamulka hotelka Wac: {phone}\n📧 gmail: {email}\n💬 WhatsApp: {whatsapp}",
    "reservation_status": "Haddii aad hore u qabsatay qol oo aad rabto inaad xaqiijiso, fadlan Wac: {phone}\n📧 gmail: {email}\n💬 WhatsApp: {whatsapp}."
    }
}

# ==================
# Enhanced Handlers
# ==================

def handle_rooms(msg: str, uid: str, lang: str) -> str:
    entities = nlp_processor.extract_entities(msg)
    
    if entities['room_types']:
        room_type = entities['room_types'][0]
        room = next(r for r in HOTEL_INFO["rooms"] if r["type"].lower() == room_type.lower())
        context_manager.update_context(uid, {'last_room_viewed': room_type})
        return RESPONSES[lang]["room_details"].format(**room)
    
    room_list = "\n".join([f"- {room['type']} ({room['price']})" for room in HOTEL_INFO["rooms"]])
    return RESPONSES[lang]["room_list"].format(room_list=room_list)

def handle_fallback(lang: str) -> str:
    user_attempts = context_manager.get_context(lang).get("fallback_attempts", 0)

    if user_attempts >= 2:
        return f"Let me connect you to a live agent. Click here: {HOTEL_INFO['whatsapp']}"

    context_manager.update_context(lang, {"fallback_attempts": user_attempts + 1})
    return random.choice(RESPONSES[lang]["fallback"]).format(**HOTEL_INFO)

# =====================
# Enhanced Chat Flow
# =====================

@app.route('/')
def home():
    return "Welcome to Jees Hotel Chatbot! Use /chatbot at the end of the url to start chatting"

@app.route('/api', methods=['POST'])
def api_handler():
    try:
        data = request.get_json()
        action = data.get("action")

        if action == "chat":
            user_id = request.remote_addr
            if context_manager.check_rate_limit(user_id):
                return jsonify({"response": "Please wait a moment before sending another message."})
            if not data or 'message' not in data:
                return jsonify({"error": "Invalid request"}), 400
            response = generate_response(user_id, data['message'])
            return jsonify({"response": response})
        else:
            return jsonify({"error": "Invalid action"}), 400

    except Exception as e:
        app.logger.error(f"API error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/chatbot', methods=['GET'])
def chatbot_interface():
    """
    A more professional and modern Chatbot Web Interface for Jees Hotel.
    """
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Jees Hotel Chat</title>
      <!-- Google Fonts -->
      <link href="https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap" rel="stylesheet">
      <style>
        :root {
          --primary-color: #0d6efd;
          --primary-hover: #0056b3;
          --light-color: #f8f9fa;
          --dark-color: #343a40;
          --white: #ffffff;
        }
        /* Basic reset and body styling */
        body {
          margin: 0;
          padding: 0;
          background: #e9ecef;
          font-family: 'Roboto', sans-serif;
          display: flex;
          align-items: center;
          justify-content: center;
          height: 100vh;
        }
        /* Chat container styling */
        #chat-container {
          width: 400px;
          max-width: 100%;
          height: 600px;
          background: var(--white);
          border-radius: 10px;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
          display: flex;
          flex-direction: column;
          overflow: hidden;
          animation: fadeIn 0.5s ease-in;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        /* Header styling */
        #chat-header {
          background: var(--primary-color);
          color: var(--white);
          padding: 20px;
          text-align: center;
          font-size: 22px;
          font-weight: 500;
          letter-spacing: 0.5px;
        }
        /* Chat messages area */
        #chat-box {
          flex: 1;
          padding: 20px;
          overflow-y: auto;
          background: var(--light-color);
        }
        /* Input area styling */
        #message-input {
          display: flex;
          padding: 15px;
          background: var(--white);
          border-top: 1px solid #dee2e6;
        }
        #message {
          flex: 1;
          padding: 12px;
          border: 1px solid #ced4da;
          border-radius: 30px;
          font-size: 16px;
          outline: none;
          transition: border-color 0.3s ease;
        }
        #message:focus {
          border-color: var(--primary-color);
        }
        #send-btn {
          background: var(--primary-color);
          border: none;
          color: var(--white);
          padding: 12px 20px;
          margin-left: 10px;
          border-radius: 30px;
          font-size: 16px;
          cursor: pointer;
          transition: background 0.3s ease;
        }
        #send-btn:hover {
          background: var(--primary-hover);
        }
        /* Message bubbles styling */
        .message {
          margin-bottom: 20px;
          display: flex;
          animation: slideIn 0.3s ease-out;
        }
        @keyframes slideIn {
          from { opacity: 0; transform: translateX(20px); }
          to { opacity: 1; transform: translateX(0); }
        }
        .user-message {
          justify-content: flex-end;
        }
        .bot-message {
          justify-content: flex-start;
        }
        .message p {
          max-width: 70%;
          padding: 12px 18px;
          border-radius: 20px;
          font-size: 15px;
          margin: 0;
        }
        .user-message p {
          background: var(--primary-color);
          color: var(--white);
          border-bottom-right-radius: 0;
        }
        .bot-message p {
          background: var(--light-color);
          color: var(--dark-color);
          border-bottom-left-radius: 0;
          border: 1px solid #ced4da;
        }
      </style>
    </head>
    <body>
      <div id="chat-container">
        <div id="chat-header">Jees Hotel Chat</div>
        <div id="chat-box"></div>
        <div id="message-input">
          <input type="text" id="message" placeholder="Type your message..." onkeypress="checkEnter(event)">
          <button id="send-btn" onclick="sendMessage()">Send</button>
        </div>
      </div>
      <script>
        async function sendMessage() {
          const input = document.getElementById("message");
          const message = input.value.trim();
          if (!message) return;
          
          const chatBox = document.getElementById("chat-box");
          // Append the user's message
          chatBox.innerHTML += `<div class="message user-message"><p>${message}</p></div>`;
          
          // Send the message to the server
          const response = await fetch("/api", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "chat", message: message })
          });
          
          const data = await response.json();
          // Append the bot's message
          chatBox.innerHTML += `<div class="message bot-message"><p>${data.response}</p></div>`;
          
          input.value = "";
          chatBox.scrollTop = chatBox.scrollHeight;
        }
  
        function checkEnter(event) {
          if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
          }
        }
      </script>
    </body>
    </html>
    '''
# --- Context Manager Update ---
class ContextManager:
    def __init__(self):
        self.contexts: Dict[str, Dict] = {}
        self.user_profiles: Dict[str, Dict] = {}
        self.rate_limits: Dict[str, datetime] = {}

    def get_context(self, user_id: str) -> Dict:
        return self.contexts.get(user_id, {})
    
    def update_context(self, user_id: str, updates: Dict):
        self.contexts.setdefault(user_id, {}).update(updates)
    
    def clear_context(self, user_id: str):
        self.contexts.pop(user_id, None)
    
    def get_user_profile(self, user_id: str) -> Dict:
        return self.user_profiles.setdefault(user_id, {
            'preferred_language': None,  # No default language
            'state': 'awaiting_language',  # Awaiting language selection
            'last_interaction': datetime.now(),
            'conversation_history': [],
            'preferred_room_type': None,
            'booking_history': []
        })
    
    def log_interaction(self, user_id: str, message: str, intent: str):
        profile = self.get_user_profile(user_id)
        profile['conversation_history'].append({
            'timestamp': datetime.now(),
            'message': message,
            'intent': intent
        })
        profile['last_interaction'] = datetime.now()
    
    def check_rate_limit(self, user_id: str) -> bool:
        last_req = self.rate_limits.get(user_id)
        if last_req and (datetime.now() - last_req).seconds < 2:
            return True
        self.rate_limits[user_id] = datetime.now()
        return False

context_manager = ContextManager()

# --- Language Selection Handler ---
def handle_language_selection(user_id: str, message: str) -> str:
    profile = context_manager.get_user_profile(user_id)
    msg = message.strip().lower()
    if msg in ['en', 'english', '1']:
        profile.update({'preferred_language': 'en', 'state': 'normal'})
        return random.choice(RESPONSES['en']['greetings'])
    elif msg in ['so', 'somali', 'soomaali', '2']:
        profile.update({'preferred_language': 'so', 'state': 'normal'})
        return random.choice(RESPONSES['so']['greetings'])
    else:
        # If the selection is not recognized, prompt again.
        return RESPONSES['en']['language_prompt']

# --- Main Response Generator ---
def generate_response(user_id: str, message: str) -> str:
    profile = context_manager.get_user_profile(user_id)
    
    # Check if language selection is needed.
    if profile.get('preferred_language') is None or profile.get('state') == 'awaiting_language':
        return handle_language_selection(user_id, message)
    
    lang = profile.get('preferred_language', 'en')
    msg_lower = message.lower()
    
    # Handle greetings.
    if any(greet in msg_lower for greet in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]):
        return random.choice(RESPONSES[lang]["greetings"])
    
    # Handle room booking inquiries.
    if "book" in msg_lower or "reserve" in msg_lower or "room" in msg_lower:
        return "You can book a room directly through our website: [Book Now](https://live.ipms247.com/booking/book-rooms-jeeshotel)"
    
    # Handle customer support inquiries.
    if "support" in msg_lower or "help" in msg_lower or "contact" in msg_lower:
        return f"For immediate assistance, you can contact our support team via WhatsApp: {HOTEL_INFO['whatsapp']}"
    
    # Handle hotel location inquiries.
    if "where" in msg_lower or "location" in msg_lower or "address" in msg_lower:
        return f"Jees Hotel is located at {HOTEL_INFO['address']}."
    
    # Handle amenities inquiries.
    if "amenities" in msg_lower or "facilities" in msg_lower or "services" in msg_lower:
        amenities_list = "\n".join(HOTEL_INFO["amenities"])
        return f"We offer the following amenities:\n{amenities_list}\n\nIs there anything specific you’d like to know more about?"
    
    # Handle check-in/check-out inquiries.
    if "check-in" in msg_lower or "check-out" in msg_lower or "time" in msg_lower:
        return f"Check-in time: {HOTEL_INFO['check_in']} | Check-out time: {HOTEL_INFO['check_out']}."
    
    # Handle hotel policy inquiries.
    if "policy" in msg_lower or "rules" in msg_lower or "regulations" in msg_lower:
        policies_list = "\n".join(HOTEL_INFO["policies"])
        return f"Here are our hotel policies:\n{policies_list}\n\nLet us know if you need further clarification."
    
    # Default fallback.
    return handle_fallback(lang) or "Sorry, I didn’t understand that. Could you please rephrase?"

#UPLOAD TO CLOUD
def upload_to_cloud(file_path: str) -> str:
    """
    Simulates uploading a file to cloud storage and returns a URL.
    Replace this function with actual cloud upload logic.
    """
    if os.path.exists(file_path):
        print(f"✅ File uploaded successfully: {file_path}")
        return f"http://localhost:5000/static/{os.path.basename(file_path)}"  # Fake URL
    else:
        print(f"❌ File not found: {file_path}")
        return None
@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    data = request.get_json()
    incoming_msg = data.get('message', '')
    sender_number = data.get('sender', '')

    # Process chatbot response
    response_text = generate_response(sender_number, incoming_msg)

    # Send response back via Gupshup
    send_gupshup_message(sender_number, response_text)

    return jsonify({"message": "Message sent via Gupshup."}), 200

def send_gupshup_message(to_number, message):
    url = "https://api.gupshup.io/sm/api/v1/msg"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "apikey": GUPSHUP_API_KEY
    }
    payload = {
        "channel": "whatsapp",
        "source": GUPSHUP_WHATSAPP_NUMBER,
        "destination": to_number,
        "message": message,
        "src.name": "your_gupshup_bot_name"
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.json()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
