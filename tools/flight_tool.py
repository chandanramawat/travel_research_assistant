# tools/flight_tool.py
import os
import requests
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()


@tool
def search_flights(departure_id: str, arrival_id: str, outbound_date: str) -> str:
    """
    Search real flight prices using SerpApi's Google Flights engine.

    Args:
        departure_id: 3-letter IATA airport code for departure (e.g. DEL for Delhi, JDH for Jodhpur)
        arrival_id: 3-letter IATA airport code for arrival
        outbound_date: travel date in YYYY-MM-DD format
    """
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        return "Error: SerpApi key not configured."

    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "outbound_date": outbound_date,
        "type": "2",  # one-way — simpler and enough for a price estimate
        "currency": "INR",
        "hl": "en",
        "api_key": api_key,
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=15)
        data = response.json()

        if "error" in data:
            return f"Flight search error: {data['error']}"

        flights = data.get("best_flights") or data.get("other_flights") or []
        if not flights:
            return f"No flights found for {departure_id} to {arrival_id} on {outbound_date}."

        lines = []
        for group in flights[:5]:
            price = group.get("price", "N/A")
            duration = group.get("total_duration", "N/A")
            legs = group.get("flights", [])
            airline = legs[0].get("airline", "Unknown airline") if legs else "Unknown airline"
            stops = "Non-stop" if len(legs) == 1 else f"{len(legs) - 1} stop(s)"
            lines.append(f"{airline} — ₹{price} — {stops} — {duration} min total")

        return "\n".join(lines)

    except requests.exceptions.Timeout:
        return f"Flight search timed out for {departure_id} to {arrival_id}."
    except Exception as e:
        return f"Flight search error: {e}"