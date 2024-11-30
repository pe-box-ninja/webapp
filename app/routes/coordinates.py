
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError

geolocator = Nominatim(user_agent="webapp-main")

def get_coordinates(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"Geocoding failed for address: {address}")
    except GeopyError as e:
        print(f"GeopyError: {str(e)}")
    return None, None

