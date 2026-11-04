#!/usr/bin/env python3
"""Minimal fal.ai queue client. Reads FAL_KEY from the environment.

python3 scripts/fal.py ENDPOINT out_prefix --prompt "..." [--image a.png --image b.jpg] [--json '{"k":v}']
Local images are sent as data URIs (downscaled to <= 2560px). Writes out_prefix_N.<ext> and out_prefix.json.
"""
import argparse, base64, io, json, os, sys, time, urllib.request, urllib.error

KEY = os.environ["FAL_KEY"]
H = {"Authorization": f"Key {KEY}", "Content-Type": "application/json"}

def data_uri(path, max_side=2560):
    if path.startswith("http"): return path
    from PIL import Image
    im = Image.open(path)
    has_alpha = im.mode in ("RGBA", "LA")
    im = im.convert("RGBA" if has_alpha else "RGB")
    if max(im.size) > max_side: im.thumbnail((max_side, max_side))
    buf = io.BytesIO(); fmt = "PNG" if has_alpha else "JPEG"
    im.save(buf, fmt, **({} if has_alpha else {"quality": 93}))
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode()

def req(url, body=None, method=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, headers=H, method=method or ("POST" if data else "GET"))
    for attempt in range(6):
        try:
            with urllib.request.urlopen(r, timeout=120) as resp: return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:2000]
            if e.code in (429, 500, 502, 503, 504) and attempt < 5: time.sleep(3 * (attempt + 1)); continue
            raise SystemExit(f"HTTP {e.code} {url}\n{msg}")
        except urllib.error.URLError:
            time.sleep(3 * (attempt + 1))
    raise SystemExit("network failure")

def run(endpoint, body, timeout=900):
    sub = req(f"https://queue.fal.run/{endpoint}", body)
    status_url, resp_url = sub["status_url"], sub["response_url"]
    t0 = time.time()
    while time.time() - t0 < timeout:
        st = req(status_url)
        if st.get("status") == "COMPLETED": return req(resp_url)
        time.sleep(4)
    raise SystemExit(f"timeout {endpoint} {sub.get('request_id')}")

def save(result, prefix):
    os.makedirs(os.path.dirname(prefix) or ".", exist_ok=True)
    json.dump(result, open(prefix + ".json", "w"), indent=1)
    imgs = result.get("images") or ([result["image"]] if result.get("image") else [])
    out = []
    for i, im in enumerate(imgs):
        url = im["url"]; ext = (im.get("content_type") or "image/png").split("/")[-1].replace("jpeg", "jpg")
        p = f"{prefix}_{i}.{ext}"
        if url.startswith("data:"): open(p, "wb").write(base64.b64decode(url.split(",", 1)[1]))
        else: urllib.request.urlretrieve(url, p)
        out.append(p)
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("endpoint"); ap.add_argument("prefix")
    ap.add_argument("--prompt"); ap.add_argument("--prompt-file")
    ap.add_argument("--image", action="append", default=[]); ap.add_argument("--image-key", default="image_urls")
    ap.add_argument("--json", default="{}")
    a = ap.parse_args()
    body = json.loads(a.json)
    p = open(a.prompt_file).read() if a.prompt_file else a.prompt
    if p: body["prompt"] = p
    if a.image:
        uris = [data_uri(x) for x in a.image]
        body[a.image_key] = uris if a.image_key.endswith("s") else uris[0]
    t = time.time(); res = run(a.endpoint, body)
    files = save(res, a.prefix)
    print(f"{a.endpoint} {time.time()-t:.0f}s ->", files)
