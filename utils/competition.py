import requests


def get_competition_data(competition_id):
    url = f"https://unstop.com/api/public/competition/{competition_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    r = requests.get(url, headers=headers)

    data = r.json().get("data", {}).get("competition", {})

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

    return result


if __name__ == "__main__":
    competition_id = 1608968
    competition_details = get_competition_data(competition_id)

    import json

    print(json.dumps(competition_details, indent=4))
