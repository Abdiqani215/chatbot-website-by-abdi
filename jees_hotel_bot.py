from flask import Flask, request, jsonify
import random
import spacy
import requests  # For web search functionality

app = Flask(__name__)

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

# Hotel information and configuration
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
        "Free airport transfer for VIP rooms."
    ],
    "policies": [
        "Pets are not allowed."
    ]
}

# Enhanced Response templates
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
            "I'm here to help with:\n1️⃣ Room bookings\n2️⃣ Amenities info\n3️⃣ Special offers\n4️⃣ Hotel policies\n\nOr chat with a live agent: {whatsapp}",
            "Need help with:\n• Room availability\n• Check-in times\n• Special packages\n• Payment methods\n\nContact us directly: {phone}"
        ],
        "room_list": "Here are our room options:\n{room_list}\n\nWould you like to know more about any specific room type?",
        "room_details": (
            "Here are the details for the {room_type}:\n"
            "- Price: {price}\n"
            "- Size: {size}\n"
            "- Beds: {beds}\n"
            "- Bathrooms: {bathrooms}\n\n"
            "Would you like to book this room?"
        ),
        "amenities": "We offer the following amenities:\n{amenities}\n\nIs there anything specific you'd like to know more about?",
        "check_times": "Our check-in time is {check_in} and check-out is {check_out}.\nDo you need help with your booking schedule?",
        "contact": "📞 Call us: {phone}\n📧 Email: {email}\n💬 WhatsApp: {whatsapp}\n\nWe're available 24/7!",
        "address": "We're located at {address}.\nDo you need directions or transportation information?",
        "whatsapp": {
            "message": "Click the WhatsApp icon below to chat with us directly!",
            "whatsapp_url": "{whatsapp}",
            "icon_suggestion": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
        },
        "booking": "Great! You've selected the {room_type}. When would you like to check in?",
        "special_offers": "We have the following special offers:\n{offers}\n\nWould you like to take advantage of any of these?",
        "policies": "Here are our hotel policies:\n{policies}\n\nDo you have any questions about these?",
        "feedback": "Thank you for chatting with us! How would you rate your experience today? (1-5)",
        "thank_you": "Thank you for your feedback! We hope to see you again soon.",
        "language_prompt": "Please choose your language:\n1. English (Type 'en')\n2. Somali (Type 'so')"
    },
    "so": {
        "greetings": [
            "Salaam! Ku soo dhawoow hôtelka Jees. Sideen kuu caawin karnaa maanta?",
            "Iska warran! Sideen kugu caawin karnaa galashadaada hôtelka Jees?",
            "Salaan! Maxaan kuu qaban karaa maanta?"
        ],
        "farewells": [
            "Waad ku mahadsan tahay inaad nala hadashay! Maalintaa wanaagsan ha kuu dhaqdo!",
            "Haddii aad wax u baahan tahay, waan joognaa. Maalintaa wanaagsan ha kuu dhaqdo!",
            "Waxaan ku faraxsanahay inaan kugu caawinay. Iska warran!"
        ],
        "fallback": [
            "Waan kuu caawin karaa:\n1️⃣ Buugista qolalka\n2️⃣ Adeegyada\n3️⃣ Hormarimo\n4️⃣ Qaanuunnada\n\nAma kala hadal shaqaale: {whatsapp}",
            "Caawimaad ku saabsan:\n• Qolalka la heli karo\n• Waqtiga check-in\n• Xawaariiq gaar ah\n• Hababka lacag bixinta\n\nNala soo xiriir: {phone}"
        ],
        "room_list": "Waa kuwan qolalkayaga:\n{room_list}\n\nMa doonaysaa inaad wax badan ka ogaato nooc gaar ah oo qol?",
        "room_details": (
            "Waa kuwan faahfaahinta qolka {room_type}:\n"
            "- Qiimaha: {price}\n"
            "- Cabbirka: {size}\n"
            "- Sariir: {beds}\n"
            "- Musqul: {bathrooms}\n\n"
            "Ma rabtaa inaad buuxiso qolkan?"
        ),
        "amenities": "Waxaan bixinaa adeegyadan:\n{amenities}\n\nMa jirtaa wax gaar ah oo aad rabto inaad wax badan ka ogaato?",
        "check_times": "Waqtiga check-in waa {check_in}, check-out waa {check_out}.\nMa u baahan tahay caawimo ku saabsan jadwalkaaga buugista?",
        "contact": "📞 Wac: {phone}\n📧 Iimeyl: {email}\n💬 WhatsApp: {whatsapp}\n\nWaa aan heli karnaa 24/7!",
        "address": "Waxaan ku yaallaa {address}.\nMa u baahan tahay tilmaamo ama macluumaad gaadiid?",
        "whatsapp": {
            "message": "Guji sumadda WhatsApp hoose si aad nala hadasho si toos ah!",
            "whatsapp_url": "{whatsapp}",
            "icon_suggestion": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
        },
        "booking": "Waad ku mahadsan tahay! Waxaad dooratay qolka {room_type}. Goormaad rabtaa inaad check-in sameyso?",
        "special_offers": "Waxaan haysannaa hormarimo gaar ah:\n{offers}\n\nMa rabtaa inaad ka faa'iideysato mid ka mid ah?",
        "policies": "Waa kuwan qaanuunnadeena:\n{policies}\n\nMa jiraan su'aalo aad ku qabato kuwaas?",
        "feedback": "Waad ku mahadsan tahay inaad nala hadashay! Immisa ayaad ku qiimeyn lahayd waxtarkayaga maanta? (1-5)",
        "thank_you": "Waad ku mahadsan tahay jawaabtaada! Waxaan ku rajeyneynaa inaan mar kale ku arki doono.",
        "language_prompt": "Fadlan dooro luqadda:\n1. English (Qor 'en')\n2. Soomaali (Qor 'so')"
    }
}

