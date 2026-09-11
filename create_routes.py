import asyncio

import searoute as sr

from pprint import pprint

from reverse_geocoder import (
    get_addresses,
    get_origin_destination_coordinates
)


# ---------------------------------------------------------
# Sample route coordinates
# ---------------------------------------------------------

def sample_coordinates(
    coordinates,
    max_points=10
):

    if not coordinates:
        return []

    if len(coordinates) <= max_points:
        return coordinates

    # Always include first point
    # and last point.

    indexes = []

    for i in range(max_points):

        index = round(
            i * (len(coordinates) - 1)
            / (max_points - 1)
        )

        indexes.append(index)

    return [
        coordinates[index]
        for index in indexes
    ]


# ---------------------------------------------------------
# Calculate route
# ---------------------------------------------------------

async def get_route_between_origin_and_destination(
    origin_address,
    destination_address,
    max_address_points=10
):

    # -----------------------------------------------------
    # Geocode origin and destination
    # -----------------------------------------------------

    (
        origin_lat_lon,
        destination_lat_lon
    ) = await get_origin_destination_coordinates(
        origin_address,
        destination_address
    )

    if origin_lat_lon is None:

        raise ValueError(
            f"Could not geocode origin: "
            f"{origin_address}"
        )

    if destination_lat_lon is None:

        raise ValueError(
            f"Could not geocode destination: "
            f"{destination_address}"
        )

    print()
    print("Origin coordinates:")
    print(origin_lat_lon)

    print()

    print("Destination coordinates:")
    print(destination_lat_lon)

    # -----------------------------------------------------
    # searoute expects:
    #
    # [longitude, latitude]
    # -----------------------------------------------------

    origin = [
        origin_lat_lon["lon"],
        origin_lat_lon["lat"]
    ]

    destination = [
        destination_lat_lon["lon"],
        destination_lat_lon["lat"]
    ]

    print()
    print("Calculating sea route...")

    # -----------------------------------------------------
    # Calculate route
    # -----------------------------------------------------

    route = sr.searoute(
        origin,
        destination
    )

    # -----------------------------------------------------
    # Get route coordinates
    #
    # searoute returns:
    #
    # [longitude, latitude]
    # -----------------------------------------------------

    route_coordinates = (
        route.geometry.coordinates
    )

    print()
    print(
        f"Total route coordinates: "
        f"{len(route_coordinates)}"
    )

    # -----------------------------------------------------
    # Convert:
    #
    # [longitude, latitude]
    #
    # to:
    #
    # (latitude, longitude)
    #
    # because reverse geocoder expects lat/lon.
    # -----------------------------------------------------

    coordinates = []

    for lon, lat in route_coordinates:

        coordinates.append(
            (lat, lon)
        )

    # -----------------------------------------------------
    # Sample coordinates
    # -----------------------------------------------------

    sampled_coordinates = sample_coordinates(
        coordinates,
        max_points=max_address_points
    )

    print()
    print(
        f"Coordinates selected for "
        f"reverse geocoding: "
        f"{len(sampled_coordinates)}"
    )

    # -----------------------------------------------------
    # Reverse geocode sampled coordinates
    # -----------------------------------------------------

    addresses = await get_addresses(
        sampled_coordinates
    )

    # -----------------------------------------------------
    # Combine coordinate + address
    # -----------------------------------------------------

    route_addresses = []

    for coordinate, address in zip(
        sampled_coordinates,
        addresses
    ):

        lat, lon = coordinate

        route_addresses.append(
            {
                "lat": lat,
                "lon": lon,
                "address": address
            }
        )

    # -----------------------------------------------------
    # Return result
    # -----------------------------------------------------

    return {

        "two_way_distance": {

            "origin_to_destination": {            

                "addresses": route_addresses
            }
        }
    }


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

async def main():

    origin_address = "Boston"

    destination_address = "India"

    result = (
        await get_route_between_origin_and_destination(
            origin_address,
            destination_address,
            max_address_points=10
        )
    )
    return result


# ---------------------------------------------------------
# Run
# ---------------------------------------------------------

if __name__ == "__main__":

    asyncio.run(main())