from flask import Flask, request, jsonify
from flask_cors import CORS
import random

# Create Flask app
app = Flask(__name__)
CORS(app)  # This allows your frontend to talk to backend

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
}

@app.route('/')
def home():
    """Home page - just to check if server is running"""
    return "🤖 Chatbot API is running! Use /chat endpoint to chat."

@app.route('/chat', methods=['POST'])
def chat():
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
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
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
        
        # Return the response
        return jsonify({
            "response": bot_response,
            "user_message": user_message,
            "language": language
        })
    
    except Exception as e:
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
    app.run(debug=True, port=5000)