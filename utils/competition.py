import requests
import logging


def get_competition_data(competition_id):
    """
    Fetches detailed data for a specific competition ID from Unstop.

    Args:
        competition_id (int or str): The ID of the competition.

    Returns:
        dict: A dictionary containing relevant competition details.
    """
    logging.info(f"Fetching data for competition ID: {competition_id}")
    url = f"https://unstop.com/api/public/competition/{competition_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()

        data = r.json().get("data", {}).get("competition", {})

        # Check if data is populated
        if not data:
            logging.warning(
                f"No competition data found for ID {competition_id} (or empty response)."
            )

        result = {
            "title": data.get("title"),
            "start_date": data.get("start_date"),
            "end_date": data.get("end_date"),
            "type": data.get("type"),
            "subtype": data.get("subtype"),
            "region": data.get("region"),
            "url": data.get("short_url"),
            "viewCount": data.get("viewsCount"),
            "registerCount": data.get("registerCount"),
            "prizes": data.get("overall_prizes"),
            "organizer": data.get("organisation", {}).get("name"),
            "details": data.get("details"),
            "eligibility": data.get("regnRequirements", {}).get("eligibility", "N/A"),
            "rounds": [
                {
                    "round": item.get("round_order"),
                    "title": (item.get("details") or [{}])[0].get("title"),
                    "description": (item.get("details") or [{}])[0].get("display_text"),
                }
                for item in data.get("rounds", [])
            ],
        }
        logging.info(
            f"Successfully fetched stats for '{result.get('title', 'Unknown')}'"
        )
        return result

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching competition data for ID {competition_id}: {e}")
        raise e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    competition_id = 1608968
    try:
        competition_details = get_competition_data(competition_id)
        import json

        print(json.dumps(competition_details, indent=4))
    except Exception as e:
        logging.error(f"Failed to run standalone test: {e}")
