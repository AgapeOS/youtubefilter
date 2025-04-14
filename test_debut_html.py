# test_debug_html.py
import requests

url = "https://www.youtube.com/@answersingenesis"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
}

resp = requests.get(url, headers=headers)
with open("debug_output.html", "w", encoding="utf-8") as f:
    f.write(resp.text)

print("File written!")
