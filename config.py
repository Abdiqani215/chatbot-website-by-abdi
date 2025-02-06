# config.py
# =============================================================================
# JEES HOTEL CHATBOT CONFIGURATION
# =============================================================================
#
# This configuration file contains all settings, global constants, and response
# templates for the Jees Hotel chatbot. It includes API keys, hotel information,
# room specifications, multilingual response templates, as well as additional
# settings for debugging, logging, reservations, guest services, loyalty programs,
# and safety protocols.
#
# Please ensure that any modifications to these settings are thoroughly tested
# in a development environment prior to deployment.
#
# =============================================================================

# -----------------------------------------------------------------------------
# External API Configuration
# -----------------------------------------------------------------------------
GUPSHUP_API_KEY = "sk_29765d09144b460f98cbe7761c5a4601"
GUPSHUP_WHATSAPP_NUMBER = "+252634747907"

# -----------------------------------------------------------------------------
# HOTEL GENERAL INFORMATION
# -----------------------------------------------------------------------------
HOTEL_INFO = {
    "name": "Jees Hotel",
    "address": "Sha'ab Area, Hargeisa, Somaliland",
    "phone": "+252 63 8533333",
    "email": "info@jeeshotel.com",
    "whatsapp": "https://wa.me/252638533333",
    # -------------------------------------------------------------------------
    # Room Configurations
    # -------------------------------------------------------------------------
    "rooms": [
        {
            "type": "Deluxe Room",
            "price": "$49/night",
            "size": "24.20 m²",
            "beds": 1,
            "bathrooms": 1
        },
        {
            "type": "Super Deluxe Room",
            "price": "$59/night",
            "size": "26.30 m²",
            "beds": 1,
            "bathrooms": 1
        },
        {
            "type": "Twin/Double Room",
            "price": "$79/night",
            "size": "26.30 m²",
            "beds": 2,
            "bathrooms": 1
        },
        {
            "type": "Triple Room",
            "price": "$105/night",
            "size": "50 m²",
            "beds": 3,
            "bathrooms": 1
        },
        {
            "type": "VIP/Suite Room",
            "price": "$83/night",
            "size": "50 m²",
            "beds": 1,
            "bathrooms": 1
        }
    ],
    # -------------------------------------------------------------------------
    # Hotel Amenities Offered
    # -------------------------------------------------------------------------
    "amenities": [
        "Complimentary Wi-Fi",
        "Free Parking",
        "Fitness Center",
        "Rooftop Restaurant",
        "Complimentary Airport Transfer",
        "Laundry Service",
        "On-site ATMs"
    ],
    # -------------------------------------------------------------------------
    # Check-In and Check-Out Timings
    # -------------------------------------------------------------------------
    "check_in": "1:00 PM",
    "check_out": "12:00 PM",
    # -------------------------------------------------------------------------
    # Special Offers for Guests
    # -------------------------------------------------------------------------
    "special_offers": [
        "Free airport transfer for ALL rooms.",
        "20% discount on extended stays during off-peak seasons.",
        "Complimentary breakfast for reservations made 30 days in advance."
    ],
    # -------------------------------------------------------------------------
    # Hotel Policies and Guidelines
    # -------------------------------------------------------------------------
    "policies": [
        "Pets are not allowed on the premises.",
        "No smoking is permitted in any indoor areas.",
        "Guests must adhere to the designated check-in/check-out times.",
        "Any damage to hotel property will be charged to the guest."
    ],
    # -------------------------------------------------------------------------
    # Additional Guest Services and Programs
    # -------------------------------------------------------------------------
    "guest_services": {
        "concierge": "Our concierge service is available 24/7 to assist with local recommendations and bookings.",
        "room_service": "Room service is available from 7:00 AM to 11:00 PM daily.",
        "laundry": "Laundry services are provided with a same-day turnaround option at an additional cost.",
        "spa": "Rejuvenate at our in-house spa offering a variety of therapeutic treatments."
    },
    # -------------------------------------------------------------------------
    # Loyalty and Rewards Program Details
    # -------------------------------------------------------------------------
    "loyalty_program": {
        "program_name": "Jees Rewards",
        "benefits": [
            "Earn points on every booking",
            "Exclusive discounts on room rates",
            "Priority booking for special events",
            "Complimentary upgrades (subject to availability)"
        ],
        "join_url": "https://jeeshotel.com/loyalty"
    },
    # -------------------------------------------------------------------------
    # COVID-19 Safety Guidelines and Protocols
    # -------------------------------------------------------------------------
    "covid_guidelines": "We strictly adhere to enhanced cleaning protocols, social distancing measures, and contactless services to ensure your safety.",
    # -------------------------------------------------------------------------
    # Social Media and Online Presence
    # -------------------------------------------------------------------------
    "social_media": {
        "facebook": "https://www.facebook.com/jeeshotel",
        "instagram": "https://www.instagram.com/jeeshotel",
        "twitter": "https://twitter.com/jeeshotel"
    },
    # -------------------------------------------------------------------------
    # Corporate and Business Inquiries Contact Information
    # -------------------------------------------------------------------------
    "corporate_contact": {
        "phone": "+252 63 8533333 ext. 101",
        "email": "corporate@jeeshotel.com"
    }
}

