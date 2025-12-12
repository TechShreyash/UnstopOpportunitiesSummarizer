from utils.search import search_competitions
from utils.competition import get_competition_data
from utils.summarize import summarize_data
from utils.db import save_competition_to_db, is_competition_in_db
from utils.telegram import send_telegram_message
import time
import json


def main():
    competitions = search_competitions(1)

    for competition in competitions:
        if is_competition_in_db(competition):
            continue

        summary = None
        try:
            competition_data = get_competition_data(competition)
            print(json.dumps(competition_data, indent=4))
            summary = summarize_data(competition_data)
        except Exception as e:
            print(f"Error summarizing competition {competition}: {str(e)}")
            continue

        if summary is None:
            print(f"Skipping competition {competition} due to rate limit or error.")
            continue

        print(json.dumps(summary, indent=4))

        try:
            send_telegram_message(summary)
        except Exception as e:
            print(f"Error sending message to Telegram: {str(e)}")
            continue

        save_competition_to_db(competition)


if __name__ == "__main__":
    main()
