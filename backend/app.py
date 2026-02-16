"""
Tourism Chatbot Backend with Database Integration
This Flask app connects to tourism_chatbot.db and responds to user queries
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import random
import os

app = Flask(__name__)
CORS(app)

<<<<<<< HEAD
# Check if database exists
DATABASE_FILE = 'tourism_chatbot.db'

if not os.path.exists(DATABASE_FILE):
    print("❌ ERROR: Database file not found!")
    print("📝 Please run: python create_database.py")
    print("   This will create the tourism_chatbot.db file")
    exit(1)

print(f"✅ Database found: {DATABASE_FILE}")

# Database helper function
def get_db_connection():
    """Connect to SQLite database"""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Returns rows as dictionaries
    return conn

# Multi-language responses
RESPONSES = {
    'en': [
        "Let me check our database for you...",
        "I found some great options!",
        "Here's what I discovered:",
        "Perfect! Let me show you:",
    ],
    'hi': [
        "मुझे आपके लिए डेटाबेस जांचने दें...",
        "मुझे कुछ बढ़िया विकल्प मिले!",
    ],
    'es': ["¡Déjame revisar nuestra base de datos!", "¡Encontré opciones geniales!"],
    'fr': ["Laissez-moi vérifier notre base de données...", "J'ai trouvé d'excellentes options!"],
    'de': ["Lass mich unsere Datenbank überprüfen...", "Ich habe tolle Optionen gefunden!"]
=======
# Dummy chatbot responses in multiple languages
RESPONSES = {
    'en': [
        "That's interesting! Tell me more.",
        "I see what you mean. Can you elaborate?",
        "Hmm, let me think about that...",
        "Great question! Here's what I think:",
        "I understand. Would you like to know more?",
        "That's a good point!",
        "I'm here to help! What else would you like to know?",
    ],
    'hi': [
        "यह दिलचस्प है! मुझे और बताएं।",
        "मैं समझता हूं। क्या आप विस्तार से बता सकते हैं?",
        "हम्म, मुझे इसके बारे में सोचने दें...",
        "बढ़िया सवाल! यहाँ मेरा विचार है:",
        "मैं समझ गया। क्या आप और जानना चाहेंगे?",
        "यह एक अच्छा बिंदु है!",
        "मैं मदद के लिए यहाँ हूँ! आप और क्या जानना चाहेंगे?",
    ],
    'es': [
        "¡Eso es interesante! Cuéntame más.",
        "Entiendo lo que quieres decir. ¿Puedes elaborar?",
        "Hmm, déjame pensar en eso...",
        "¡Gran pregunta! Esto es lo que pienso:",
        "Entiendo. ¿Te gustaría saber más?",
        "¡Ese es un buen punto!",
        "¡Estoy aquí para ayudar! ¿Qué más te gustaría saber?",
    ],
    'fr': [
        "C'est intéressant! Dis-moi en plus.",
        "Je vois ce que vous voulez dire. Pouvez-vous développer?",
        "Hmm, laissez-moi y réfléchir...",
        "Excellente question! Voici ce que je pense:",
        "Je comprends. Voulez-vous en savoir plus?",
        "C'est un bon point!",
        "Je suis là pour vous aider! Que voulez-vous savoir d'autre?",
    ],
    'de': [
        "Das ist interessant! Erzähl mir mehr.",
        "Ich verstehe, was Sie meinen. Können Sie näher darauf eingehen?",
        "Hmm, lass mich darüber nachdenken...",
        "Tolle Frage! Das denke ich:",
        "Ich verstehe. Möchten Sie mehr wissen?",
        "Das ist ein guter Punkt!",
        "Ich bin hier um zu helfen! Was möchten Sie noch wissen?",
    ]
}

# Greetings in different languages
GREETINGS = {
    'en': {
        'hello': "Hello! How can I help you today?",
        'bye': "Goodbye! Have a great day!",
        'how_are_you': "I'm doing great! Thanks for asking. How are you?",
        'name': "I'm your friendly AI chatbot assistant!"
    },
    'hi': {
        'hello': "नमस्ते! आज मैं आपकी कैसे मदद कर सकता हूं?",
        'bye': "अलविदा! आपका दिन शुभ हो!",
        'how_are_you': "मैं बहुत अच्छा हूं! पूछने के लिए धन्यवाद। आप कैसे हैं?",
        'name': "मैं आपका दोस्ताना AI चैटबॉट सहायक हूं!"
    },
    'es': {
        'hello': "¡Hola! ¿Cómo puedo ayudarte hoy?",
        'bye': "¡Adiós! ¡Que tengas un gran día!",
        'how_are_you': "¡Estoy genial! Gracias por preguntar. ¿Cómo estás?",
        'name': "¡Soy tu amigable asistente chatbot de IA!"
    },
    'fr': {
        'hello': "Bonjour! Comment puis-je vous aider aujourd'hui?",
        'bye': "Au revoir! Passez une excellente journée!",
        'how_are_you': "Je vais très bien! Merci de demander. Comment allez-vous?",
        'name': "Je suis votre assistant chatbot IA convivial!"
    },
    'de': {
        'hello': "Hallo! Wie kann ich Ihnen heute helfen?",
        'bye': "Auf Wiedersehen! Haben Sie einen schönen Tag!",
        'how_are_you': "Mir geht es großartig! Danke der Nachfrage. Wie geht es Ihnen?",
        'name': "Ich bin Ihr freundlicher KI-Chatbot-Assistent!"
    }
>>>>>>> 21deca4cb83c080f23160562c4a13445e92d63f9
}

@app.route('/')
def home():
    """Home page"""
    return "🏨 Tourism Chatbot API with Database is running! Use /chat endpoint."

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint - also verifies database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Count records in each table
        cursor.execute('SELECT COUNT(*) FROM destinations')
        dest_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM hotels')
        hotel_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM attractions')
        attr_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM packages')
        pkg_count = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            "status": "✅ Backend & Database Working!",
            "database": DATABASE_FILE,
            "records": {
                "destinations": dest_count,
                "hotels": hotel_count,
                "attractions": attr_count,
                "packages": pkg_count,
                "total": dest_count + hotel_count + attr_count + pkg_count
            },
            "features": [
                "Search destinations",
                "Find hotels (by city/price)",
                "Browse attractions",
                "View tour packages",
                "Multi-language support"
            ]
        })
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

@app.route('/chat', methods=['POST'])
def chat():
<<<<<<< HEAD
    """Main chat endpoint with database queries"""
    try:
        # Get user message and language
        data = request.get_json()
        user_message = data.get('message', '').lower()
        language = data.get('language', 'en')
=======
    """
    Main chat endpoint with multi-language support
    Receives: { "message": "user's message", "language": "en" }
    Returns: { "response": "bot's response" }
    """
    try:
        # Get the message and language from user
        data = request.get_json()
        user_message = data.get('message', '')
        language = data.get('language', 'en')  # Default to English
>>>>>>> 21deca4cb83c080f23160562c4a13445e92d63f9
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
<<<<<<< HEAD
        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        bot_response = ""
        
        # ==================================================
        # QUERY TYPE 1: LIST ALL DESTINATIONS
        # ==================================================
        if any(word in user_message for word in ['destination', 'place', 'city', 'cities', 'show me', 'list', 'where to go']):
            cursor.execute('SELECT name, rating, description, best_season FROM destinations ORDER BY rating DESC')
            destinations = cursor.fetchall()
            
            if destinations:
                bot_response = "🏛️ **Top Destinations in Rajasthan:**\n\n"
                for i, dest in enumerate(destinations, 1):
                    bot_response += f"{i}. **{dest['name']}** ⭐ {dest['rating']}/5\n"
                    bot_response += f"   📝 {dest['description']}\n"
                    bot_response += f"   🌤️ Best Time: {dest['best_season']}\n\n"
                bot_response += "💡 Ask: 'Hotels in Jaipur' or 'What to see in Udaipur'"
            else:
                bot_response = "Sorry, no destinations found in database."
        
        # ==================================================
        # QUERY TYPE 2: FIND HOTELS
        # ==================================================
        elif any(word in user_message for word in ['hotel', 'stay', 'accommodation', 'where to stay', 'lodge']):
            
            # Check if specific city mentioned
            cursor.execute('SELECT id, name FROM destinations')
            destinations = cursor.fetchall()
            
            destination_id = None
            destination_name = None
            
            for dest in destinations:
                if dest['name'].lower() in user_message:
                    destination_id = dest['id']
                    destination_name = dest['name']
                    break
            
            # Build query based on whether city was specified
            if destination_id:
                cursor.execute('''
                    SELECT h.name, h.price, h.rating, h.amenities
                    FROM hotels h
                    WHERE h.destination_id = ?
                    ORDER BY h.rating DESC
                ''', (destination_id,))
                bot_response = f"🏨 **Hotels in {destination_name}:**\n\n"
            else:
                cursor.execute('''
                    SELECT h.name, h.price, h.rating, h.amenities, d.name as destination
                    FROM hotels h
                    JOIN destinations d ON h.destination_id = d.id
                    ORDER BY h.rating DESC
                    LIMIT 10
                ''')
                bot_response = "🏨 **Top Hotels in Rajasthan:**\n\n"
            
            hotels = cursor.fetchall()
            
            if hotels:
                for i, hotel in enumerate(hotels, 1):
                    bot_response += f"{i}. **{hotel['name']}**"
                    if 'destination' in hotel.keys():
                        bot_response += f" - {hotel['destination']}"
                    bot_response += "\n"
                    bot_response += f"   💰 ₹{hotel['price']}/night | ⭐ {hotel['rating']}/5\n"
                    bot_response += f"   ✨ {hotel['amenities']}\n\n"
                bot_response += "💡 Try: 'Hotels under 2000' or 'Cheap hotels'"
            else:
                bot_response = "Sorry, no hotels found."
        
        # ==================================================
        # QUERY TYPE 3: SHOW ATTRACTIONS
        # ==================================================
        elif any(word in user_message for word in ['attraction', 'visit', 'see', 'tourist spot', 'sightseeing', 'what to do']):
            
            # Check if specific city mentioned
            cursor.execute('SELECT id, name FROM destinations')
            destinations = cursor.fetchall()
            
            destination_id = None
            destination_name = None
            
            for dest in destinations:
                if dest['name'].lower() in user_message:
                    destination_id = dest['id']
                    destination_name = dest['name']
                    break
            
            if destination_id:
                cursor.execute('''
                    SELECT name, entry_fee, timing, type
                    FROM attractions
                    WHERE destination_id = ?
                ''', (destination_id,))
                bot_response = f"🎯 **Things to See in {destination_name}:**\n\n"
            else:
                cursor.execute('''
                    SELECT a.name, a.entry_fee, a.timing, a.type, d.name as destination
                    FROM attractions a
                    JOIN destinations d ON a.destination_id = d.id
                    ORDER BY a.entry_fee ASC
                    LIMIT 15
                ''')
                bot_response = "🎯 **Top Tourist Attractions:**\n\n"
            
            attractions = cursor.fetchall()
            
            if attractions:
                for i, attr in enumerate(attractions, 1):
                    fee_text = "Free Entry" if attr['entry_fee'] == 0 else f"₹{attr['entry_fee']}"
                    bot_response += f"{i}. **{attr['name']}**"
                    if 'destination' in attr.keys():
                        bot_response += f" - {attr['destination']}"
                    bot_response += "\n"
                    bot_response += f"   🎫 {fee_text} | ⏰ {attr['timing']}\n"
                    bot_response += f"   📌 Type: {attr['type']}\n\n"
                bot_response += "💡 Ask: 'Show attractions in Jaipur'"
            else:
                bot_response = "Sorry, no attractions found."
        
        # ==================================================
        # QUERY TYPE 4: TOUR PACKAGES
        # ==================================================
        elif any(word in user_message for word in ['package', 'tour', 'trip', 'plan', 'booking']):
            cursor.execute('''
                SELECT p.name, p.duration, p.price, p.includes, d.name as destination
                FROM packages p
                JOIN destinations d ON p.destination_id = d.id
                ORDER BY p.price ASC
            ''')
            packages = cursor.fetchall()
            
            if packages:
                bot_response = "📦 **Available Tour Packages:**\n\n"
                for i, pkg in enumerate(packages, 1):
                    bot_response += f"{i}. **{pkg['name']}** - {pkg['destination']}\n"
                    bot_response += f"   ⏱️ {pkg['duration']}\n"
                    bot_response += f"   💰 ₹{pkg['price']}\n"
                    bot_response += f"   ✅ Includes: {pkg['includes']}\n\n"
                bot_response += "💡 These packages include accommodation & meals!"
            else:
                bot_response = "Sorry, no packages found."
        
        # ==================================================
        # QUERY TYPE 5: BUDGET-BASED HOTEL SEARCH
        # ==================================================
        elif any(word in user_message for word in ['cheap', 'budget', 'affordable', 'under', 'below', 'less than']):
            
            # Try to extract price from message
            words = user_message.split()
            price_limit = 2000  # default
            
            for word in words:
                # Remove commas and rupee symbol
                clean_word = word.replace(',', '').replace('₹', '').replace('rs', '')
                if clean_word.isdigit():
                    price_limit = int(clean_word)
                    break
            
            cursor.execute('''
                SELECT h.name, h.price, h.rating, h.amenities, d.name as destination
                FROM hotels h
                JOIN destinations d ON h.destination_id = d.id
                WHERE h.price <= ?
                ORDER BY h.price ASC
            ''', (price_limit,))
            
            hotels = cursor.fetchall()
            
            if hotels:
                bot_response = f"🏨 **Hotels Under ₹{price_limit}:**\n\n"
                for i, hotel in enumerate(hotels, 1):
                    bot_response += f"{i}. **{hotel['name']}** - {hotel['destination']}\n"
                    bot_response += f"   💰 ₹{hotel['price']}/night | ⭐ {hotel['rating']}/5\n"
                    bot_response += f"   ✨ {hotel['amenities']}\n\n"
                bot_response += f"💡 Found {len(hotels)} hotels in your budget!"
            else:
                bot_response = f"Sorry, no hotels found under ₹{price_limit}. Try a higher budget!"
        
        # ==================================================
        # QUERY TYPE 6: SPECIFIC CITY INFO
        # ==================================================
        elif any(city in user_message for city in ['jaipur', 'udaipur', 'jaisalmer', 'jodhpur', 'pushkar', 'mount abu', 'bikaner']):
            
            # Find which city
            city_map = {
                'jaipur': 'Jaipur',
                'udaipur': 'Udaipur',
                'jaisalmer': 'Jaisalmer',
                'jodhpur': 'Jodhpur',
                'pushkar': 'Pushkar',
                'mount abu': 'Mount Abu',
                'bikaner': 'Bikaner'
            }
            
            dest_name = None
            for key, value in city_map.items():
                if key in user_message:
                    dest_name = value
                    break
            
            cursor.execute('SELECT * FROM destinations WHERE name = ?', (dest_name,))
            dest = cursor.fetchone()
            
            if dest:
                bot_response = f"🏛️ **{dest['name']}, {dest['state']}**\n\n"
                bot_response += f"📝 {dest['description']}\n\n"
                bot_response += f"⭐ Rating: {dest['rating']}/5\n"
                bot_response += f"🌤️ Best Season: {dest['best_season']}\n\n"
                bot_response += "💡 **What you can ask:**\n"
                bot_response += f"• 'Hotels in {dest_name}'\n"
                bot_response += f"• 'What to see in {dest_name}'\n"
                bot_response += f"• 'Tour packages for {dest_name}'"
            else:
                bot_response = "Sorry, destination not found in database."
        
        # ==================================================
        # GREETING
        # ==================================================
        elif any(word in user_message for word in ['hello', 'hi', 'hey', 'namaste', 'नमस्ते']):
            bot_response = "👋 **Hello! I'm your Rajasthan Tourism Assistant!**\n\n"
            bot_response += "I have information about **7 amazing destinations** with:\n"
            bot_response += "🏨 17 Hotels\n"
            bot_response += "🎯 25 Tourist Attractions\n"
            bot_response += "📦 13 Tour Packages\n\n"
            bot_response += "**Try asking:**\n"
            bot_response += "• 'Show me destinations'\n"
            bot_response += "• 'Find hotels in Jaipur'\n"
            bot_response += "• 'What to visit in Udaipur'\n"
            bot_response += "• 'Show tour packages'\n"
            bot_response += "• 'Hotels under 2000'\n"
            bot_response += "• 'Tell me about Jaisalmer'"
        
        # ==================================================
        # DEFAULT RESPONSE
        # ==================================================
        else:
            responses = RESPONSES.get(language, RESPONSES['en'])
            bot_response = random.choice(responses) + "\n\n"
            bot_response += "**I can help you with:**\n"
            bot_response += "🏛️ Destinations - 'show me places'\n"
            bot_response += "🏨 Hotels - 'find hotels in Jaipur'\n"
            bot_response += "🎯 Attractions - 'what to see in Udaipur'\n"
            bot_response += "📦 Packages - 'show tour packages'\n"
            bot_response += "💰 Budget - 'hotels under 2000'\n\n"
            bot_response += "Just ask me anything!"
        
        # Close database connection
        conn.close()
=======
        # Get responses for the selected language
        responses = RESPONSES.get(language, RESPONSES['en'])
        greetings = GREETINGS.get(language, GREETINGS['en'])
        
        # Simple rule-based responses
        user_message_lower = user_message.lower()
        
        if any(word in user_message_lower for word in ['hello', 'hi', 'hey', 'hola', 'bonjour', 'hallo', 'namaste', 'नमस्ते']):
            bot_response = greetings['hello']
        elif any(word in user_message_lower for word in ['bye', 'goodbye', 'see you', 'adiós', 'au revoir', 'auf wiedersehen', 'अलविदा']):
            bot_response = greetings['bye']
        elif any(word in user_message_lower for word in ['how are you', 'how r u', 'cómo estás', 'comment allez-vous', 'wie geht', 'कैसे हो']):
            bot_response = greetings['how_are_you']
        elif any(word in user_message_lower for word in ['name', 'who are you', 'quién eres', 'qui es-tu', 'wer bist du', 'नाम', 'कौन हो']):
            bot_response = greetings['name']
        else:
            # Random response for other messages
            bot_response = random.choice(responses)
>>>>>>> 21deca4cb83c080f23160562c4a13445e92d63f9
        
        return jsonify({
            "response": bot_response,
            "user_message": user_message,
            "language": language
        })
    
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
<<<<<<< HEAD
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🏨 TOURISM CHATBOT SERVER WITH DATABASE")
    print("=" * 60)
    print(f"📍 Server: http://localhost:5000")
    print(f"🗄️ Database: {DATABASE_FILE}")
    print("🌍 Covering: Jaipur, Udaipur, Jaisalmer, Jodhpur, Pushkar, Mount Abu, Bikaner")
    print("=" * 60)
    print("\n✅ Server starting...\n")
=======
        return jsonify({"error": str(e)}), 500

# Test endpoint to check if server is working
@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        "status": "Backend is working!", 
        "message": "API is ready",
        "features": [
            "Multi-language support (EN, HI, ES, FR, DE)",
            "Voice input/output",
            "Export to PDF/TXT",
            "Chat history storage",
            "Typing animation"
        ]
    })

if __name__ == '__main__':
    print("🚀 Starting chatbot server...")
    print("📍 Server running at: http://localhost:5000")
    print("💬 Chat endpoint: http://localhost:5000/chat")
    print("🌍 Supported languages: English, Hindi, Spanish, French, German")
    print("🎤 Features: Voice I/O, PDF/TXT Export, Multi-language")
>>>>>>> 21deca4cb83c080f23160562c4a13445e92d63f9
    app.run(debug=True, port=5000)