# -----------------------------------------------------------------------------
# CHATBOT RESPONSE TEMPLATES
# -----------------------------------------------------------------------------
RESPONSES = {
    "en": {
        # ---------------------------------------------------------------------
        # Greetings for New Interactions
        # ---------------------------------------------------------------------
        "greetings": [
            "Hello and welcome to Jees Hotel! How may I assist you with your stay today?",
            "Greetings! Thank you for choosing Jees Hotel. How can I be of service?",
            "Good day! I am here to help with any inquiries regarding your stay at Jees Hotel."
        ],
        # ---------------------------------------------------------------------
        # Farewell Messages at the End of Conversations
        # ---------------------------------------------------------------------
        "farewells": [
            "Thank you for chatting with us. We wish you a wonderful day!",
            "It was our pleasure assisting you. We hope to welcome you again soon.",
            "Thank you for your inquiry. Have a great day ahead!"
        ],
        # ---------------------------------------------------------------------
        # Fallback Responses for Unrecognized Inputs
        # ---------------------------------------------------------------------
        "fallback": [
            "I'm sorry, I did not understand your request. Could you please rephrase or select one of the following options?\n\n"
            "1️⃣ Room bookings\n2️⃣ Amenities details\n3️⃣ Special offers\n4️⃣ Hotel policies\n\n"
            "Alternatively, you may speak with a live agent: {whatsapp}",
            "I apologize for the inconvenience. I can assist with queries regarding room availability, check-in times, or special packages. "
            "If needed, please contact us directly at {phone}."
        ],
        # ---------------------------------------------------------------------
        # Room List Response
        # ---------------------------------------------------------------------
        "room_list": (
            "Below is a list of our available room options:\n{room_list}\n\n"
            "Please let me know if you would like further details about any specific room type."
        ),
        # ---------------------------------------------------------------------
        # Detailed Room Information
        # ---------------------------------------------------------------------
        "room_details": (
            "Here are the comprehensive details for the {room_type}:\n"
            "- Price: {price}\n"
            "- Room Size: {size}\n"
            "- Number of Beds: {beds}\n"
            "- Number of Bathrooms: {bathrooms}\n\n"
            "To proceed with a booking, please visit our online booking portal: [👉 Book Here](https://live.ipms247.com/booking/book-rooms-jeeshotel)."
        ),
        # ---------------------------------------------------------------------
        # Amenities Information
        # ---------------------------------------------------------------------
        "amenities": (
            "Our hotel proudly offers the following amenities:\n{amenities}\n\n"
            "Should you require additional details on any service, please let me know."
        ),
        # ---------------------------------------------------------------------
        # Check-In and Check-Out Timings
        # ---------------------------------------------------------------------
        "check_times": (
            "Our standard check-in time is {check_in} and check-out is at {check_out}. "
            "Would you like assistance with your arrival or departure arrangements?"
        ),
        # ---------------------------------------------------------------------
        # Contact Information
        # ---------------------------------------------------------------------
        "contact": (
            "For any inquiries, please reach out through the following channels:\n"
            "📞 Phone: {phone}\n"
            "📧 Email: {email}\n"
            "💬 WhatsApp: {whatsapp}\n\n"
            "Our support team is available around the clock to assist you."
        ),
        # ---------------------------------------------------------------------
        # Hotel Location Details
        # ---------------------------------------------------------------------
        "address": (
            "Jees Hotel is located at {address}. Would you like directions or additional transportation information?"
        ),
        # ---------------------------------------------------------------------
        # WhatsApp Contact Details
        # ---------------------------------------------------------------------
        "whatsapp": {
            "message": "Tap the WhatsApp icon below to initiate a direct conversation with our support team.",
            "whatsapp_url": "{whatsapp}",
            "icon_suggestion": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
        },
        # ---------------------------------------------------------------------
        # Booking Related Responses
        # ---------------------------------------------------------------------
        "booking": (
            "Please note that we no longer process bookings via this chatbot. "
            "To secure your reservation, kindly visit our online booking portal: [👉 Book Now](https://live.ipms247.com/booking/book-rooms-jeeshotel)."
        ),
        "booking_date_prompt": (
            "Bookings cannot be processed via the chatbot interface. For booking inquiries, please visit: [👉 Book Here](https://live.ipms247.com/booking/book-rooms-jeeshotel)."
        ),
        "booking_confirm": (
            "Our chatbot is currently not configured to handle direct bookings. "
            "Please proceed to our website for booking confirmations: [👉 Click Here](https://live.ipms247.com/booking/book-rooms-jeeshotel)."
        ),
        "booking_success": (
            "All bookings are exclusively handled through our official website. "
            "Kindly complete your reservation at [👉 Visit Here](https://live.ipms247.com/booking/book-rooms-jeeshotel)."
        ),
        "booking_cancel": (
            "Modifications or cancellations to bookings cannot be processed via this chatbot. "
            "Please contact our hotel management directly for any changes."
        ),
        # ---------------------------------------------------------------------
        # Additional Responses for Erroneous Room Selections
        # ---------------------------------------------------------------------
        "room_selection_retry": (
            "The room type you selected is not recognized. Please choose a valid option from the list provided."
        ),
        # ---------------------------------------------------------------------
        # Acknowledgment and Gratitude Responses
        # ---------------------------------------------------------------------
        "thanks": (
            "You're welcome! If you require further assistance, please feel free to ask."
        ),
        # ---------------------------------------------------------------------
        # Request for Additional Information
        # ---------------------------------------------------------------------
        "more_info": (
            "Could you kindly provide additional details or clarify your request?"
        ),
        # ---------------------------------------------------------------------
        # General Inquiry Responses
        # ---------------------------------------------------------------------
        "general": (
            "I am here to help with any questions you may have regarding our hotel services. "
            "Please feel free to ask your questions."
        ),
        # ---------------------------------------------------------------------
        # Promotional and Special Offers Notifications
        # ---------------------------------------------------------------------
        "promotion": (
            "Don't miss out on our exclusive deals and seasonal promotions! "
            "For more details, please visit our website."
        ),
        # ---------------------------------------------------------------------
        # Reservation Status Inquiry Response
        # ---------------------------------------------------------------------
        "reservation_status": (
            "For inquiries regarding an existing reservation, please contact our hotel management directly."
        ),
        # ---------------------------------------------------------------------
        # Feedback and Review Request
        # ---------------------------------------------------------------------
        "feedback": (
            "We value your feedback! On a scale of 1-5, how would you rate your experience with us today?"
        ),
        "thank_you": (
            "Thank you for your valuable feedback. We look forward to serving you again soon."
        ),
        # ---------------------------------------------------------------------
        # Language Selection Prompt
        # ---------------------------------------------------------------------
        "language_prompt": (
            "🌍 *Please select your preferred language:*\n\n"
            "1️⃣ *English 🇬🇧*\n"
            "2️⃣ *Somali 🇸🇴*\n\n"
            "👉 Type '1' for English or '2' for Somali."
        )
    },

    "so": {
        # ---------------------------------------------------------------------
        # Greetings in Somali
        # ---------------------------------------------------------------------
        "greetings": [
            "Asalaamu calaykum! Ku soo dhawoow Jees Hotel. Sideen kuu caawin karnaa maanta?",
            "Asalaamu calaykum! Ku soo dhawoow Jees Hotel. Maxaan kuu qabaa?",
            "Salaan diiran! Ma u baahan tahay caawimaad ku saabsan adeegyada Jees Hotel?"
        ],
        # ---------------------------------------------------------------------
        # Farewell Messages in Somali
        # ---------------------------------------------------------------------
        "farewells": [
            "Mahadsanid inaad nala soo xiriirtay. Maalin wanaagsan!",
            "Haddii aad wax su'aalo ah qabto, waxaan joognaa 24/7. Maalin wanaagsan!",
            "Waxaan ku faraxsanahay inaan kaa caawinay. Nabad gelyo! Waxaan rajaynaynaa inaan kugu aragno mar kale."
        ],
        # ---------------------------------------------------------------------
        # Fallback Responses in Somali
        # ---------------------------------------------------------------------
        "fallback": [
            "Waan ka xumahay, ma fahmin su'aashaada. Fadlan isku day mar kale ama dooro mid ka mid ah xulashooyinkan:\n\n"
            "1️⃣ Qolalka\n2️⃣ Adeegyada\n3️⃣ Dalacsiinta\n4️⃣ Qaanuunnada hotelka\n\n"
            "Ama si toos ah ula xiriir shaqaalaha: {whatsapp}",
            "Waxaan kaa caawin karaa su'aalaha ku saabsan:\n• Qolalka la heli karo\n• Waqtiga check-in\n• Xawaariiq gaar ah\n• Hababka lacag bixinta\n\n"
            "Waxaad sidoo kale nagala soo xiriiri kartaa: {phone}"
        ],
        # ---------------------------------------------------------------------
        # Room List in Somali
        # ---------------------------------------------------------------------
        "room_list": (
            "Kuwani waa qolalka aanu bixino:\n{room_list}\n\n"
            "Fadlan sheeg qolka aad rabto si aad u hesho faahfaahin dheeraad ah."
        ),
        # ---------------------------------------------------------------------
        # Detailed Room Information in Somali
        # ---------------------------------------------------------------------
        "room_details": (
            "Waa kuwan faahfaahinta qolka {room_type}:\n"
            "- Qiimaha: {price}\n"
            "- Cabbirka: {size}\n"
            "- Sariiro: {beds}\n"
            "- Musqul: {bathrooms}\n\n"
            "Haddii aad rabto inaad qolka qabsato, fadlan booqo boggayaga: [👉 Guji Halkan](https://live.ipms247.com/booking/book-rooms-jeeshotel)"
        ),
        # ---------------------------------------------------------------------
        # Amenities Information in Somali
        # ---------------------------------------------------------------------
        "amenities": (
            "Waxaan bixinaa adeegyada soo socda:\n{amenities}\n\n"
            "Ma jirtaa wax gaar ah oo aad rabto inaad wax badan ka ogaato?"
        ),
        # ---------------------------------------------------------------------
        # Check-In and Check-Out Timings in Somali
        # ---------------------------------------------------------------------
        "check_times": (
            "Waqtiga check-in waa {check_in} iyo check-out waa {check_out}.\n"
            "Ma u baahan tahay caawimaad ku saabsan jadwalka buugista ama faahfaahin kale?"
        ),
        # ---------------------------------------------------------------------
        # Contact Information in Somali
        # ---------------------------------------------------------------------
        "contact": (
            "Waxaad nagala soo xiriiri kartaa adigoo adeegsanaya:\n"
            "📞 Wac: {phone}\n"
            "📧 Iimeyl: {email}\n"
            "💬 WhatsApp: {whatsapp}\n\n"
            "Waxaan nahay 24/7 si aan kuu caawinno."
        ),
        # ---------------------------------------------------------------------
        # Hotel Location Details in Somali
        # ---------------------------------------------------------------------
        "address": (
            "Hotelka wuxuu ku yaallaa {address}. Ma u baahan tahay tilmaamo ama macluumaad gaadiid?"
        ),
        # ---------------------------------------------------------------------
        # WhatsApp Contact Details in Somali
        # ---------------------------------------------------------------------
        "whatsapp": {
            "message": "Guji sumadda WhatsApp ee hoose si aad ula xiriirto shaqaalaha si toos ah!",
            "whatsapp_url": "{whatsapp}",
            "icon_suggestion": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
        },
        # ---------------------------------------------------------------------
        # Additional Services Information in Somali
        # ---------------------------------------------------------------------
        "wifi": "Haa, waxaan bixinaa internet xawaare sare leh (200 Mbps) oo bilaash ah.",
        "laundry": "Haa, waxaan bixinaa adeeg dhar dhaqis, balse qiimaha wuu kala duwan yahay iyadoo ku xiran dharka la dhaqayo.",
        "family": (
            "Hotelkan waxaa loogu talagalay qoysaska, inkasta oo aanu bixin sariiro dheeraad ah. "
            "Waxaad ka heli kartaa qolalka qoyska ee website-ka iyadoo la isticmaalayo nidaamka saddexda sariirood."
        ),
        "gym": "Haa, jimicsiga waa furan yahay laga bilaabo 6AM ilaa 10PM.",
        "restaurant": "Waxaan leenahay 7 maqaaxi oo kala duwan oo bixiya cuntooyin kala duwan sida rooftop, kafateeriyada, iyo maqaaxida caadiga ah.",
        "taxi": "Haa, waxaan bixin karnaa adeeg taksi oo lacag ah haddii aad u baahan tahay.",
        "airport": "Haa, waxaan bixinaa gaadiid bilaash ah oo lagu qaado dadka ka soo degaya garoonka, gaar ahaan qaybta VIP.",
        "rooms": (
            "Fadlan booqo: (https://live.ipms247.com/booking/book-rooms-jeeshotel) si aad u aragto noocyada kala duwan ee qolalka aanu bixino."
        ),
        "booking": (
            "Haddii aad rabto inaad qol qabsato, fadlan booqo boggayaga: (https://live.ipms247.com/booking/book-rooms-jeeshotel)"
        ),
        "policies": (
            "Kuwani waa qaanuunnada hotelka:\n{policies}\n\nMa jirtaa wax su'aalo ah oo aad qabto ku saabsan?"
        ),
        "feedback": (
            "Mahadsanid inaad nala soo xiriirtay! Fadlan sheeg haddii aad wax su'aalo ah qabtid ama aad rabto in wax badan lagaaga faahfaahiyo."
        ),
        "thank_you": "Waad ku mahadsan tahay jawaabtaada! Waxaan rajaynaynaa inaan mar kale kuu adeegno.",
        "language_prompt": (
            "🌍 *Fadlan dooro luqadda aad ku hadasho:* / *Please select your preferred language:*\n\n"
            "--------------------\n"
            "1️⃣ *English 🇬🇧*\n"
            "2️⃣ *Soomaali 🇸🇴*\n"
            "--------------------\n"
            "👉 *Qor '1' si aad u doorato Ingiriis, ama '2' si aad u doorato Soomaali.*\n"
            "👉 *Type '1' for English or '2' for Somali.*"
        )
    }
}

