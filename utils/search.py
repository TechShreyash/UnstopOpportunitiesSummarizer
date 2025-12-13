import requests
import logging


def search_competitions(total_competitions):
    """
    Searches for competitions on Unstop.

    Args:
        total_competitions (int): Although named 'total_competitions', currently used as 'per_page' param in the API.

    Returns:
        list: A list of competition IDs found.
    """
    logging.info(f"Searching for competitions (limit: {total_competitions})...")

    url = f"https://unstop.com/api/public/opportunity/search-result?opportunity=all&page=1&per_page={total_competitions}&oppstatus=open&sortBy=&orderBy=&filter_condition=&sort=prize&dir=desc&undefined=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json().get("data", {}).get("data", [])
        competitions = [item["id"] for item in data]
        logging.info(f"Successfully retrieved {len(competitions)} competitions.")
        return competitions
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching search results: {e}")
        return []


if __name__ == "__main__":
    # Configure basic logging for standalone run
    logging.basicConfig(level=logging.INFO)
    total_competitions = 5
    competitions = search_competitions(total_competitions)

    print(competitions)
