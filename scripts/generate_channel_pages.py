import os
import json
from datetime import datetime

# === CONFIG ===
CACHE_DIR = "html/cached"
OUTPUT_DIR = "html/channels"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def format_duration(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"

def format_date(iso_str):
    dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    return dt.strftime("%b %d, %Y")

def format_views(count):
    if count >= 1_000_000:
        return f"{count // 1_000_000}M views"
    elif count >= 1_000:
        return f"{count // 1_000}K views"
    return f"{count} views"

def render_video_block(video, handle):
    short_class = " short" if video["duration"] <= 130 else ""
    return f"""
    <div class="video{short_class}">
        <a href="../watch.html?channel={handle}&video={video['video_id']}">
            <img src="{video['thumbnail']}" alt="{video['title']}">
        </a>
        <div class="meta">
            <h3>{video['title']}</h3>
            <p>📅 {format_date(video['published_at'])}</p>
            <p>👁️ {format_views(video['view_count'])} • 🕒 {format_duration(video['duration'])}</p>
        </div>
    </div>
    """

def build_html(handle, data):
    title = handle.strip("@")
    videos = data["videos"]

    full_videos = sorted([v for v in videos if v["duration"] > 120], key=lambda v: v["published_at"], reverse=True)
    shorts = sorted([v for v in videos if v["duration"] <= 120], key=lambda v: v["published_at"], reverse=True)

    top_videos = sorted(
        [v for v in full_videos],
        key=lambda v: v["view_count"],
        reverse=True
    )[:5]

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title} - AgapeOS</title>
    <style>
        body {{
            font-family: sans-serif;
            background-color: #f4f4f4;
            padding: 2em;
        }}
        h1, h2, h3 {{
            text-align: center;
        }}
        .section {{
            margin-bottom: 3em;
        }}
        .video-grid {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 1.5em;
        }}
        .video {{
            background: white;
            border-radius: 8px;
            box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
            padding: 0.5em;
            width: 280px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .video.short {{
            background-color: #f9f9f9;
            border-left: 5px solid #aaa;
        }}
        .video img {{
            width: 100%;
            border-radius: 6px;
        }}
        .meta {{
            width: 100%;
        }}
        .meta h3 {{
            margin: 0.5em 0 0.2em;
            font-size: 1em;
        }}
        .meta p {{
            margin: 0.2em 0;
            color: #444;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="section">
        <h2>🔥 Top 5 Most Viewed</h2>
        <div class="video-grid">
            {"".join(render_video_block(v, title) for v in top_videos)}
        </div>
    </div>

    <div class="section">
        <h2>📅 Latest Videos and Shorts</h2>
"""
    i = 0
    chunk_full = 30
    chunk_shorts = 10
    while i < max(len(full_videos), len(shorts)):
        full_chunk = full_videos[i:i+chunk_full]
        short_chunk = shorts[i:i+chunk_shorts]

        if full_chunk:
            html += f"<h3>🎥 Full Videos {i+1}–{i+len(full_chunk)}</h3><div class='video-grid'>"
            html += "".join(render_video_block(v, title) for v in full_chunk)
            html += "</div>"

        if short_chunk:
            html += f"<h3>📱 Shorts {i+1}–{i+len(short_chunk)}</h3><div class='video-grid'>"
            html += "".join(render_video_block(v,title) for v in short_chunk)
            html += "</div>"

        i += max(chunk_full, chunk_shorts)

    html += "</div></body></html>"
    return html

def main():
    for filename in os.listdir(CACHE_DIR):
        if not filename.endswith(".json"):
            continue

        path = os.path.join(CACHE_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        handle = os.path.splitext(filename)[0]
        html = build_html(handle, data)

        out_path = os.path.join(OUTPUT_DIR, f"{handle}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Built page: {out_path}")

if __name__ == "__main__":
    main()
