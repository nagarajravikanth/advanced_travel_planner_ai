# travel_api.py
import requests

# Amadeus API credentials
AMADEUS_API_KEY = 'KGOBCxFdup5Sx6ZbCeRF4OygADQbQ7tL'  # Replace with your actual API Key
AMADEUS_API_SECRET = 'q4cQeCHv6N438hV8'  # Replace with your actual API Secret

def get_access_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = "grant_type=client_credentials&client_id=KGOBCxFdup5Sx6ZbCeRF4OygADQbQ7tL&client_secret=q4cQeCHv6N438hV8"
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Error getting access token: {response.status_code} - {response.text}")
        return None

# def get_hotels(destination):
#     access_token = get_access_token()
#     if not access_token:
#         return []

#     # Ensure the destination is a valid city code
#     url = f'https://test.api.amadeus.com/v2/shopping/hotel-offers?cityCode={destination}'
#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }
    
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         return response.json()['data']  # Return the list of hotel offers
#     else:
#         print(f"Error fetching hotels: {response.status_code} - {response.text}")
#         return []

# def get_cheapest_flight(origin,destination):
#     access_token = get_access_token()
#     if not access_token:
#         return {}

#     # Make the API call to fetch flight destinations
#     url = f"https://test.api.amadeus.com/v1/shopping/flight-destinations?origin=MAD&departureDate=2020-07-24,2021-01-19&oneWay=false&duration=1,15&nonStop=false&viewBy=DURATION"
#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }
    
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         return response.json()  # Return the JSON response if successful
#     else:
#         print(f"Error fetching flight destinations: {response.status_code} - {response.text}")
#         return {}

# def get_activities(destination):
#     access_token = get_access_token()
#     if not access_token:
#         return []

#     # Replace with the actual endpoint for activities
#     url = f'https://test.api.amadeus.com/v1/activities?cityCode={destination}'
#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }
    
#     response = requests.get(url, headers=headers)
    
#     if response.status_code == 200:
#         return response.json()['data']  # Return the list of activities
#     else:
#         print(f"Error fetching activities: {response.status_code} - {response.text}")
#         return []
    
    