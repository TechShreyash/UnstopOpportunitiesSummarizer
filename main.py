import logging
import json
import time

from utils.search import search_competitions
from utils.competition import get_competition_data
from utils.summarize import summarize_data
from utils.db import save_competition_to_db, is_competition_in_db
from utils.telegram import send_telegram_message

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

# Suppress noisy logs from external libraries
for logger_name in ["google", "urllib3", "httpcore", "httpx", "google_genai"]:
    logging.getLogger(logger_name).setLevel(logging.WARNING)


def main():
    """
    Main function to orchestrate the scraping, summarizing, and posting process.
    """
    logging.info("Starting the Unstop Opportunities Summarizer.")

    # Search for latest competitions
    # You can adjust the number of competitions to search
    try:
        competitions = search_competitions(50)
        logging.info(f"Found {len(competitions)} competitions.")
    except Exception as e:
        logging.error(f"Failed to search competitions: {e}")
        return

    for competition in competitions:
        # Check if we have already processed this competition
        if is_competition_in_db(competition):
            logging.info(f"Competition {competition} already in DB. Skipping.")
            continue

        logging.info(f"Processing competition {competition}...")

        summary = None
        try:
            # Fetch detailed data for the competition
            competition_data = get_competition_data(competition)
            logging.debug(f"Competition Data: {json.dumps(competition_data, indent=4)}")

            # Generate a summary using Gemini
            summary = summarize_data(competition_data)
        except Exception as e:
            logging.error(f"Error summarising competition {competition}: {str(e)}")
            continue

        if summary is None:
            logging.warning(
                f"Skipping competition {competition} due to rate limit or error."
            )
            continue

        logging.info(f"Summary generated for {competition}.")
        logging.debug(f"Summary Content: {summary}")

        try:
            # Send the summary to the Telegram channel
            send_telegram_message(summary)
            logging.info(f"Notification sent for competition {competition}.")
        except Exception as e:
            logging.error(f"Error sending message to Telegram: {str(e)}")
            continue

        # Save to DB to avoid reprocessing
        save_competition_to_db(competition)
        logging.info(f"Competition {competition} saved to DB.")

    logging.info("Run complete.")


if __name__ == "__main__":
    main()
