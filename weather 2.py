import json
import urllib.request
import urllib.parse
import urllib.error


def get_weather(location):
    """
    Fetches current weather data for the given location using wttr.in.
    Returns a dict with weather info, or None if it fails.
    """
    encoded_location = urllib.parse.quote(location)
    url = f"https://wttr.in/{encoded_location}?format=j1"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data
    except urllib.error.HTTPError as e:
        print(f"Error: Could not fetch weather (HTTP {e.code}). Check the location name.")
    except urllib.error.URLError:
        print("Error: No internet connection or weather service unavailable.")
    except json.JSONDecodeError:
        print("Error: Received invalid response from weather service.")
    return None


def display_weather(data, location):
    """Prints formatted weather information from the API response."""
    try:
        current = data["current_condition"][0]
        area = data["nearest_area"][0]

        city = area["areaName"][0]["value"]
        region = area["region"][0]["value"]
        country = area["country"][0]["value"]

        temp_c = current["temp_C"]
        temp_f = current["temp_F"]
        feels_like_c = current["FeelsLikeC"]
        humidity = current["humidity"]
        condition = current["weatherDesc"][0]["value"]
        wind_speed = current["windspeedKmph"]
        wind_dir = current["winddir16Point"]
        pressure = current["pressure"]
        visibility = current["visibility"]

        print("\n" + "=" * 40)
        print(f"  Weather for {city}, {region}, {country}")
        print("=" * 40)
        print(f"  Condition     : {condition}")
        print(f"  Temperature   : {temp_c}°C ({temp_f}°F)")
        print(f"  Feels Like    : {feels_like_c}°C")
        print(f"  Humidity      : {humidity}%")
        print(f"  Wind          : {wind_speed} km/h, {wind_dir}")
        print(f"  Pressure      : {pressure} hPa")
        print(f"  Visibility    : {visibility} km")
        print("=" * 40 + "\n")

    except (KeyError, IndexError):
        print(f"Could not parse weather data for '{location}'. Try a different location name or ZIP code.")


def main():
    print("=" * 40)
    print("       COMMAND-LINE WEATHER APP")
    print("=" * 40)
    

    while True:
        location = input("Enter location: ").strip()

        if location.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        if not location:
            print("Please enter a valid location.\n")
            continue

        print(f"\nFetching weather for '{location}'...")
        data = get_weather(location)

        if data:
            display_weather(data, location)


if __name__ == "__main__":
    main()