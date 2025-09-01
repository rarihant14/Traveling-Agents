import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

def get_destination_id(city_name: str, locale: str = "en-gb"):
    """
    Get the Booking.com destination ID (dest_id) for a city.
    """
    url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"
    querystring = {"name": city_name, "locale": locale}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            return data[0].get("dest_id")  # pick the first match
        else:
            return None
    except Exception:
        return None


def get_hotel_availability(city_name: str, checkin, checkout, currency: str = "USD", locale: str = "en-gb"):
    """
    Fetch available hotels from Booking.com RapidAPI by city name.
    Always returns a list of dicts with keys: name, price, rating.
    """

    dest_id = get_destination_id(city_name, locale)
    if not dest_id:
        return [{"name": f"Could not find destination for {city_name}", "price": "N/A", "rating": "N/A"}]

    url = "https://booking-com.p.rapidapi.com/v1/hotels/search"
    querystring = {
        "order_by": "popularity",
        "adults_number": "1",
        "checkin_date": str(checkin),
        "checkout_date": str(checkout),
        "units": "metric",
        "room_number": "1",
        "dest_type": "city",
        "locale": locale,
        "currency": currency,
        "dest_id": dest_id
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        data = response.json()

        hotels_list = []
        if isinstance(data, dict) and "result" in data:
            for h in data["result"][:10]:  # top 10 hotels
                hotels_list.append({
                    "name": h.get("hotel_name", "Unknown"),
                    "price": h.get("price_breakdown", {}).get("gross_price", "N/A"),
                    "rating": h.get("review_score", "N/A")
                })
        else:
            hotels_list.append({
                "name": "No results found",
                "price": "N/A",
                "rating": "N/A"
            })

        return hotels_list

    except Exception as e:
        return [{
            "name": "Error",
            "price": "N/A",
            "rating": str(e)
        }]


if __name__ == "__main__":
    # Example usage
    sample_hotels = get_hotel_availability("Paris", "2025-09-10", "2025-09-12")
    print(sample_hotels)
