"""
LLM Helper Module - Google Gemini Integration
Handles all AI-powered responses
"""

import google.generativeai as genai
import json

# ⚠️ REPLACE THIS WITH YOUR ACTUAL API KEY!
GEMINI_API_KEY = "AIzaSyBjQ70-1GcX_QSu0d5Ngr-CP3QWWcZrIVo"

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model
model = genai.GenerativeModel('gemini-pro')

def get_smart_response(user_message, database_results, language='en'):
    """
    Generate intelligent response using Gemini AI
    
    Args:
        user_message: What the user asked
        database_results: Data from database
        language: User's selected language
    
    Returns:
        AI-generated response
    """
    
    # Build context for AI
    context = f"""
You are a helpful Rajasthan tourism assistant chatbot. 
User's language preference: {language}
User asked: "{user_message}"

Here is relevant data from our database:
{database_results}

Instructions:
1. Be friendly and conversational
2. Use the database data to give specific recommendations
3. Include prices, ratings, and practical details
4. Keep responses concise but informative
5. Use emojis appropriately (🏨🎯💰⭐)
6. Format response with clear sections
7. End with a helpful suggestion or question

Generate a natural, helpful response.
"""
    
    try:
        # Call Gemini AI
        response = model.generate_content(context)
        return response.text
    
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        # Fallback to basic response if AI fails
        return f"Based on your query, here's what I found:\n\n{database_results}\n\nWould you like more details?"


def generate_trip_plan(destination, duration, budget, hotels_data, attractions_data):
    """
    Generate personalized trip itinerary using AI
    
    Args:
        destination: City name
        duration: Number of days
        budget: Total budget in INR
        hotels_data: List of available hotels
        attractions_data: List of attractions
    
    Returns:
        Day-by-day itinerary
    """
    
    prompt = f"""
Create a detailed {duration}-day trip itinerary for {destination}, Rajasthan.
Budget: ₹{budget}
User wants a practical, day-by-day plan.

Available Hotels:
{hotels_data}

Available Attractions:
{attractions_data}

Create an itinerary with:
- Day-by-day breakdown
- Morning/Afternoon/Evening activities
- Hotel recommendation within budget
- Estimated costs for each day
- Practical tips (timing, transport)
- Total cost calculation

Format with clear sections and emojis. Keep it realistic and budget-conscious.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        print(f"❌ Trip planning error: {e}")
        return f"I can help you plan your {duration}-day trip to {destination}! Let me know what you'd like to explore."


def analyze_and_compare(data_type, data_list):
    """
    Use AI to analyze and compare options
    
    Args:
        data_type: What kind of data (hotels, attractions, etc.)
        data_list: List of items to compare
    
    Returns:
        AI analysis with recommendations
    """
    
    prompt = f"""
Analyze these {data_type} and provide helpful insights:

{data_list}

Provide:
1. Best value for money option
2. Luxury/Premium option
3. Budget-friendly option
4. Key differences between options
5. Recommendation based on different traveler types

Keep it concise and use bullet points. Use emojis for clarity.
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return "Here are the available options. Each has unique features!"


def format_database_results_for_ai(results, result_type):
    """
    Format database results into readable text for AI
    
    Args:
        results: Raw database results
        result_type: Type of data (hotels, attractions, etc.)
    
    Returns:
        Formatted string
    """
    
    if not results:
        return f"No {result_type} found."
    
    formatted = f"\n{result_type.upper()}:\n"
    
    for i, item in enumerate(results, 1):
        formatted += f"\n{i}. "
        for key, value in dict(item).items():
            if value and key not in ['id', 'destination_id']:
                formatted += f"{key}: {value}, "
        formatted = formatted.rstrip(', ') + "\n"
    
    return formatted


def should_use_ai(user_message):
    """
    Decide if we should use AI or simple database response
    
    Args:
        user_message: User's input
    
    Returns:
        Boolean - True if should use AI
    """
    
    # Use AI for complex queries
    ai_keywords = [
        'recommend', 'suggest', 'best', 'compare', 'advice', 
        'plan', 'trip', 'itinerary', 'help me', 'which',
        'better', 'worth', 'should i', 'romantic', 'family',
        'honeymoon', 'budget', 'cheap vs expensive', 'tell me about'
    ]
    
    return any(keyword in user_message.lower() for keyword in ai_keywords)


# Test function
if __name__ == "__main__":
    print("🧪 Testing Gemini Integration...")
    
    test_message = "Recommend a good hotel in Jaipur"
    test_data = "Hotel Raj Palace: ₹2500/night, 4.2 rating"
    
    response = get_smart_response(test_message, test_data)
    print(f"\n✅ AI Response:\n{response}")
    
    print("\n✅ LLM Helper is working!")