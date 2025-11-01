#!/usr/bin/env python3
"""
Generate sitemap.xml from the repo contents.

- Maps /index.html → /
- Maps /path/index.html → /path
- Skips folders like /go, /private, /temp, /.git, node_modules, etc.
- Skips pages that declare <meta name="robots" content="noindex">
- Uses the file's last Git commit date (ISO YYYY-MM-DD) as <lastmod>,
  falling back to today's date if git data isn't available.
"""

from pathlib import Path
import subprocess
import datetime as dt
import re

# ── config ──────────────────────────────────────────────────────────────────
BASE_URL = "https://ridgwaycreative.com"  # no trailing slash
EXCLUDE_DIRS = {".git", "node_modules", "go", "temp", "private", "dist", "build", ".venv"}
PUBLISH_DIR = Path(__file__).resolve().parents[1]  # repo root; change if you publish from a subfolder
SITEMAP_PATH = PUBLISH_DIR / "sitemap.xml"
# ────────────────────────────────────────────────────────────────────────────

def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)

def is_noindex(html_path: Path) -> bool:
    try:
        txt = html_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    return bool(re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noindex', txt, flags=re.I))

def lastmod_iso(file_path: Path) -> str:
    try:
        iso = subprocess.check_output(
            ["git", "log", "-1", "--format=%cI", "--", str(file_path)],
            cwd=PUBLISH_DIR
        ).decode("utf-8").strip()
        if iso:
            return iso.split("T", 1)[0]  # YYYY-MM-DD
    except Exception:
        pass
    return dt.date.today().isoformat()

def url_for(file_path: Path) -> str:
    rel = file_path.relative_to(PUBLISH_DIR).as_posix()
    if rel == "index.html":
        path = "/"
    elif rel.endswith("/index.html"):
        path = "/" + rel[:-10]  # strip '/index.html'
    else:
        path = "/" + rel
    return f"{BASE_URL}{path}"

def collect_urls():
    urls = []
    for html in PUBLISH_DIR.rglob("*.html"):
        if is_excluded(html):
            continue
        if is_noindex(html):
            continue
        url = url_for(html)
        lm = lastmod_iso(html)
        urls.append((url, lm))
    # Deduplicate & sort (root first, then by URL)
    dedup = {}
    for u, lm in urls:
        dedup[u] = max(lm, dedup.get(u, lm))
    return sorted(dedup.items(), key=lambda x: (0 if x[0] == f"{BASE_URL}/" else 1, x[0]))

def write_sitemap(pairs):
    from xml.etree.ElementTree import Element, SubElement, tostring
    from xml.dom import minidom

    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for url, lm in pairs:
        u = SubElement(urlset, "url")
        SubElement(u, "loc").text = url
        SubElement(u, "lastmod").text = lm

    rough = tostring(urlset, encoding="utf-8")
    pretty = minidom.parseString(rough).toprettyxml(indent="  ", encoding="utf-8")
    SITEMAP_PATH.write_bytes(pretty)

def main():
    pairs = collect_urls()
    write_sitemap(pairs)
    print(f"Wrote {SITEMAP_PATH} with {len(pairs)} URLs")

if __name__ == "__main__":
    main()
