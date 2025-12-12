import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

USAGE_FILE = "gemini_usage.json"
MAX_RPM = int(os.getenv("MAX_RPM", 6))
MAX_RPD = int(os.getenv("MAX_RPD", 15))

_last_request_time = 0


def get_daily_count():
    """Reads the daily usage count from the file. Resets if the date has changed."""
    today = datetime.now().strftime("%Y-%m-%d")

    if not os.path.exists(USAGE_FILE):
        return 0

    try:
        with open(USAGE_FILE, "r") as f:
            data = json.load(f)
            if data.get("date") == today:
                return data.get("count", 0)
            else:
                return 0  # New day, reset count
    except (json.JSONDecodeError, ValueError):
        return 0


def increment_daily_count():
    """Increments the daily usage count and saves it to the file."""
    today = datetime.now().strftime("%Y-%m-%d")
    count = get_daily_count()

    new_data = {"date": today, "count": count + 1}

    with open(USAGE_FILE, "w") as f:
        json.dump(new_data, f)


def check_rate_limits():
    """
    Checks if the request is allowed based on RPM and RPD.
    Sleeps if necessary to respect RPM.
    Returns True if allowed, False if RPD limit is reached.
    """
    global _last_request_time

    # Check RPD
    current_count = get_daily_count()
    if current_count >= MAX_RPD:
        print(f"Daily limit of {MAX_RPD} requests reached. Skipping...")
        return False

    # Check RPM (simple implementation: ensure min interval between requests)
    # MAX_RPM = 6 means 1 request every 10 seconds
    min_interval = 60.0 / MAX_RPM
    elapsed = time.time() - _last_request_time

    if elapsed < min_interval:
        sleep_time = min_interval - elapsed
        print(f"Rate limit: Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

    _last_request_time = time.time()
    return True
