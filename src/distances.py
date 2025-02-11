from haversine import haversine, Unit
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def get_coordinates(city):
    geolocator = Nominatim(user_agent="distance_calculator")
    location = geolocator.geocode(city)
    if location is None:
        return None
    return location.latitude, location.longitude

def calculate_distance(city1, city2):
    coordinates1 = get_coordinates(city1)
    coordinates2 = get_coordinates(city2)
    
    if coordinates1 is None or coordinates2 is None:
        return 100000
    
    distance = haversine(coordinates1, coordinates2, unit=Unit.KILOMETERS)
    return distance
