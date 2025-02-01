from flask import Flask, request, jsonify
import random
import re
import spacy
import requests
from datetime import datetime
from typing import Dict, Tuple, Callable, Optional
import requests
from bs4 import BeautifulSoup
import os

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from twilio.rest import Client

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

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
def check_room_availability(room_type: str, checkin_date: str, checkout_date: str) -> bool:
    """
    Checks room availability on the ChessHotel booking website.
    """
    url = "https://live.ipms247.com/booking/book-rooms-jeeshotel"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example: Find the room availability section in the page (this needs to be adjusted)
            available_rooms = soup.find_all(class_="room-info")
            
            for room in available_rooms:
                if room_type.lower() in room.get_text(strip=True).lower():
                    return True  # Room is available
    except Exception as e:
        print(f"Error checking availability: {e}")
    
    return False  # Room is not available

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
            "I'm sorry, I didn't understand that. Could you please rephrase or choose from the following options?\n\n1️⃣ Room bookings\n2️⃣ Amenities info\n3️⃣ Special offers\n4️⃣ Hotel policies\n\nOr chat with a live agent: {whatsapp}",
            "I'm here to help with questions about:\n• Room availability\n• Check-in times\n• Special packages\n• Payment methods\n\nYou can also contact us directly: {phone}"
        ],
        "room_list": "Here are our room options:\n{room_list}\n\nWould you like more details about any specific room type?",
        "room_details": (
            "Here are the details for the {room_type}:\n"
            "- Price: {price}\n"
            "- Size: {size}\n"
            "- Beds: {beds}\n"
            "- Bathrooms: {bathrooms}\n\n"
            "Would you like to book this room, or do you have any further questions?"
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
        "booking": "Great! You've selected the {room_type}. When would you like to check in?",
        "special_offers": "We currently have the following special offers:\n{offers}\n\nWould you like to take advantage of any of these?",
        "policies": "Here are our hotel policies:\n{policies}\n\nDo you have any questions or need further clarification on these?",
        "feedback": "Thank you for chatting with us! How would you rate your experience today on a scale of 1-5?",
        "thank_you": "Thank you for your feedback! We look forward to welcoming you again.",
        "language_prompt": "Please choose your language:\n1. English (Type 'en')\n2. Somali (Type 'so')",
        "booking_date_prompt": "Please enter your desired check-in date (e.g., 2024-03-20):",
        "booking_confirm": "Confirm booking:\nRoom: {room_type}\nCheck-in Date: {dates}\nIs this correct? (yes/no)",
        "booking_success": "✅ Booking confirmed! We have sent the details to your email.",
        "booking_cancel": "Booking process cancelled. Let us know if you need any further assistance.",
        "room_selection_retry": "Please select a valid room type from the list.",
        "thanks": "You're welcome! Is there anything else I can assist you with?",
        "more_info": "Could you please provide more details or clarify your request?",
        "general": "I'm here to help with any questions you have about our hotel services. Feel free to ask!",
        "promotion": "Don't miss our exclusive deals and seasonal promotions! Check out our website for more details.",
        "reservation_status": "If you have a reservation and need to check its status, please provide your booking reference."
    },
    "so": {
        "greetings": [
            "Asalaamu calaykum! Ku soo dhawoow Jees Hotel. Sideen kuu caawin karnaa maanta?",
            "Asalaamu calaykum! Ku soo dhawoow Jees Hotel. Maxaan kuu qabaa?"
        ],
        "farewells": [
            "Mahadsanid inaad nala soo xiriirtay. Maalin wanaagsan!",
            "Haddii aad wax su'aalo ah qabto, waxaan joognaa 24/7. Maalin wanaagsan!",
            "Waxaan ku faraxsanahay inaan kaa caawinay. Nabad gelyo!"
        ],
        "fallback": [
            "Waan ka xumahay, ma fahmin su'aashaada. Fadlan isku day mar kale ama dooro mid ka mid ah xulashooyinkan:\n\n1️⃣ Qolalka\n2️⃣ Adeegyada\n3️⃣ Dalacsiinta\n4️⃣ Qaanuunnada hotelka\n\nAma si toos ah ula xiriir shaqaalaha: {whatsapp}",
            "Waxaan kaa caawin karaa su'aalaha ku saabsan:\n• Qolalka la heli karo\n• Waqtiga check-in\n• Xawaariiq gaar ah\n• Hababka lacag bixinta\n\nWaxaad sidoo kale nagala soo xiriiri kartaa: {phone}"
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
        "booking": "Waad ku mahadsan tahay! Waxaad dooratay qolka {room_type}. Goormaad rabtaa inaad sameyso check-in?",
        "special_offers": "Waxaan haynaa dalacsiimo gaar ah:\n{offers}\n\nMa rabtaa inaad ka faa'iideysato mid ka mid ah?",
        "policies": "Kuwani waa qaanuunnadeena:\n{policies}\n\nMa jirtaa wax su'aalo ah oo aad qabto ku saabsan?",
        "feedback": "Mahadsanid inaad nala soo xiriirtay! Sidee ayaad u qiimeyn lahayd adeeggeena maanta? (1-5)",
        "thank_you": "Waad ku mahadsan tahay jawaabtaada! Waxaan rajaynaynaa inaan mar kale ku aragno.",
        "language_prompt": "Fadlan dooro luqadda:\n1. English (Qor 'en')\n2. Soomaali (Qor 'so')",
        "booking_date_prompt": "Fadlan geli taariikhda aad rabto inaad soo gasho (tusaale, 2024-03-20):",
        "booking_confirm": "Xaqiiji buugista:\nQolka: {room_type}\nTaariikhda: {dates}\nMa saxaa? (haa/ma)",
        "booking_success": "✅ Buugista waa la xaqiijiyay! Faahfaahinta waxaa laguu soo diray iimaylkaaga.",
        "booking_cancel": "Habka buugista waa la joojiyay. Haddii aad wax su'aalo ah qabto, fadlan nala soo xiriir.",
        "room_selection_retry": "Fadlan dooro nooc qol oo sax ah oo ka mid ah liiska.",
        "thanks": "Adigaa mudan! Ma jirtaa wax kale oo aan ku caawin karo?",
        "more_info": "Fadlan faahfaahin dheeraad ah bixiso si aan u fahamno baahidaada.",
        "general": "Waxaan kuu joognaa inaan kaa caawinno su'aalaha ku saabsan adeegyada hotelka. Weydii wixii aad qabto!",
        "promotion": "Ha moogaan dalacsiimadayada gaarka ah iyo heshiisyada xilliga! Booqo website-keena wixii faahfaahin ah.",
        "reservation_status": "Haddii aad hore u buugatay qol oo aad rabto inaad xaqiijiso, fadlan bixi tixraaca buugista."
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

def handle_booking(msg: str, uid: str, lang: str) -> str:
    context = context_manager.get_context(uid)
    profile = context_manager.get_user_profile(uid)
    entities = nlp_processor.extract_entities(msg)
    
    if not context.get('booking_stage'):
        context_manager.update_context(uid, {
            'booking_stage': 'room_selection',
            'booking_data': {}
        })
        return RESPONSES[lang]["room_list"].format(
            room_list="\n".join([f"- {room['type']}" for room in HOTEL_INFO["rooms"]])
        )
    
    if context['booking_stage'] == 'room_selection':
        room_match = next((room for room in HOTEL_INFO["rooms"] 
                         if room["type"].lower() in msg.lower()), None)
        if room_match:
            context['booking_data']['room'] = room_match
            context['booking_stage'] = 'date_selection'
            return RESPONSES[lang]["booking_date_prompt"]
        return RESPONSES[lang]["room_selection_retry"]
    
    if context['booking_stage'] == 'date_selection':
        if entities['dates']:
            context['booking_data']['dates'] = entities['dates'][0]
            context['booking_stage'] = 'confirmation'
            return RESPONSES[lang]["booking_confirm"].format(
                room_type=context['booking_data']['room']['type'],
                dates=context['booking_data']['dates']
            )
        return RESPONSES[lang]["booking_date_prompt"]
    
    if context['booking_stage'] == 'confirmation':
        if 'yes' in msg.lower() or 'ha' in msg.lower():
            profile['booking_history'].append(context['booking_data'])
            context_manager.clear_context(uid)
            return RESPONSES[lang]["booking_success"]
        context_manager.clear_context(uid)
        return RESPONSES[lang]["booking_cancel"]
    
    return handle_fallback(lang)

def handle_fallback(lang: str) -> str:
    web_result = search_web("Hotel services")
    fallback = random.choice(RESPONSES[lang]["fallback"]).format(**HOTEL_INFO)
    return f"{fallback}\n\n🌐 {web_result}"

# =====================
# Enhanced Chat Flow
# =====================

intent_system = IntentHandler()
def generate_booking_confirmation_pdf(booking_data: dict, filename="booking_confirmation.pdf") -> str:
    """
    Generate a PDF booking confirmation based on the provided details.
    """
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "CONFIRM BOOKING")

    # Booking Reference Number
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Booking Reference No: {booking_data.get('request_number', 'N/A')}")

    # Customer and Booking Details
    c.drawString(50, height - 140, f"Customer Name: {booking_data.get('name', 'N/A')}")
    c.drawString(50, height - 160, f"Check-in Date: {booking_data.get('checkindate', 'N/A')}")
    c.drawString(50, height - 180, f"Check-out Date: {booking_data.get('checkoutdate', 'N/A')}")
    c.drawString(50, height - 200, f"Room Type: {booking_data.get('room_type', 'N/A')}")
    c.drawString(50, height - 220, f"Nights: {booking_data.get('noofnights', 'N/A')}")
    
    # Special Requests
    c.drawString(50, height - 260, f"Special Request: {booking_data.get('specialrequirement', 'None')}")

    # Contact Details
    c.drawString(50, height - 300, f"Hotel Name: {booking_data.get('hotelname', 'Chess Hotel')}")
    c.drawString(50, height - 320, f"Hotel Address: {booking_data.get('hoteladdress1', 'N/A')}")
    c.drawString(50, height - 340, f"Hotel Phone: {booking_data.get('hotelphone', 'N/A')}")
    c.drawString(50, height - 360, f"Hotel Email: {booking_data.get('owneremail', 'N/A')}")

    c.drawString(50, height - 400, "Thank you for choosing Chess Hotel. We look forward to welcoming you!")
    
    c.save()
    return filename

# Register intent handlers
intent_system.register_handler(
    intents=['room', 'suite', 'accommodation'],
    handler=handle_rooms,
    priority=2
)

intent_system.register_handler(
    intents=['book', 'reserve', 'booking'],
    handler=handle_booking,
    priority=1
)

intent_system.set_fallback(lambda msg, uid, lang: handle_fallback(lang))

@app.route('/')
def home():
    return "Welcome to Jees Hotel Chatbot! Use /chatbot at the end of the url to start chatting"

@app.route('/api', methods=['POST'])
def api_handler():
    """
    Handles:
    - Room booking confirmation
    - Chatbot conversations
    """
    try:
        data = request.get_json()
        action = data.get("action")

        # === HANDLE ROOM BOOKING ===
        if action == "confirm_booking":
            room_type = data.get("room_type")
            checkin_date = data.get("checkindate")
            checkout_date = data.get("checkoutdate")
            
            # 1. Check room availability
            if not check_room_availability(room_type, checkin_date, checkout_date):
                return jsonify({"error": "The selected room is not available for the chosen dates."}), 400

            # 2. Generate PDF confirmation
            pdf_filename = generate_booking_confirmation_pdf(data)
            
            # 3. Upload the file to cloud storage and get URL
            media_url = upload_to_cloud(pdf_filename)  # Implement this function
            
            if not media_url:
                return jsonify({"error": "Failed to upload confirmation document."}), 500

            # 4. Send WhatsApp message to the hotel
            message_body = f"New booking confirmed for {data['name']}.\nRoom: {room_type}\nCheck-in: {checkin_date}"
            send_whatsapp_message(media_url, message_body, "whatsapp:+HOTEL_WHATSAPP_NUMBER")

            return jsonify({"message": "Booking confirmed and sent to hotel via WhatsApp."}), 200

        # === HANDLE CHATBOT CONVERSATIONS ===
        elif action == "chat":
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
    Chatbot Web Interface for Jees Hotel
    """
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Jees Hotel Chat</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: white;
                padding: 0;
                margin: 0;
            }
            #chat-container {
                width: 100%;
                height: 100%;
                max-width: 340px;
                max-height: 450px;
                display: flex;
                flex-direction: column;
                border: 2px solid #007bff;
                border-radius: 15px;
                overflow: hidden;
            }
            #chat-header {
                background: linear-gradient(45deg, #007bff, #0056b3);
                color: white;
                padding: 10px;
                text-align: center;
                font-weight: bold;
                font-size: 16px;
                border-radius: 15px 15px 0 0;
            }
            #chat-box {
                flex: 1;
                padding: 10px;
                overflow-y: auto;
                height: 320px;
                background: #f8f9fa;
            }
            #message-input {
                display: flex;
                border-top: 1px solid #ddd;
                padding: 8px;
                background: white;
            }
            #message {
                flex: 1;
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
            }
            #send-btn {
                padding: 8px 15px;
                background: #007bff;
                color: white;
                border: none;
                cursor: pointer;
                margin-left: 5px;
                border-radius: 5px;
            }
        </style>
    </head>
    <body>
        <div id="chat-container">
            <div id="chat-header">🏨 Jees Hotel</div>
            <div id="chat-box"></div>
            <div id="message-input">
                <input type="text" id="message" placeholder="Type a message..." onkeypress="checkEnter(event)">
                <button id="send-btn" onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            async function sendMessage() {
                let input = document.getElementById("message");
                let message = input.value.trim();
                if (message === "") return;
                
                let chatBox = document.getElementById("chat-box");
                chatBox.innerHTML += `<div style="text-align: right; margin: 5px;"><strong>You:</strong> ${message}</div>`;
                
                let response = await fetch("/api", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ action: "chat", message: message })
                });
                
                let data = await response.json();
                chatBox.innerHTML += `<div style="text-align: left; margin: 5px; color: blue;"><strong>Bot:</strong> ${data.response}</div>`;
                
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

def generate_response(user_id: str, message: str) -> str:
    profile = context_manager.get_user_profile(user_id)
    
    # Handle language selection
    if profile.get('state') == 'language_selection':
        return handle_language_selection(user_id, message)
    
    # Process message
    lang = profile.get('preferred_language', 'en')
    intent_handler = intent_system.match_intent(message, user_id)
    
    if intent_handler:
        context_manager.log_interaction(user_id, message, intent_handler.__name__)
        return intent_handler(message, user_id, lang)
    
    return handle_fallback(lang)

def handle_language_selection(user_id: str, message: str) -> str:
    msg = message.strip().lower()
    if msg in ['en', 'english', '1']:
        profile = context_manager.get_user_profile(user_id)
        profile.update({'preferred_language': 'en', 'state': 'normal'})
        return random.choice(RESPONSES['en']['greetings'])
    if msg in ['so', 'somali', 'soomaali', '2']:
        profile = context_manager.get_user_profile(user_id)
        profile.update({'preferred_language': 'so', 'state': 'normal'})
        return random.choice(RESPONSES['so']['greetings'])
    return RESPONSES[profile.get('preferred_language', 'en')]["language_prompt"]

def search_web(query: str) -> str:
    try:
        response = requests.get(f"http://api.duckduckgo.com/?q={query}&format=json", timeout=3)
        result = response.json()
        return result.get('AbstractText', '')[:200] + '...' if result.get('AbstractText') else "No results found"
    except Exception as e:
        return "Search unavailable"

# Keep other handler functions (handle_amenities, handle_contact, etc.) similar to original
def send_whatsapp_message(media_url: str, body: str, to_whatsapp_number: str) -> str:
    """
    Sends a WhatsApp message with a media attachment (PDF confirmation).
    """
    # Twilio Credentials (Replace with actual credentials)
    account_sid = "YOUR_TWILIO_ACCOUNT_SID"
    auth_token = "YOUR_TWILIO_AUTH_TOKEN"
    twilio_whatsapp_number = "whatsapp:+YOUR_TWILIO_WHATSAPP_NUMBER"

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_=twilio_whatsapp_number,
        to=to_whatsapp_number,
        media_url=[media_url]
    )
    return message.sid
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
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
