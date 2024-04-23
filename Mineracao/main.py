import requests
from bs4 import BeautifulSoup
import re

def extract_video_ids(html_content):
    soup = BeautifulSoup(html_content, 'lxml')

    video_ids = []

    # Search for video IDs using the pattern "videoId"
    for match in re.findall(r'"videoId":"(\w+)"', html_content):
        video_ids.append(match)

    return video_ids

def save_response_content(response):
    # Convert response content to plain text (if needed)
    if isinstance(response.content, bytes):
        response_content = response.content.decode('utf-8')
    else:
        response_content = response.content

    # Extract video IDs before saving
    video_ids = extract_video_ids(response_content)
    seen_items = set()  # Use a set to efficiently check for seen items
    unique_list = []

    for item in video_ids:
        if item not in seen_items:  # The 'if' statement
            seen_items.add(item)  # This line should be indented at the same level as 'if'
            unique_list.append(item)  # This line should also be indented

    print(unique_list[:10])


def main():
    url = "https://youtube.com/results?search_query=airdrop"  # Replace with your desired URL
    response = requests.get(url)

    if response.status_code == 200:
        print("Successfully retrieved content.")
        save_response_content(response)  # Replace with your desired filename
    else:
        print(f"Failed to access URL: {response.status_code}")

if __name__ == "__main__":
    main()
