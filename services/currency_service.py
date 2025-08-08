import json
import requests
from datetime import datetime, timezone
from config.settings import EXCHANGE_API_URL
from db.connection import get_connection

LOCAL_JSON = "resources/RON.json"

def check_exchange_update(local_file=LOCAL_JSON):
    try:
        with open(local_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        next_update = data.get("time_next_update_unix", 0)
        return datetime.now(timezone.utc).timestamp() >= next_update
    except Exception:
        return True

def fetch_exchange_rates():
    if not EXCHANGE_API_URL:
        raise ValueError("Exchange API URL not configured!")
    response = requests.get(EXCHANGE_API_URL)
    if response.status_code != 200:
        raise ConnectionError("Failed to fetch exchange rates from API!")
    data = response.json()
    with open (LOCAL_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return data

def update_exchange_rates():
    data = None
    if check_exchange_update():
        print("Fetching fresh exchange rates...")
        data = fetch_exchange_rates()
    else:
        print("Using local exchange rates...")
        with open(LOCAL_JSON, "r", encoding="utf-8") as f:
            data=json.load(f)
    if data is None or data["result"] != "success":
        raise ValueError("Invalid exchange data!")

    base = data["base_code"]
    rates = data["conversion_rates"]
    timestamp = datetime.fromtimestamp(data["time_last_update_unix"], timezone.utc)

    with get_connection() as conn:
        with conn.cursor() as cur:
            for currency_to, rate in rates.items():
                if currency_to == base:
                    continue
                cur.execute("""
                    INSERT INTO exchange_rates (currency_from, currency_to, rate)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (currency_from, currency_to)
                    DO UPDATE SET rate = EXCLUDED.rate;
                """, (base, currency_to, rate))
        conn.commit()

    print(f"Exchange rates updated successfully from {base} at {timestamp}.")