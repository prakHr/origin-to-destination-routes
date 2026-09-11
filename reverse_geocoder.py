import aiohttp
import asyncio


NOMINATIM_URL = "https://nominatim.openstreetmap.org"

HEADERS = {
    "User-Agent": "create-routes/1.0"
}

# Public Nominatim should not be hammered with requests.
REQUEST_DELAY = 1.1


# ---------------------------------------------------------
# Forward geocoding
# Address -> latitude / longitude
# ---------------------------------------------------------

async def geocode_address(session, address):

    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "addressdetails": 1
    }

    try:

        async with session.get(
            f"{NOMINATIM_URL}/search",
            params=params,
            headers=HEADERS
        ) as response:

            if response.status != 200:
                print(
                    f"Geocoding failed for {address}: "
                    f"HTTP {response.status}"
                )
                return None

            data = await response.json()

            if not data:
                print(f"Could not geocode: {address}")
                return None

            return {
                "lat": float(data[0]["lat"]),
                "lon": float(data[0]["lon"])
            }

    except Exception as e:

        print(
            f"Error while geocoding "
            f"{address}: {e}"
        )

        return None


# ---------------------------------------------------------
# Reverse geocoding
# latitude / longitude -> address
# ---------------------------------------------------------

async def get_address(
    session,
    lat,
    lon
):

    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "zoom": 18,
        "addressdetails": 1
    }

    try:

        async with session.get(
            f"{NOMINATIM_URL}/reverse",
            params=params,
            headers=HEADERS
        ) as response:

            if response.status != 200:

                print(
                    f"Reverse geocoding failed "
                    f"for ({lat}, {lon}): "
                    f"HTTP {response.status}"
                )

                return None

            data = await response.json()

            return data.get("display_name")

    except Exception as e:

        print(
            f"Error while reverse geocoding "
            f"({lat}, {lon}): {e}"
        )

        return None


# ---------------------------------------------------------
# Multiple reverse geocoding requests
# ---------------------------------------------------------

async def get_addresses(coordinates):

    addresses = []

    async with aiohttp.ClientSession() as session:

        for index, (lat, lon) in enumerate(
            coordinates,
            start=1
        ):

            print(
                f"Reverse geocoding "
                f"{index}/{len(coordinates)}: "
                f"{lat}, {lon}"
            )

            address = await get_address(
                session,
                lat,
                lon
            )

            addresses.append(address)

            # Respect Nominatim rate limit
            if index < len(coordinates):
                await asyncio.sleep(
                    REQUEST_DELAY
                )

    return addresses


# ---------------------------------------------------------
# Geocode origin and destination
# ---------------------------------------------------------

async def get_origin_destination_coordinates(
    origin_address,
    destination_address
):

    async with aiohttp.ClientSession() as session:

        print(
            f"Geocoding origin: "
            f"{origin_address}"
        )

        origin = await geocode_address(
            session,
            origin_address
        )

        await asyncio.sleep(
            REQUEST_DELAY
        )

        print(
            f"Geocoding destination: "
            f"{destination_address}"
        )

        destination = await geocode_address(
            session,
            destination_address
        )

    return origin, destination