# -----------------------------------------------------------------------------
# Debug and Logging Settings
# -----------------------------------------------------------------------------
DEBUG_MODE = True
LOG_FILE_PATH = "logs/jees_hotel_chatbot.log"
MAX_LOG_SIZE_MB = 5
BACKUP_COUNT = 3

# -----------------------------------------------------------------------------
# Application Behavior Settings
# -----------------------------------------------------------------------------
RESPONSE_TIMEOUT_SECONDS = 30     # Timeout duration for chatbot responses (in seconds)
MAX_CHAT_HISTORY = 50             # Maximum number of messages stored per conversation
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ["en", "so"]

# -----------------------------------------------------------------------------
# API Endpoint Configuration
# -----------------------------------------------------------------------------
API_ENDPOINTS = {
    "booking": "https://live.ipms247.com/booking/book-rooms-jeeshotel",
    "loyalty": "https://jeeshotel.com/loyalty",
    "corporate": "https://jeeshotel.com/corporate"
}

# =============================================================================
# TERMS, CONDITIONS, AND PRIVACY POLICY
# =============================================================================
TERMS_AND_CONDITIONS = """
Welcome to Jees Hotel. By accessing our services, you agree to the following terms and conditions:
1. Reservations must be made exclusively through our official website.
2. Cancellation policies apply as per hotel guidelines.
3. All guest information is managed in accordance with our privacy policy.
4. Jees Hotel reserves the right to modify services without prior notice.
"""

