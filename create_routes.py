from geopy.geocoders import Nominatim
import searoute as sr
from pprint import pprint
import time


# ---------------------------------------------------------
# Nominatim configuration
# ---------------------------------------------------------

geolocator = Nominatim(
    user_agent="create_routes/1.0",
    timeout=30
)


# ---------------------------------------------------------
# Geocode address
# ---------------------------------------------------------

def get_lat_lon_from_address(address):
    location = geolocator.geocode(address)

    if location is None:
        raise ValueError(
            f"Could not geocode address: {address}"
        )

    return {
        "lat": location.latitude,
        "lon": location.longitude
    }


# ---------------------------------------------------------
# Calculate route
# ---------------------------------------------------------

def get_route_between_origin_and_destination(
    origin_address,
    destination_address
):
    # Geocode origin
    origin_lat_lon = get_lat_lon_from_address(
        origin_address
    )

    # Small delay between Nominatim requests
    time.sleep(1.2)

    # Geocode destination
    destination_lat_lon = get_lat_lon_from_address(
        destination_address
    )

    # IMPORTANT:
    # searoute expects [longitude, latitude]
    origin = [
        origin_lat_lon["lon"],
        origin_lat_lon["lat"]
    ]

    destination = [
        destination_lat_lon["lon"],
        destination_lat_lon["lat"]
    ]

    
    # Origin -> Destination
    route = sr.searoute(
        origin,
        destination
    )

    
    return {
        "two_way_distance": {
            "origin_to_destination": route
            
        }
    }


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    origin_address = "Taj Mahal, Agra, Uttar Pradesh 282001"

    destination_address = "Bits Hyderabad Pilani"
    
    two_way_route = get_route_between_origin_and_destination(
        origin_address,
        destination_address
    )

    pprint(two_way_route)