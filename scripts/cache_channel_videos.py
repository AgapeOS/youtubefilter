import os
import json
from googleapiclient.discovery import build
from isodate import parse_duration

# === CONFIG ===
INPUT_JSON = "data/channels.json"
CACHE_DIR = "html/cached"
API_KEY = "AIzaSyD56dZt99QWN1Q_wRAU7Q3SKdTWnZ5Yy-8"
VIDEOS_PER_REQUEST = 50

# === SETUP ===
os.makedirs(CACHE_DIR, exist_ok=True)
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_uploads_playlist_id(channel_id: str) -> str:
    response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()
    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def fetch_playlist_items(playlist_id: str, page_token: str = None):
    return youtube.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=VIDEOS_PER_REQUEST,
        pageToken=page_token
    ).execute()

def fetch_video_details(video_ids: list[str]):
    response = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=','.join(video_ids)
    ).execute()

    results = []
    for item in response.get("items", []):
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        content = item.get("contentDetails", {})

        # Ensure 'duration' is present (skip if missing)
        if "duration" not in content:
            print(f"⚠️ Skipping video {item.get('id')} - missing duration.")
            continue

        results.append({
            "video_id": item["id"],
            "title": snippet.get("title", "Untitled"),
            "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
            "published_at": snippet.get("publishedAt", ""),
            "duration": parse_duration(content["duration"]).total_seconds(),
            "description": snippet.get("description", ""),
            "tags": snippet.get("tags", []),
            "view_count": int(stats.get("viewCount", 0)),
            "channel_id": snippet.get("channelId", ""),
            "url": f"https://www.youtube.com/watch?v={item['id']}"
        })
    return results

def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        channels = json.load(f)

    for handle, info in channels.items():
        print(f"Fetching videos for: {handle}")
        cache_path = os.path.join(CACHE_DIR, f"{handle.strip('@')}.json")

        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as cf:
                cached_data = json.load(cf)
                cached = cached_data.get("videos", [])
                cached_ids = {v["video_id"] for v in cached}
        else:
            cached = []
            cached_ids = set()

        uploads_playlist_id = get_uploads_playlist_id(info["channel_id"])
        next_page = None
        new_videos = []

        while len(new_videos) < VIDEOS_PER_REQUEST:
            print(f"🔄 Fetching playlist page... (already found {len(new_videos)} new videos)")

            playlist_data = fetch_playlist_items(uploads_playlist_id, next_page)
            ids = [item["contentDetails"]["videoId"] for item in playlist_data["items"]]
            print(f"📄 Playlist page returned {len(ids)} videos.")

            # Skip already cached
            new_ids = [vid for vid in ids if vid not in cached_ids]
            print(f"🎯 New unique videos after filter: {len(new_ids)}")

            if not new_ids:
                next_page = playlist_data.get("nextPageToken")
                if not next_page:
                    print("⛔️ No more pages to paginate.")
                    break
                continue

            details = fetch_video_details(new_ids)
            for video in details:
                if video["video_id"] not in cached_ids and len(new_videos) < VIDEOS_PER_REQUEST:
                    new_videos.append(video)

            print(f"📦 Total new videos collected so far: {len(new_videos)}")
            next_page = playlist_data.get("nextPageToken")
            if not next_page:
                print("✅ Reached last page of playlist.")
                break

        if new_videos:
            print(f"➕ {len(new_videos)} new videos found for {handle}")
            cached.extend(new_videos)
            cached.sort(key=lambda x: x["published_at"])  # Keep oldest first
            with open(cache_path, "w", encoding="utf-8") as cf:
                json.dump({
                    "channel_id": info["channel_id"],
                    "videos": cached
                }, cf, indent=2)
        else:
            print(f"✅ No new videos for {handle}\n📺 Channel ID: {info['channel_id']}")

if __name__ == "__main__":
    main()