PRIVACY_POLICY = """
At Jees Hotel, your privacy is of paramount importance. All personal information collected is used solely for enhancing your experience and will not be shared with third parties without your explicit consent.
For detailed information, please review our full privacy policy on our website.
"""

# =============================================================================
# RESERVATION AND BOOKING INSTRUCTIONS
# =============================================================================
RESERVATION_INSTRUCTIONS = """
To make a reservation at Jees Hotel:
1. Visit our official booking website at: {booking_url}
2. Select your preferred room and provide the necessary details.
3. You will receive a confirmation email containing your booking details.
"""

# =============================================================================
# GUEST SERVICES AND ADDITIONAL INFORMATION
# =============================================================================
GUEST_SERVICES = {
    "concierge": (
        "Our concierge service is available 24/7 to assist with local recommendations, "
        "transportation arrangements, and other guest needs."
    ),
    "room_service": "Room service is available from 7:00 AM to 11:00 PM daily.",
    "laundry": "Laundry services are provided with a same-day turnaround option. Charges apply per service.",
    "spa": "Experience our rejuvenating spa treatments. Appointments are recommended."
}
# =============================================================================
# SOCIAL MEDIA AND ONLINE PRESENCE
# =============================================================================
SOCIAL_MEDIA_LINKS = {
    "facebook": "https://www.facebook.com/jeeshotel",
    "instagram": "https://www.instagram.com/jeeshotel",
    "twitter": "https://twitter.com/jeeshotel",
    "linkedin": "https://www.linkedin.com/company/jeeshotel"
}

# =============================================================================
# ADDITIONAL REMINDER AND NOTIFICATION MESSAGES
# =============================================================================
NOTIFICATION_MESSAGES = {
    "check_in_reminder": (
        "Dear guest, this is a friendly reminder that your check-in time is at {check_in}. "
        "We look forward to welcoming you at Jees Hotel."
    ),
    "check_out_reminder": (
        "Please be advised that check-out time is at {check_out}. We hope you enjoyed your stay."
    ),
    "feedback_request": (
        "Your feedback is important to us. Kindly rate your experience on a scale of 1-5 after your stay."
    )
}
