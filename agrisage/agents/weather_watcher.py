"""
Weather Watcher Agent (☀️ వాతావరణ మిత్రుడు)
Job: Reads temperature, rainfall, and humidity from Open-Meteo API.
Fallback: If offline or API fails, uses reliable realistic backup data.
Analogy: Like the village elder who steps outside, looks at the sky and clouds, and warns if rain is coming!
"""

import requests

class WeatherWatcher:
    def __init__(self):
        self.name = "Weather Watcher ☀️"
        # Fast lookup coordinates for popular Andhra / Telangana farming regions
        self.city_coordinates = {
            "hyderabad": (17.3850, 78.4867),
            "vijayawada": (16.5062, 80.6480),
            "guntur": (16.3067, 80.4365),
            "warangal": (17.9689, 79.5941),
            "kurnool": (15.8281, 78.0373),
            "tirupati": (13.6288, 79.4192),
            "karimnagar": (18.4386, 79.1288),
            "nizamabad": (18.6725, 78.0941),
            "rajahmundry": (17.0005, 81.8040),
            "khammam": (17.2473, 80.1514)
        }

    def get_weather(self, city_name: str = "Hyderabad") -> dict:
        """
        Fetches live weather or falls back to realistic mock weather data.
        Returns temperature, humidity, rain chance, and traffic-light status.
        """
        clean_city = (city_name or "Hyderabad").strip().lower()
        lat, lon = self.city_coordinates.get(clean_city, (17.3850, 78.4867))

        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m&timezone=auto"
            response = requests.get(url, timeout=3.0)
            if response.status_code == 200:
                data = response.json().get("current", {})
                temp = float(data.get("temperature_2m", 30.5))
                humidity = float(data.get("relative_humidity_2m", 65.0))
                rain = float(data.get("precipitation", 0.0))
                wind = float(data.get("wind_speed_10m", 10.0))
                source = "Live Open-Meteo API 🌐"
            else:
                temp, humidity, rain, wind, source = self._get_fallback_data(clean_city)
        except Exception:
            temp, humidity, rain, wind, source = self._get_fallback_data(clean_city)

        # Determine Traffic Light Status
        if rain > 15.0 or temp > 40.0:
            status = "red"
            summary_en = f"Severe Weather Alert! ({temp}°C, Rain: {rain}mm)"
            summary_te = f"తీవ్ర వాతావరణ హెచ్చరిక! (ఉష్ణోగ్రత: {temp}°C, వర్షం: {rain}మి.మీ)"
            advice_en = "Heavy rain/heat warning. Delay pesticide spraying and ensure drainage."
            advice_te = "భారీ వర్షం లేదా అధిక ఎండ హెచ్చరిక. మందుల పిచికారీ వాయిదా వేయండి, నీటి పారుదల చూడండి."
        elif temp > 34.0 or rain > 3.0:
            status = "yellow"
            summary_en = f"Warm / Light Rain Forecast ({temp}°C, Rain: {rain}mm)"
            summary_te = f"వేడి లేదా తేలికపాటి వర్షం సూచన ({temp}°C, వర్షం: {rain}మి.మీ)"
            advice_en = "Moderate weather. Water plants in early morning or evening to reduce evaporation."
            advice_te = "సాధారణ వేడి ఉంది. ఉదయం లేదా సాయంత్రం వేళల్లో మాత్రమే నీరు పెట్టండి."
        else:
            status = "green"
            summary_en = f"Ideal Crop Weather ({temp}°C, Humidity: {humidity}%)"
            summary_te = f"పంటలకు అనుకూలమైన వాతావరణం ({temp}°C, తేమ: {humidity}%)"
            advice_en = "Pleasant conditions. Excellent time for regular farm activities."
            advice_te = "వాతావరణం చాలా బాగుంది. సాధారణ వ్యవసాయ పనులకు అనువైన సమయం."

        return {
            "status": status,
            "city": city_name.capitalize() if city_name else "Local Farm",
            "temperature": temp,
            "humidity": humidity,
            "rainfall_mm": rain,
            "wind_speed": wind,
            "source": source,
            "summary_en": summary_en,
            "summary_te": summary_te,
            "advice_en": advice_en,
            "advice_te": advice_te
        }

    def _get_fallback_data(self, clean_city: str):
        """Reliable backup data for demo day when offline."""
        return 31.0, 62.0, 0.0, 8.5, "Safe Offline Backup Data 🛡️"

