from bs4 import BeautifulSoup
import re


# List of bot IDs to skip
bots_to_skip = ["777000", "1629538930", "928179081"]


def extract_peer_ids(html_file_path):
    # Read the HTML file
    with open(html_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Find all div tags with class "Avatar"
    avatar_divs = soup.find_all("div", class_="Avatar")

    # Extract data-peer-id attributes, skipping those with no photo
    peer_ids = [
        div.get("data-peer-id")
        for div in avatar_divs
        if div.get("data-peer-id") and "no-photo" not in div.get("class", [])
    ]

    # Filter out peer IDs that start with '-' and bot IDs
    peer_ids = set(
        pid for pid in peer_ids if not pid.startswith("-") and pid not in bots_to_skip
    )
    return peer_ids


html_file_path = "a.html"

peer_ids = extract_peer_ids(html_file_path)

with open("output.txt", "w", encoding="utf-8") as output_file:
    for peer_id in peer_ids:
        output_file.write(f"https://web.telegram.org/a/#{peer_id}\n")
