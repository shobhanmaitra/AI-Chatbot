from flask import Flask, request, jsonify
from flask_cors import CORS
import random

# Create Flask app
app = Flask(__name__)
CORS(app)  # This allows your frontend to talk to backend

# Dummy chatbot responses
RESPONSES = [
    "That's interesting! Tell me more.",
    "I see what you mean. Can you elaborate?",
    "Hmm, let me think about that...",
    "Great question! Here's what I think:",
    "I understand. Would you like to know more?",
    "That's a good point!",
    "I'm here to help! What else would you like to know?",
]

@app.route('/')
def home():
    """Home page - just to check if server is running"""
    return "🤖 Chatbot API is running! Use /chat endpoint to chat."

@app.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    Receives: { "message": "user's message" }
    Returns: { "response": "bot's response" }
    """
    try:
        # Get the message from user
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Simple echo + random response
        if "hello" in user_message.lower() or "hi" in user_message.lower():
            bot_response = "Hello! How can I help you today?"
        elif "bye" in user_message.lower():
            bot_response = "Goodbye! Have a great day!"
        elif "how are you" in user_message.lower():
            bot_response = "I'm doing great! Thanks for asking. How are you?"
        elif "name" in user_message.lower():
            bot_response = "I'm your friendly AI chatbot assistant!"
        else:
            # Random response for other messages
            bot_response = random.choice(RESPONSES)
        
        # Return the response
        return jsonify({
            "response": bot_response,
            "user_message": user_message
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Test endpoint to check if server is working
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"status": "Backend is working!", "message": "API is ready"})

if __name__ == '__main__':
    print("🚀 Starting chatbot server...")
    print("📍 Server running at: http://localhost:5000")
    print("💬 Chat endpoint: http://localhost:5000/chat")
    app.run(debug=True, port=5000)