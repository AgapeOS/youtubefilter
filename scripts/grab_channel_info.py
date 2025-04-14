import json
import re
import requests
from bs4 import BeautifulSoup

INPUT_FILE = "data/new_handles.json"
OUTPUT_FILE = "data/channels.json"

def extract_info_from_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    match = re.search(r'"browseId":"(UC[0-9A-Za-z_-]{21}[AQgw])"', html)
    channel_id = match.group(1) if match else None
    title = soup.find("meta", {"property": "og:title"})
    thumb = soup.find("link", {"itemprop": "thumbnailUrl"})
    canonical = soup.find("link", {"rel": "canonical"})
    canonical_handle = canonical["href"].split("/")[-1] if canonical else None
    return channel_id, title["content"] if title else None, thumb["href"] if thumb else None, canonical_handle

def get_channel_data(handle: str, category: str, age_group: str) -> dict | None:
    url = f"https://www.youtube.com/{handle}"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            channel_id, title, thumbnail, canonical_handle = extract_info_from_html(resp.text)

            if canonical_handle and canonical_handle.lower() != handle.lower().lstrip("@"):
                print(f"⚠️ Handle mismatch: {handle} → @{canonical_handle}")

            if channel_id:
                return {
                    "channel_id": channel_id,
                    "title": title or handle,
                    "thumbnail": thumbnail,
                    "category": category,
                    "age_group": age_group
                }
        else:
            print(f"HTTP error {resp.status_code} for {handle}")
    except Exception as e:
        print(f"Error fetching {handle}: {e}")
    return None

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        structure = json.load(f)

    approved = {}

    for category, age_groups in structure.items():
        for age_group, handles in age_groups.items():
            for handle in handles:
                print(f"Fetching {handle} ({category} - {age_group})...")
                data = get_channel_data(handle, category, age_group)
                if data:
                    approved[handle] = data
                    print(f"✔ Added: {handle} → {data['channel_id']}")
                else:
                    print(f"Failed to fetch {handle}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(approved, f, indent=4)

    print(f"\nSaved {len(approved)} channels to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