# Enhanced conversation context management
conversation_context = {}

def update_context(user_id, key, value):
    if user_id not in conversation_context:
        conversation_context[user_id] = {}
    conversation_context[user_id][key] = value

def get_context(user_id, key):
    return conversation_context.get(user_id, {}).get(key)

# Web search functionality
def search_web(query):
    """Use DuckDuckGo Instant Answer API"""
    try:
        response = requests.get(f"http://api.duckduckgo.com/?q={query}&format=json")
        result = response.json()
        if result['AbstractText']:
            return f"Here's what I found: {result['AbstractText'][:200]}..."
        return "I couldn't find specific information online. Please contact our team directly."
    except Exception as e:
        return "Search unavailable. Please try again later."

# AI-Powered Suggestions
def generate_suggestions(user_id):
    context = conversation_context.get(user_id, {})
    if context.get('last_room_viewed'):
        return f"Would you like to book our {context['last_room_viewed']}?"
    return "Check out our rooftop restaurant specials!" if random.random() > 0.5 else "Need directions to the hotel?"

# Enhanced Intent Handlers
INTENT_HANDLERS = {
    'greeting': (
        ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'salaam', 'iska warran', 'asc'],
        lambda lang: random.choice(RESPONSES[lang]["greetings"])
    ),
    'farewell': (
        ['bye', 'goodbye', 'see you', 'thanks', 'thank you', 'mahadsanid', 'wcs', 'farewell'],
        lambda lang: random.choice(RESPONSES[lang]["farewells"])
    ),
    'room': (
        ['room', 'suite', 'accommodation', 'stay', 'bed', 'reservation', 
         'availability', 'book now', 'pricing', 'rates', 'qolka', 'meherka'],
        lambda msg, uid, lang: handle_rooms(msg, uid, lang)
    ),
    'booking': (
        ['book', 'reserve', 'booking', 'reservation', 'i want to make booking', 
         'can i book a room', 'how to book', 'make a booking', 'reserve a room'],
        lambda msg, uid, lang: handle_booking(msg, uid, lang)
    ),
    'amenities': (
        ['amenities', 'services', 'facilities', 'features', 'adeegyada', 
         'what do you offer', 'hotel services'],
        lambda lang: handle_amenities(lang)
    ),
    'check_times': (
        ['check-in', 'check-out', 'check in', 'check out', 'waqti', 
         'when can i check in', 'schedule'],
        lambda lang: handle_check_times(lang)
    ),
    'contact': (
        ['contact', 'phone', 'email', 'reach', 'xiriir', 
         'how can i reach you', 'hotel email'],
        lambda lang: handle_contact(lang)
    ),
    'address': (
        ['location', 'address', 'where are you', 'directions', 
         'meesha', 'goobta', 'xagay ku taala'],
        lambda lang: handle_address(lang)
    ),
    'whatsapp': (
        ['talk to person', 'human', 'representative', 'whatsapp', 
         'chat', 'hadal', 'send whatsapp'],
        lambda lang: handle_whatsapp(lang)
    ),
    'special_offers': (
        ['offers', 'discounts', 'promotions', 'hormarimo', 
         'any special offers', 'hotel deals'],
        lambda lang: handle_special_offers(lang)
    ),
    'policies': (
        ['policies', 'rules', 'cancellation', 'qaanuun', 
         'what are your policies', 'hotel rules'],
        lambda lang: handle_policies(lang)
    ),
    'feedback': (
        ['feedback', 'rate', 'review', 'qiimee', 
         'can i leave feedback', 'hotel review'],
        lambda uid, lang: handle_feedback(uid, lang)
    ),
    'thank_you': (
        ['thank you', 'mahadsanid', 'thanks', 'shukran'],
        lambda lang: handle_thank_you(lang)
    ),
    'language': (
        ['change language', 'luqad', 'language', 
         'how to switch language', 'english', 'soomaali'],
        lambda uid: handle_language_change(uid)
    ),
    'weather': (
        ['weather', 'temperature', 'forecast', 
         'climate', 'celcis', 'how hot is it'],
        lambda lang: search_web(f"Weather in {HOTEL_INFO['address']}")
    )
}

