import requests
from geopy.geocoders import Nominatim

def calculate_distance(origin,destination):
    geolocator = Nominatim(user_agent="atm_locator")
    location = geolocator.geocode(origin)
    origin = (location.latitude,location.longitude)
    print("Origin: ",origin)
    location = geolocator.geocode(destination)
    destination = (location.latitude,location.longitude)
    print("destination: ",destination)
    url = f"http://router.project-osrm.org/route/v1/driving/{origin[1]},{origin[0]};{destination[1]},{destination[0]}?overview=false"
    response = requests.get(url)
    data = response.json()

    if 'routes' in data and len(data['routes']) > 0:
        distance = data['routes'][0]['distance']
        print("Distance: ",distance / 1000)
        return distance / 1000 #in KM
    else:
        return None
    
def check_others(location, radius):
    base_url = "https://nominatim.openstreetmap.org/"
    geocode_params = {
        "q": location,
        "format": "json",
        "limit": 1
    }
    geocode_url = base_url + "search"
    geocode_response = requests.get(geocode_url, params=geocode_params)
    geocode_data = geocode_response.json()

    if geocode_response.status_code == 200 and geocode_data:
        latitude = geocode_data[0]["lat"]
        longitude = geocode_data[0]["lon"]

        # Step 2: Search for shopping malls using Overpass API
        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = f"""
            [out:json];
            node["shop"="mall"](around:{radius},{latitude},{longitude});
            out;
        """
        overpass_params = {
            "data": overpass_query
        }
        overpass_response = requests.post(overpass_url, data=overpass_params)
        overpass_data = overpass_response.json()
        nearbyothers = 0

        if overpass_response.status_code == 200:
            malls_and_theaters = []
            for element in overpass_data["elements"]:
                print(element["tags"])
                if element["tags"].get("name"):
                    malls_and_theaters.append(element["tags"]["name"])

            if malls_and_theaters:
                print("Nearby Shopping Malls and Theaters:")
                for item in malls_and_theaters:
                    nearbyothers += 1
                    print(item)
                print("NEARBY OTHERS: ",nearbyothers)
            else:
                print("No shopping malls found nearby.")
        else:
            print("Error occurred while accessing the Overpass API.")
    else:
        print("Error occurred while geocoding the location.")

    return nearbyothers



def check_existing_atms(latitude, longitude, radius):
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json];
    (
      node["amenity"="atm"](around:{radius},{latitude},{longitude});
    );
    out center;
    """
    print("test")
    response = requests.get(overpass_url, params={'data': query})
    print(response)
    data = response.json()
    nearbyatms = 0
    
    if data.get('elements') and len(data['elements']) > 0:
       #print(data.get('elements'))
        for data in data.get('elements'):
            print(data['tags'])
            nearbyatms += 1
        print("NEARBY: ",nearbyatms)       
    return nearbyatms

def check_population_density(pop_dens,population_threshold):
    return abs(pop_dens - population_threshold) 

def find_potential_location(address, population_threshold, radius,bankname):
    geolocator = Nominatim(user_agent="atm_locator")
    location = geolocator.geocode(address)
    
    if location is None:
        print("Invalid address.")
        return None
    
    latitude = location.latitude
    longitude = location.longitude
    
    #check_others(address,radius)
    print("1...")
    check_existing_atms(latitude, longitude, radius)
    print("2...")
    #check_population_density(latitude, longitude, population_threshold)
    
    return latitude, longitude

if __name__ == "__main__":
    address = "Porur"
    population_threshold = 10000  
    radius = 3000  
    bankname = "My bank"

    potential_location = find_potential_location(address, population_threshold, radius,bankname)

