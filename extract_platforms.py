import pandas as pd
import json

df = pd.read_excel("Meghna.xlsx", sheet_name="Sheet1")

platforms = []
current_platform = None

for _, row in df.iterrows():
    platform_name = row["Platform"]
    url = row["Policy URL"]
    
    # New platform row
    if pd.notna(platform_name) and str(platform_name).strip() not in ["", "▶  US — K-12", "▶  India"]:
        current_platform = str(platform_name).strip()
    
    # Collect all URLs for current platform
    if current_platform and pd.notna(url) and str(url).strip().startswith("http"):
        platforms.append({
            "platform": current_platform,
            "url": str(url).strip()
        })

with open("data/platforms.json", "w") as f:
    json.dump(platforms, f, indent=2)

print(f"Extracted {len(platforms)} URLs across platforms")

# Preview
for p in platforms[:10]:
    print(f"  {p['platform']}: {p['url']}")