def detect_intent(message):
    message = message.lower()
    for intent, (keywords, _) in INTENT_HANDLERS.items():
        if any(keyword in message for keyword in keywords):
            return intent
    return None

def generate_response(user_id, message):
    if user_id not in conversation_context:
        conversation_context[user_id] = {'state': 'language_selection'}

    user_context = conversation_context[user_id]

    if user_context.get('state') == 'language_selection':
        msg = message.strip().lower()
        if msg in ['en', 'english', '1']:
            user_context['lang'] = 'en'
            user_context['state'] = 'normal'
            return random.choice(RESPONSES['en']['greetings'])
        elif msg in ['so', 'somali', 'soomaali', '2']:
            user_context['lang'] = 'so'
            user_context['state'] = 'normal'
            return random.choice(RESPONSES['so']['greetings'])
        else:
            return RESPONSES[user_context.get('lang', 'en')]["language_prompt"]

    lang = user_context.get('lang', 'en')
    intent = detect_intent(message)
    
    if intent:
        handler = INTENT_HANDLERS[intent][1]
        response = ""
        if intent in ['room', 'booking', 'feedback']:
            response = handler(message, user_id, lang)
        elif intent == 'language':
            response = handler(user_id)
        else:
            response = handler(lang)
        
        # Add AI-powered suggestions
        suggestion = generate_suggestions(user_id)
        return f"{response}\n\n💡 Suggestion: {suggestion}"

    # Enhanced fallback with web search
    web_result = search_web(message)
    fallback = random.choice(RESPONSES[lang]["fallback"]).format(**HOTEL_INFO)
    return f"{fallback}\n\n🌐 Web Search: {web_result}"

@app.route('/')
def home():
    return "Welcome to Jees Hotel Chatbot!"

