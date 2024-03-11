import os
import requests
from wget import download
from typing import Dict, Tuple, Union, List
import sys

url = "https://tokviewer.net/api/"
session = requests.Session()  # Create a session
video_link: List[str] = []  # Initialize the list of video links

# Check if the target username is provided as a command-line argument
if len(sys.argv) < 2:
    print(
        "Please provide the target username as a command-line argument.\nExample: -> $ python ChocoTok_downloader.py User"
    )
    sys.exit(1)

target = sys.argv[1]  # Get the target username from the command-line argument

print("Processing...")

payload = {"username": f"@{target}"}
headers = {
    "content-type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54",
}

# Make the first POST request using the session
with session as s:
    profile = s.post(
        url=url + "check-profile", json=payload, headers=headers, timeout=30
    )

# Make the second POST request using the same session
payload["key"] = profile.json()["data"]["key"]
payload["token"] = profile.json()["data"]["token"]


def video_reset(data: Dict) -> Union[Tuple[Dict[str, str], Tuple[str, str, str]], bool]:
    response = session.post(url=url + "video", json=data, headers=headers, timeout=30)
    response_data = response.json()
    if response_data["cursor"]:
        data["after"] = response_data["cursor"]
        return data, tuple(url["play"] for url in response_data["data"])
    else:
        return False


# Call the function in a loop and update the list of video links
while result := video_reset(payload):
    payload, urls = result
    video_link.extend(urls)  # Extend the list of video links

unique_video_links = tuple(set(video_link))


def download_files(urls: Tuple, target_folder: str) -> str:
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)  # Create the folder if it doesn't exist

    for index, url in enumerate(urls, start=1):
        file_name = f"video_{index}.mp4"  # Generate the file name dynamically
        file_path = os.path.join(
            target_folder, file_name
        )  # Create the full file path in the target folder

        # Download the file to the target folder
        download(url, out=file_path)
    return "\nDownloads completed!"


print(f"Downloadable links: {len(unique_video_links)}")
print(download_files(urls=unique_video_links, target_folder=target))
