# app.py
from flask import Flask, render_template, request, jsonify
from functions import get_chatbot_response, handle_user_preferences, fetch_hotels, fetch_activities,fetch_flight_cheapest

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('conversation_bot.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form['user_input']
    user_id = request.form['user_id']  # Assume user_id is passed from the frontend
    response = get_chatbot_response(user_input, user_id)
    return jsonify({'response': response})

@app.route('/preferences', methods=['POST'])
def preferences():
    user_id = request.form['user_id']
    preferences = request.form['preferences']  # Assume preferences are sent as JSON
    handle_user_preferences(user_id, preferences)
    return jsonify({'status': 'Preferences updated'})

@app.route('/hotels', methods=['POST'])
def hotels():
    destination = request.form['destination']
    hotels = fetch_hotels(destination)
    return jsonify({'hotels': hotels})

@app.route('/activities', methods=['POST'])
def activities():
    destination = request.form['destination']
    activities = fetch_activities(destination)
    return jsonify({'activities': activities})

@app.route('/flights', methods=['POST'])
def flights():
    origin = request.form['origin']
    destination = request.form['destination']
    flights = fetch_flight_cheapest(origin,destination)
    return jsonify({'flights': flights})

if __name__ == '__main__':
    app.run(debug=True)