@app.route('/chatbot', methods=['GET'])
def chatbot_interface():
    return '''
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Jees Hotel Smart Chatbot</h1>
        <div style="border: 1px solid #ccc; padding: 20px; width: 400px;">
            <div id="chat-box" style="height: 300px; overflow-y: scroll; margin-bottom: 10px;"></div>
            <input type="text" id="message" style="width: 70%; padding: 5px;">
            <button onclick="sendMessage()" style="padding: 5px;">Send</button>
        </div>
        <script>
            async function sendMessage() {
                const message = document.getElementById('message').value;
                const chatBox = document.getElementById('chat-box');
                
                // Add user message
                chatBox.innerHTML += `<div style="text-align: right; margin: 5px;">You: ${message}</div>`;
                
                // Get bot response
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                
                // Add bot response
                chatBox.innerHTML += `<div style="text-align: left; margin: 5px; color: blue;">Bot: ${data.response}</div>`;
                
                // Clear input
                document.getElementById('message').value = '';
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        </script>
    </body>
    </html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_id = request.remote_addr  # Use IP as temporary user ID
        response = generate_response(user_id, data['message'])
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Intent Handler Implementations
def handle_rooms(message, user_id, lang):
    doc = nlp(message.lower())
    room_types = [room["type"].lower() for room in HOTEL_INFO["rooms"]]
    
    for token in doc:
        if token.text.lower() in room_types:
            room = next(r for r in HOTEL_INFO["rooms"] if r["type"].lower() == token.text.lower())
            update_context(user_id, 'last_room_viewed', room["type"])
            return RESPONSES[lang]["room_details"].format(**room)
    
    room_list = "\n".join([f"- {room['type']} ({room['price']})" for room in HOTEL_INFO["rooms"]])
    return RESPONSES[lang]["room_list"].format(room_list=room_list)

def handle_booking(message, user_id, lang):
    doc = nlp(message.lower())
    room_types = [room["type"].lower() for room in HOTEL_INFO["rooms"]]
    
    for token in doc:
        if token.text.lower() in room_types:
            room_type = next(r["type"] for r in HOTEL_INFO["rooms"] if r["type"].lower() == token.text.lower())
            update_context(user_id, 'booking_room', room_type)
            return RESPONSES[lang]["booking"].format(room_type=room_type)
    
    return random.choice(RESPONSES[lang]["fallback"]).format(**HOTEL_INFO)

def handle_amenities(lang):
    amenities = "\n".join([f"- {amenity}" for amenity in HOTEL_INFO["amenities"]])
    return RESPONSES[lang]["amenities"].format(amenities=amenities)

def handle_check_times(lang):
    return RESPONSES[lang]["check_times"].format(**HOTEL_INFO)

def handle_contact(lang):
    return RESPONSES[lang]["contact"].format(**HOTEL_INFO)

def handle_address(lang):
    return RESPONSES[lang]["address"].format(**HOTEL_INFO)

def handle_whatsapp(lang):
    return f"{RESPONSES[lang]['whatsapp']['message']}\n{RESPONSES[lang]['whatsapp']['whatsapp_url'].format(**HOTEL_INFO)}"

def handle_special_offers(lang):
    offers = "\n".join([f"- {offer}" for offer in HOTEL_INFO["special_offers"]])
    return RESPONSES[lang]["special_offers"].format(offers=offers)

def handle_policies(lang):
    policies = "\n".join([f"- {policy}" for policy in HOTEL_INFO["policies"]])
    return RESPONSES[lang]["policies"].format(policies=policies)

def handle_feedback(user_id, lang):
    update_context(user_id, 'awaiting_feedback', True)
    return RESPONSES[lang]["feedback"]

def handle_thank_you(lang):
    return RESPONSES[lang]["thank_you"]

def handle_language_change(user_id):
    conversation_context[user_id]["state"] = "language_selection"
    return RESPONSES[conversation_context[user_id].get("lang", "en")]["language_prompt"]

# Final App Initialization
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)