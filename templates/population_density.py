import requests

base_url = "api.geonames.org/findNearbyPlaceName?"
username = "mythreya_kesavan"  # Replace with your GeoNames username
endpoint = "findNearbyPlaceNameJSON"
location = "New York"  # Replace with the location you want to get population density for

url = f"{base_url}{endpoint}?q={location}&maxRows=1&username={username}"
response = requests.get(url)
print(response)
if response.status_code == 200:
    data = response.json()
    print(data)
    if "geonames" in data and len(data["geonames"]) > 0:
        population_density = data["geonames"][0]["populationDensity"]
        print(f"Population Density: {population_density}")
    else:
        print("No data found for the location.")
else:
    print("Error occurred while accessing the API.")

