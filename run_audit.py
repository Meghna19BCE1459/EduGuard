from dotenv import load_dotenv
load_dotenv()

from scraper.scraper import scrape_policy
from agent.scorer import score_policy
from storage.db import init_db, save_result

import json, time
from collections import defaultdict

def audit(platform: str, url: str):
    print(f"Scraping {platform}...")
    text = scrape_policy(url)
    print(f"Scoring ({len(text)} chars)...")
    scores = score_policy(text[:4000])
    save_result(platform, url, scores)
    print(f"  C1={scores['C1']} C2={scores['C2']} C3={scores['C3']} C4={scores['C4']} C5={scores['C5']} → {scores['total']}/10")
    return scores

if __name__ == "__main__":
    init_db()

    with open("data/platforms.json") as f:
        all_entries = json.load(f)

    grouped = defaultdict(list)
    for entry in all_entries:
        grouped[entry["platform"]].append(entry["url"])

    for platform, urls in grouped.items():
        print(f"\n=== {platform} ({len(urls)} URLs) ===")
        combined_text = ""
        for url in urls:
            try:
                print(f"  Scraping {url}...")
                text = scrape_policy(url)
                combined_text += f"\n\n--- Source: {url} ---\n{text}"
                time.sleep(1)
            except Exception as e:
                print(f"  FAILED scraping {url}: {e}")

        if combined_text:
            try:
                print(f"  Scoring ({len(combined_text)} chars combined)...")
                scores = score_policy(combined_text[:4000])
                save_result(platform, " | ".join(urls), scores)
                print(f"  C1={scores['C1']} C2={scores['C2']} C3={scores['C3']} C4={scores['C4']} C5={scores['C5']} → {scores['total']}/10")
            except Exception as e:
                print(f"  FAILED scoring {platform}: {e}")

        time.sleep(3)