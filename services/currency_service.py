import json
import requests
from datetime import datetime, timezone
from config.settings import EXCHANGE_API_URL
from services.crud.exchange_rate_service import read_last_updated_exchange_rate, create_exchange_rate

LOCAL_JSON = "resources/RON.json"

#Checks if current time is after the timestamp for the next update from the json file. If so, returns True.
def check_exchange_update(next_update):
    try:
        return datetime.now(timezone.utc).timestamp() >= next_update
    except Exception:
        return True     #Update exchange rates on exception for safety.

#Checks for the API URL and, afterward, for the corrects status code. If everything is correct, writes over LOCAL_JSON.
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

#Update exchange rates if needed
def update_exchange_rates():

    #Fetch last update timestamp from DB
    db_last_update = read_last_updated_exchange_rate()
    db_last_update = db_last_update[0] if db_last_update and db_last_update[0] else None

    #Load local JSON
    with open(LOCAL_JSON, "r", encoding="utf-8") as f:
        local_data = json.load(f)

    #Determine last updated time according to JSON
    last_update_unix = local_data.get("time_last_update_unix", 0)
    last_update_time = datetime.fromtimestamp(last_update_unix, timezone.utc)

    #Determine next update time
    next_update_unix = local_data.get("time_next_update_unix", 0)
    next_update_time = datetime.fromtimestamp(next_update_unix, timezone.utc)

    print(f"{db_last_update} {next_update_time}")

    #Skip update if not needed
    if db_last_update and next_update_time > db_last_update >= last_update_time:
        print(f"Exchange rates are already up-to-date. Last update {db_last_update}.")
        return False

    #Determine whether update necessary from local JSON or from the API.
    if check_exchange_update(next_update_unix):
        print("Fetching fresh exchange rates...")
        data = fetch_exchange_rates()
    else:
        print("Updating using local data.")
        data = local_data

    if not data or data.get("result") != "success":
        raise ValueError("Invalid exchange data!")

    #Base currency and conversion rates are memorized in data, last update timestamp as well.
    base = data["base_code"]
    rates = data["conversion_rates"]
    timestamp = datetime.fromtimestamp(data["time_last_update_unix"], timezone.utc)

    #Updates the rows and reports back how many it's updated.
    update_count = 0
    for currency_to, rate in rates.items():
        if currency_to == base:
            continue
        create_exchange_rate(base, currency_to, rate)
        update_count += 1

    print(f"{update_count} exchange rates updated successfully from {base} at {timestamp}.")
    return True