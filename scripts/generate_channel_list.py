import os
import json

CACHE_DIR = "html/cached"
OUTPUT_FILE = "html/index.html"
CHANNEL_PAGE_DIR = "channels"
CHANNEL_INFO_JSON = "data/channels.json"

os.makedirs("html", exist_ok=True)

def build_index():
    with open(CHANNEL_INFO_JSON, "r", encoding="utf-8") as f:
        channel_info = json.load(f)

    groups = {
        "Biblical & Creation": [],
        "Conventional Sciences": [],
        "Music & Art": [],
        "Toddler Content": [],
        "Other": []
    }

    for handle, info in channel_info.items():
        filename = f"{handle.strip('@')}.json"
        cached_path = os.path.join(CACHE_DIR, filename)

        if not os.path.exists(cached_path):
            continue

        html_block = f"""
        <a class="channel-card" href="{CHANNEL_PAGE_DIR}/{handle.strip('@')}.html">
            <img class="thumb" src="{info['thumbnail']}" alt="{info['title']}">
            <div class="channel-name">{info['title']}</div>
        </a>
        """

        cat = info.get("category", "")
        age = info.get("age_group", "")

        if age == "toddler":
            groups["Toddler Content"].append(html_block)
        elif cat in ["Christ-Centered Knowledge", "Creation-based science & nature", "Christian Child Development"]:
            groups["Biblical & Creation"].append(html_block)
        elif cat in ["Conventional STEM", "Coding and Computer Science"]:
            groups["Conventional Sciences"].append(html_block)
        elif cat in ["Learn Music", "Art and Drawing"]:
            groups["Music & Art"].append(html_block)
        else:
            groups["Other"].append(html_block)

    # Build the final HTML
    sections = []
    for group_name, cards in groups.items():
        if not cards:
            continue
        sections.append(f"""
        <h2>{group_name}</h2>
        <div class="channel-grid">
            {''.join(cards)}
        </div>
        """)

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AgapeOS Approved Channels</title>
    <style>
        body {{
            font-family: sans-serif;
            background: #f9f9f9;
            padding: 2em;
        }}
        h1, h2 {{
            text-align: center;
        }}
        .channel-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 2em;
            margin: 2em 0;
            justify-items: center;
        }}
        .channel-card {{
            display: flex;
            flex-direction: column;
            align-items: center;
            background: white;
            padding: 1em;
            border-radius: 8px;
            box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
            text-decoration: none;
            color: inherit;
            transition: transform 0.2s ease;
        }}
        .channel-card:hover {{
            transform: scale(1.03);
        }}
        .thumb {{
            width: 200px;
            height: 200px;
            object-fit: cover;
            border-radius: 50%;
            margin-bottom: 0.8em;
        }}
        .channel-name {{
            font-size: 1em;
            font-weight: bold;
            text-align: center;
        }}
    </style>
</head>
<body>
    <h1>📺 AgapeOS Approved Channels</h1>
    {''.join(sections)}
</body>
</html>"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Index built: {OUTPUT_FILE}")

if __name__ == "__main__":
    build_index()
