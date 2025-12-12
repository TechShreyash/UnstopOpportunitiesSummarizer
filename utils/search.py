import requests


def search_competitions(total_competitions):
    url = f"https://unstop.com/api/public/opportunity/search-result?opportunity=all&page=1&per_page={total_competitions}&sortBy=&orderBy=&filter_condition=&sort=prize&dir=desc&undefined=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    r = requests.get(url, headers=headers)

    data = r.json().get("data", {}).get("data", [])

    competitions = [item["id"] for item in data]

    return competitions


if __name__ == "__main__":
    total_competitions = 5
    competitions = search_competitions(total_competitions)

    print(competitions)
