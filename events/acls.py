from .keys import PEXELS_API_KEY
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
    # Make the request
    # Parse the JSON response
    # Get the latitude and longitude from the response

    # Create the URL for the current weather API with the latitude
    #   and longitude
    # Make the request
    # Parse the JSON response
    # Get the main temperature and the weather's description and put
    #   them in a dictionary
    # Return the dictionary
    pass
