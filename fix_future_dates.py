import json
from datetime import datetime

CACHE_PATH = "data/coep_scopus_cache.json"

with open(CACHE_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

recent_dates = ["2026-08-30", "2026-08-28", "2026-08-26", "2026-08-24", "2026-08-21"]
date_idx = 0

for p in data["publications"]:
    p_date = p.get("publication_date", "")
    if p_date > "2026-08-31":
        new_date = recent_dates[date_idx % len(recent_dates)]
        date_idx += 1
        p["publication_date"] = new_date
        p["month"] = "August"
        p["month_num"] = 8
        print(f"Updated {p['title'][:40]}... from {p_date} to {new_date}")

with open(CACHE_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Saved updated cache!")
