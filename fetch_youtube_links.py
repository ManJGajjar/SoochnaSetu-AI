import json
import urllib.parse
import requests
import re
from pathlib import Path
import time

SEED_PATH = Path("backend/data/schemes_seed.json")

def fetch_youtube_links():
    if not SEED_PATH.exists():
        print(f"Error: Could not find {SEED_PATH}")
        return

    with open(SEED_PATH, "r", encoding="utf-8") as f:
        schemes = json.load(f)

    updated_count = 0
    print("Fetching actual video links from YouTube...")
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for scheme in schemes:
        # Check if it already has a real youtube.com/watch link
        if "youtubeTutorialLink" in scheme and "watch?v=" in scheme["youtubeTutorialLink"]:
            continue
            
        search_query = f"how to apply for {scheme['name']} online official tutorial"
        encoded_query = urllib.parse.quote_plus(search_query)
        url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        try:
            response = requests.get(url, headers=headers)
            # Find the first video ID in the raw HTML
            match = re.search(r"watch\?v=([a-zA-Z0-9_-]{11})", response.text)
            
            if match:
                video_url = f"https://www.youtube.com/watch?v={match.group(1)}"
                scheme["youtubeTutorialLink"] = video_url
                print(f"Found video for {scheme['name']}: {video_url}")
                updated_count += 1
            else:
                print(f"No video found for {scheme['name']}")
                
            time.sleep(1.5)  # Rate limiting to prevent IP block
        except Exception as e:
            print(f"Error searching for {scheme['name']}: {e}")

    if updated_count > 0:
        with open(SEED_PATH, "w", encoding="utf-8") as f:
            json.dump(schemes, f, indent=2, ensure_ascii=False)
        print(f"Successfully updated {updated_count} schemes with exact YouTube video links.")
    else:
        print("No new links needed updating.")

if __name__ == "__main__":
    fetch_youtube_links()
