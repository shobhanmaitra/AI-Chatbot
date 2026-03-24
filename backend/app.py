from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import random
import os
from llm_helper import get_smart_response, should_use_ai, format_database_results_for_ai, generate_trip_plan

app = Flask(__name__)
CORS(app)

DATABASE_FILE = 'tourism_chatbot.db'

if not os.path.exists(DATABASE_FILE):
    print("❌ ERROR: Database file not found!")
    exit(1)

print(f"✅ Database found: {DATABASE_FILE}")
print(f"✅ LLM Integration: Active (Google Gemini)")

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

RESPONSES = {
    'en': ["Let me check our database...", "I found some great options!", "Here's what I discovered:"],
    'hi': ["मुझे डेटाबेस जांचने दें...", "मुझे कुछ बढ़िया विकल्प मिले!"],
    'es': ["¡Déjame revisar!", "¡Encontré opciones geniales!"],
    'fr': ["Laissez-moi vérifier...", "J'ai trouvé d'excellentes options!"],
    'de': ["Lass mich überprüfen...", "Ich habe tolle Optionen gefunden!"]
}

@app.route('/')
def home():
    return "🏨 Tourism Chatbot API with LLM + Visualization!"

@app.route('/test', methods=['GET'])
def test():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
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
            "status": "✅ Backend, Database & LLM Working!",
            "database": DATABASE_FILE,
            "llm": "Google Gemini Pro",
            "visualization": "Chart.js Ready",
            "records": {
                "destinations": dest_count,
                "hotels": hotel_count,
                "attractions": attr_count,
                "packages": pkg_count,
                "total": dest_count + hotel_count + attr_count + pkg_count
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# CHART DATA ENDPOINTS
# ==========================================

@app.route('/api/chart/hotel-prices', methods=['GET'])
def get_hotel_prices_chart():
    """Get hotel price comparison data for charts"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT d.name as city, AVG(h.price) as avg_price, COUNT(h.id) as hotel_count
            FROM hotels h
            JOIN destinations d ON h.destination_id = d.id
            GROUP BY d.name
            ORDER BY avg_price DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        chart_data = {
            "labels": [row['city'] for row in results],
            "prices": [round(row['avg_price'], 2) for row in results],
            "counts": [row['hotel_count'] for row in results]
        }
        
        return jsonify(chart_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chart/destination-ratings', methods=['GET'])
def get_destination_ratings():
    """Get destination ratings for pie chart"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT name, rating FROM destinations ORDER BY rating DESC')
        results = cursor.fetchall()
        conn.close()
        
        chart_data = {
            "labels": [row['name'] for row in results],
            "ratings": [row['rating'] for row in results]
        }
        
        return jsonify(chart_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chart/attraction-prices', methods=['GET'])
def get_attraction_prices():
    """Get attraction entry fees for horizontal bar chart"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.name, a.entry_fee, d.name as city
            FROM attractions a
            JOIN destinations d ON a.destination_id = d.id
            WHERE a.entry_fee > 0
            ORDER BY a.entry_fee DESC
            LIMIT 10
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        chart_data = {
            "labels": [f"{row['name']} ({row['city']})" for row in results],
            "fees": [row['entry_fee'] for row in results]
        }
        
        return jsonify(chart_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chart/package-prices', methods=['GET'])
def get_package_prices():
    """Get tour package prices for comparison"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.name, p.price, p.duration, d.name as city
            FROM packages p
            JOIN destinations d ON p.destination_id = d.id
            ORDER BY p.price ASC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        
        chart_data = {
            "labels": [row['name'] for row in results],
            "prices": [row['price'] for row in results],
            "durations": [row['duration'] for row in results],
            "cities": [row['city'] for row in results]
        }
        
        return jsonify(chart_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
# MAIN CHAT ENDPOINT WITH LLM
# ==========================================

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        language = data.get('language', 'en')
        use_ai = data.get('use_ai', True)  # Can be toggled from frontend
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        bot_response = ""
        chart_data = None
        
        # QUERY: List destinations
        if any(word in user_message for word in ['destination', 'place', 'city', 'cities', 'show me', 'list']):
            cursor.execute('SELECT * FROM destinations ORDER BY rating DESC')
            results = cursor.fetchall()
            
            if use_ai and should_use_ai(user_message):
                formatted_data = format_database_results_for_ai(results, "destinations")
                bot_response = get_smart_response(user_message, formatted_data, language)
            else:
                bot_response = "🏛️ **Top Destinations:**\n\n"
                for i, dest in enumerate(results, 1):
                    bot_response += f"{i}. **{dest['name']}** ⭐ {dest['rating']}/5\n"
                    bot_response += f"   {dest['description']}\n\n"
        
        # QUERY: Find hotels
        elif any(word in user_message for word in ['hotel', 'stay', 'accommodation']):
            cursor.execute('SELECT id, name FROM destinations')
            destinations = cursor.fetchall()
            
            destination_id = None
            for dest in destinations:
                if dest['name'].lower() in user_message:
                    destination_id = dest['id']
                    break
            
            if destination_id:
                cursor.execute('''
                    SELECT h.*, d.name as city
                    FROM hotels h
                    JOIN destinations d ON h.destination_id = d.id
                    WHERE h.destination_id = ?
                    ORDER BY h.rating DESC
                ''', (destination_id,))
            else:
                cursor.execute('''
                    SELECT h.*, d.name as city
                    FROM hotels h
                    JOIN destinations d ON h.destination_id = d.id
                    ORDER BY h.rating DESC
                    LIMIT 10
                ''')
            
            results = cursor.fetchall()
            
            if use_ai and should_use_ai(user_message):
                formatted_data = format_database_results_for_ai(results, "hotels")
                bot_response = get_smart_response(user_message, formatted_data, language)
                chart_data = {"type": "hotel-prices"}
            else:
                bot_response = "🏨 **Available Hotels:**\n\n"
                for i, hotel in enumerate(results, 1):
                    bot_response += f"{i}. **{hotel['name']}** - {hotel['city']}\n"
                    bot_response += f"   💰 ₹{hotel['price']}/night | ⭐ {hotel['rating']}/5\n\n"
        
        # QUERY: Show attractions
        elif any(word in user_message for word in ['attraction', 'visit', 'see', 'sightseeing']):
            cursor.execute('''
                SELECT a.*, d.name as city
                FROM attractions a
                JOIN destinations d ON a.destination_id = d.id
                ORDER BY a.entry_fee ASC
                LIMIT 15
            ''')
            
            results = cursor.fetchall()
            
            if use_ai and should_use_ai(user_message):
                formatted_data = format_database_results_for_ai(results, "attractions")
                bot_response = get_smart_response(user_message, formatted_data, language)
                chart_data = {"type": "attraction-prices"}
            else:
                bot_response = "🎯 **Tourist Attractions:**\n\n"
                for i, attr in enumerate(results, 1):
                    fee = "Free" if attr['entry_fee'] == 0 else f"₹{attr['entry_fee']}"
                    bot_response += f"{i}. **{attr['name']}** - {attr['city']}\n"
                    bot_response += f"   🎫 {fee} | ⏰ {attr['timing']}\n\n"
        
        # QUERY: Tour packages
        elif any(word in user_message for word in ['package', 'tour', 'trip', 'plan']):
            cursor.execute('''
                SELECT p.*, d.name as city
                FROM packages p
                JOIN destinations d ON p.destination_id = d.id
                ORDER BY p.price ASC
            ''')
            
            results = cursor.fetchall()
            
            if use_ai and should_use_ai(user_message):
                formatted_data = format_database_results_for_ai(results, "tour packages")
                bot_response = get_smart_response(user_message, formatted_data, language)
                chart_data = {"type": "package-prices"}
            else:
                bot_response = "📦 **Tour Packages:**\n\n"
                for i, pkg in enumerate(results, 1):
                    bot_response += f"{i}. **{pkg['name']}** - {pkg['city']}\n"
                    bot_response += f"   ⏱️ {pkg['duration']} | 💰 ₹{pkg['price']}\n\n"
        
        # QUERY: Budget-based
        elif any(word in user_message for word in ['cheap', 'budget', 'under', 'affordable']):
            words = user_message.split()
            price_limit = 2000
            for word in words:
                clean_word = word.replace(',', '').replace('₹', '').replace('rs', '')
                if clean_word.isdigit():
                    price_limit = int(clean_word)
                    break
            
            cursor.execute('''
                SELECT h.*, d.name as city
                FROM hotels h
                JOIN destinations d ON h.destination_id = d.id
                WHERE h.price <= ?
                ORDER BY h.price ASC
            ''', (price_limit,))
            
            results = cursor.fetchall()
            
            if use_ai:
                formatted_data = format_database_results_for_ai(results, "budget hotels")
                formatted_data += f"\nUser's budget limit: ₹{price_limit}"
                bot_response = get_smart_response(user_message, formatted_data, language)
            else:
                bot_response = f"🏨 **Hotels Under ₹{price_limit}:**\n\n"
                for i, hotel in enumerate(results, 1):
                    bot_response += f"{i}. {hotel['name']} - ₹{hotel['price']}\n"
        
        # Greeting
        elif any(word in user_message for word in ['hello', 'hi', 'hey', 'namaste']):
            bot_response = "👋 **Hello! I'm your AI-powered Rajasthan Tourism Assistant!**\n\n"
            bot_response += "🤖 Powered by Google Gemini AI\n"
            bot_response += "📊 Interactive Data Visualization\n\n"
            bot_response += "**Try asking:**\n"
            bot_response += "• 'Show me destinations'\n"
            bot_response += "• 'Recommend hotels in Jaipur'\n"
            bot_response += "• 'Compare hotel prices' (shows chart!)\n"
            bot_response += "• 'Plan a 3-day trip to Udaipur'\n"
        
        # Default with AI
        else:
            if use_ai:
                # Generic query - let AI handle it
                bot_response = get_smart_response(
                    user_message, 
                    "I'm a Rajasthan tourism assistant. I can help with hotels, attractions, and trip planning.",
                    language
                )
            else:
                bot_response = "I can help with destinations, hotels, attractions, and packages!"
        
        conn.close()
        
        return jsonify({
            "response": bot_response,
            "user_message": user_message,
            "language": language,
            "chart_data": chart_data,
            "ai_powered": use_ai and should_use_ai(user_message)
        })
    
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🏨 TOURISM CHATBOT - LLM + VISUALIZATION")
    print("=" * 70)
    print(f"📍 Server: http://localhost:5000")
    print(f"🗄️ Database: {DATABASE_FILE}")
    print(f"🤖 LLM: Google Gemini Pro")
    print(f"📊 Charts: Chart.js Ready")
    print("=" * 70)
    print("\n✅ Server starting...\n")
    app.run(debug=True, port=5000)