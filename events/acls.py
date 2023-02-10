from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import json
import requests


# Use the Pexels API
def get_photo(city, state):
    # Create a dictionary for the headers to use in the request
    headers = {"Authorization": PEXELS_API_KEY}
    # Create the URL for the request with the city and state
    params = {"per_page": 1, "query": city + " " + state}
    url = "https://api.pexels.com/v1/search"
    # Make the request
    response = requests.get(url, headers=headers, params=params)
    # Parse the JSON response
    content = json.loads(response.content)
    # Return a dictionary that contains a `picture_url` key and
    #   one of the URLs for one of the pictures in the response
    try:
        return {"picture_url": content["photos"][0]["src"]["original"]}
    except:
        return {"picture_url": None}


result = get_photo("Irvine", "CA")
print(result)


# Use the Open Weather API
def get_weather_data(city, state):
    # Create the URL for the geocoding API with the city and state
    iso_country_code = "ISO 3166-2:US"
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{iso_country_code}&limit=1&appid={OPEN_WEATHER_API_KEY}"
    # Make the request
    geo_response = requests.get(geo_url)
    # Parse the JSON response
    geo_content = json.loads(geo_response.content)
    # Get the latitude and longitude from the response
    lat = geo_content[0]["lat"]
    lon = geo_content[0]["lon"]

    # Create the URL for the current weather API with the latitude
    #   and longitude
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_API_KEY}"
    # Make the request
    weather_response = requests.get(weather_url)
    # Parse the JSON response
    weather_content = json.loads(weather_response.content)
    # Get the main temperature and the weather's description and put
    #   them in a dictionary
    weather_data = {
        "temp": weather_content["main"]["temp"],
        "description": weather_content["weather"][0]["description"],
    }
    # Return the dictionary
    try:
        return weather_data
    except:
        return {"temp": None, "description": None}
