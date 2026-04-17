import time
import requests
import math

# ------------------------------
# Rescue areas with specific range for each alert type
rescue_areas = [
    {"name": "Rescue Center A", "lat": 12.9716, "lon": 77.5946, "types": ["Building collapse"], "range_km": 5},
    {"name": "Rescue Center B", "lat": 12.9352, "lon": 77.6245, "types": ["Landslide"], "range_km": 10},
    {"name": "Rescue Center C", "lat": 12.9862, "lon": 77.5831, "types": ["Flood"], "range_km": 8},
]
# ------------------------------

# ------------------------------
# Helper functions
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c  # Distance in km

def nearest_rescue_by_type(lat, lon, alert_type):
    nearest = None
    min_distance = float('inf')
    for area in rescue_areas:
        if alert_type in area["types"]:
            distance = haversine(lat, lon, area["lat"], area["lon"])
            if distance <= area["range_km"] and distance < min_distance:
                min_distance = distance
                nearest = {"name": area["name"], "distance": distance}
    return nearest
# ------------------------------

class Server:
    def __init__(self):
        self.received = 0
        self.log = []
        # Your Telegram bot details
        self.bot_token = "8373892671:AAEIEUBRzW8s2B0dagfmUENaprmgWajcNvY"   # your bot token
        self.chat_id = "7428351097"       # your chat ID

    def process_message(self, data):
        self.received += 1
        self.log.append(data)

        # Node coordinates
        node_lat = data.get("lat", 12.9750)
        node_lon = data.get("lon", 77.5900)
        alert_type = data.get("msg", "")  # type of alert

        nearest = nearest_rescue_by_type(node_lat, node_lon, alert_type)

        # Compose message
        msg_text = f"🚨 ALERT from {data['id']}: {data['msg']}"
        if nearest:
            msg_text += f"\nNearest Rescue Area: {nearest['name']} ({nearest['distance']:.1f} km)"
        else:
            msg_text += "\nNo suitable rescue area in range."

        print(f"[SERVER] ✅ {msg_text} at {time.strftime('%H:%M:%S')}")

        # Send to Telegram
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": msg_text}
        try:
            r = requests.get(url, params=payload)
            print(r.json())  # Telegram API response
        except Exception as e:
            print(f"[SERVER] ❌ Failed to send Telegram message: {e}")
