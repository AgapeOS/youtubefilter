import json

INPUT_JSON = "data/channels.json"
OUTPUT_HTML = "html/youtube.html"

TEMPLATE_START = """
<!DOCTYPE html>
<html>
  <head>
    <title>YouTube for AgapeOS</title>
    <style>
      body {
        font-family: sans-serif;
        text-align: center;
        background-color: #f4f4f4;
        padding: 2em;
      }
      .channel {
        background: white;
        border-radius: 10px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        display: inline-block;
        margin: 1em;
        padding: 1em;
        width: 300px;
        vertical-align: top;
      }
      .channel img {
        width: 100%;
        border-radius: 8px;
      }
      .channel-title {
        font-size: 1.2em;
        margin: 0.5em 0;
      }
      .button {
        background-color: #d35400;
        color: white;
        padding: 0.5em 1em;
        text-decoration: none;
        border-radius: 5px;
        display: inline-block;
        margin-top: 0.5em;
      }
      .button:hover {
        background-color: #b84300;
      }
    </style>
  </head>
  <body>
    <h1>AgapeOS Approved Channels</h1>
"""

TEMPLATE_END = """
  </body>
</html>
"""

def build_html_block(handle, info):
    return f"""
    <div class="channel">
      <a href="https://www.youtube.com/{handle}" target="_blank">
        <img src="{info['thumbnail']}" alt="{info['title']}">
      </a>
      <div class="channel-title">{info['title']}</div>
      <a class="button" href="https://www.youtube.com/{handle}" target="_blank">Visit Channel</a>
    </div>
    """

def format_group_name(group):
    if group == "2-5":
        return "Ages 2 to 5"
    elif group == "k-2":
        return "Grades K to 2"
    elif group == "3-5":
        return "Grades 3 to 5"
    else:
        return group

def main():
    with open(INPUT_JSON, "r") as f:
        channels = json.load(f)

    grouped = {}
    for handle, info in channels.items():
        group = info.get("group", "other")
        grouped.setdefault(group, []).append((handle, info))

    with open(OUTPUT_HTML, "w") as f:
        f.write(TEMPLATE_START)

        for group in sorted(grouped.keys()):
            group_label = format_group_name(group)
            f.write(f"<h2>{group_label}</h2>\n")
            for handle, info in grouped[group]:
                f.write(build_html_block(handle, info))

        f.write(TEMPLATE_END)

    print(f"✅ {OUTPUT_HTML} generated with {sum(len(v) for v in grouped.values())} channels.")

if __name__ == "__main__":
    main()
