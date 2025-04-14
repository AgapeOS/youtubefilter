import os
import json

CACHE_DIR = "html/cached"
OUTPUT_FILE = "html/all_videos.json"

def main():
    all_videos = {}

    for filename in os.listdir(CACHE_DIR):
        if not filename.endswith(".json"):
            continue

        handle = os.path.splitext(filename)[0]
        path = os.path.join(CACHE_DIR, filename)

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            channel_id = data.get("channel_id", "")
            for video in data.get("videos", []):
                video_id = video["video_id"]
                all_videos[video_id] = {
                    **video,
                    "channel": f"@{handle}",
                    "channel_id": channel_id
                }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_videos, f, indent=2)
    print(f"✅ Wrote: {OUTPUT_FILE} with {len(all_videos)} videos")

if __name__ == "__main__":
    main()
