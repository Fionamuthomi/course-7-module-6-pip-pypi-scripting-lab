"""
fetch_data.py
--------------
Fetches data from a public API using the third-party `requests` package
and writes the results to a CSV file using Python's built-in `csv` module.

Run:
    python fetch_data.py
"""

import csv
import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"
OUTPUT_FILE = "posts_output.csv"
NUM_RECORDS = 10


def fetch_posts(limit=NUM_RECORDS):
    """Fetch a list of posts from the JSONPlaceholder API."""
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()[:limit]
    print(f"Request failed with status code {response.status_code}")
    return []


def write_to_csv(posts, filename=OUTPUT_FILE):
    """Write fetched posts to a CSV file."""
    if not posts:
        print("No data to write.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "userId", "title", "body"])
        writer.writeheader()
        for post in posts:
            writer.writerow(post)

    print(f"Wrote {len(posts)} records to {filename}")


if __name__ == "__main__":
    posts = fetch_posts()
    write_to_csv(posts)