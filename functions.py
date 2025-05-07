# functions.py
import openai
import os
import requests
from amadeus import Client, ResponseError
from user_profiles import update_user_profile, get_user_profile
# from travel_api import get_hotels, get_activities




# Path to the API key file
api_key_path = "test_key.txt"  # No need for the full path

try:
    with open(api_key_path, 'r') as file:
        openai.api_key = file.read().strip()
except FileNotFoundError:
    print(f"API key file not found at: {api_key_path}. Please ensure the file exists.")
    raise


# Initialize the Amadeus client with your API credentials
amadeus = Client(
    client_id='xyz',  # Replace with your actual API Key
    client_secret='xyz'  # Replace with your actual API Secret
)

def get_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": 'xyz',
        "client_secret": 'xyz'
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Error getting access token: {response.status_code} - {response.text}")
        return None
    
def get_chatbot_response(user_input, user_id):
    # Check user profile for preferences
    user_profile = get_user_profile(user_id)
    
     # Determine if the user is asking for hotels
    if "hotel" in user_input.lower() or "search for hotels" in user_input.lower():
        destination = extract_destination(user_input)  # Implement this function to extract destination
        hotels = fetch_hotels(destination)  # Use the city code extracted from the destination
        
        if hotels:
            hotel_list = []
            for hotel in hotels:
                hotel_name = hotel['name']  # Assuming the hotel data has a 'name' field
                hotel_info = f"{hotel_name}"  # You can add more details if available
                hotel_list.append(hotel_info)
            return f"Here are some hotels in {destination}: {', '.join(hotel_list)}."
        else:
            return f"Sorry, I couldn't find any hotels in {destination}."

    # Determine if the user is asking for activities
    elif "activities" in user_input.lower() or "things to do" in user_input.lower():
        destination = extract_destination(user_input)  # Implement this function to extract destination
        activities = fetch_activities(destination)  # Call the modified function
        if activities:
            return f"Here are some activities in {destination}: {', '.join(activities)}."
        else:
            return f"Sorry, I couldn't find any activities in {destination}."
        
    # Determine if the user is asking for flights
     # Determine if the user is asking for flights
    elif "flights" in user_input.upper() or "search for flights" in user_input.upper():
        
        destination = extract_destination(user_input)
        flights = fetch_flight_cheapest(destination)
        if flights:
            flight_list = []
            for flight in flights:
                #flight_info = f"Destination: {flight['destination']}, Price: {flight['price']['total']} EUR"
                flight_list.append(flight)
            return f"Here are some flights from {destination}:\n" + "\n".join(flight_list)
        else:
            return f"Sorry, I couldn't find any flights from {destination}."

    # Default response if no specific request is found
    prompt = f"User preferences: {user_profile}. User input: {user_input}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def handle_user_preferences(user_id, preferences):
    update_user_profile(user_id, preferences)

def fetch_hotels(city_code):
    try:
        # Get list of hotels by city code
        response = amadeus.reference_data.locations.hotels.by_city.get(cityCode=city_code)
        
        # Check if the response contains data
        if response.data:
            return response.data  # Return the list of hotels
        else:
            return f"Sorry, I couldn't find any hotels in {city_code}."
    except ResponseError as error:
        print(f"Error fetching hotels: {error}")
        return None

def fetch_activities(destination):
    # Define the prompt for ChatGPT
    prompt = f"Suggest some activities to do in {destination}."

    try:
        # Call the OpenAI API to get activity suggestions
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the activities from the response
        activities = response['choices'][0]['message']['content'].strip().split('\n')
        
        # Clean up the activities list to remove any empty strings
        activities = [activity for activity in activities if activity]
        
        return activities  # Return the list of activities as strings
    except Exception as e:
        print(f"Error fetching activities: {e}")
        return []
    
def fetch_flight_cheapest(destination):
    try:
        response = amadeus.airline.destinations.get(airlineCode=destination)
        return response.data  # Return the data from the response
    except ResponseError as error:
        print(f"Error fetching flight routes: {error}")
        return None
    
# def extract_destination(user_input):
#     # Implement a simple extraction logic or use NLP to identify the destination
#     # For example, you can use regex or keyword matching
#     # This is a placeholder implementation
#     keywords = ["in ", "to ", "for "]
#     for keyword in keywords:
#         if keyword in user_input.lower():
#             return user_input.split(keyword)[-1].strip()
#     return "unknown destination"

def extract_origin(user_input):
    # Implement a simple extraction logic or use NLP to identify the destination
    # For example, you can use regex or keyword matching
    # This is a placeholder implementation
    keywords = ["in ", "to ", "for ", "from "]
    for keyword in keywords:
        if keyword in user_input.lower():
            return user_input.split(keyword)[-1].strip()
    return "unknown origin"

def extract_destination(user_input):
    # Implement a simple extraction logic or use NLP to identify the destination
    keywords = ["to ", "going to ", "destination ","in","at"]
    for keyword in keywords:
        if keyword in user_input.lower():
            return user_input.split(keyword)[-1].strip()
    return "unknown destination"