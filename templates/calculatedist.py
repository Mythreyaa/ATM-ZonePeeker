import requests
from geopy.geocoders import Nominatim


def calculate_distance(origin,destination):
    geolocator = Nominatim(user_agent="atm_locator")
    location = geolocator.geocode(origin)
    origin = (location.latitude,location.longitude)
    location = geolocator.geocode(destination)
    destination = (location.latitude,location.longitude)

    url = f"http://router.project-osrm.org/route/v1/driving/{origin[1]},{origin[0]};{destination[1]},{destination[0]}?overview=false"
    response = requests.get(url)
    data = response.json()

    if 'routes' in data and len(data['routes']) > 0:
        distance = data['routes'][0]['distance']
        return distance / 1000 #in KM
    else:
        return None
    
