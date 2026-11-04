#!/usr/bin/env python3
"""Download project media listed in data/all_media_manifest.json.

Examples:
  python3 scripts/fetch_media.py --author gus@phattyacid.studio --limit 100
  python3 scripts/fetch_media.py --since 2026-10-01 --videos
  python3 scripts/fetch_media.py --all            # every image + video (several GB)
Files go to media/downloads/<author>/<date>_<model>_<id8>.<ext> (git-ignored).
"""
import argparse, json, os, pathlib, urllib.request

root = pathlib.Path(__file__).resolve().parent.parent
p = argparse.ArgumentParser()
p.add_argument("--author"); p.add_argument("--since"); p.add_argument("--model")
p.add_argument("--limit", type=int); p.add_argument("--videos", action="store_true", help="videos only")
p.add_argument("--all", action="store_true")
a = p.parse_args()
rows = json.load(open(root / "data/all_media_manifest.json"))
if not a.all:
    if a.author: rows = [r for r in rows if r.get("author") == a.author]
    if a.since: rows = [r for r in rows if r["created_at"] >= a.since]
    if a.model: rows = [r for r in rows if r.get("model") == a.model]
    if a.limit: rows = rows[: a.limit]
n = 0
for r in rows:
    urls = [r["video_url"]] if a.videos else [u for u in (r.get("image_url"), r.get("video_url")) if u]
    for u in filter(None, urls):
        ext = u.split("?")[0].rsplit(".", 1)[-1][:4]
        out = root / "media/downloads" / (r.get("author") or "unknown") / f"{r['created_at'][:10]}_{(r.get('model') or 'na').replace('/', '-')}_{r['id'][:8]}.{ext}"
        if out.exists(): continue
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            urllib.request.urlretrieve(u, out); n += 1
        except Exception as e:
            print("FAIL", u, e)
print(f"downloaded {n} files")
