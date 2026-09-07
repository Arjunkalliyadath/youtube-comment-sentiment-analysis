"""
Extracts comments from a YouTube video using Playwright, and saves the
video's title, channel, and thumbnail so the dashboard can display them.

Output:
    comments.csv    -> raw scraped comments
    video_meta.json -> video title, channel, thumbnail, and link
"""

import json
import re
from datetime import datetime, timezone

import pandas as pd
import requests
from playwright.sync_api import sync_playwright

COMMENTS_FILE = "comments.csv"
META_FILE = "video_meta.json"


def extract_video_id(url: str) -> str | None:
    """Pull the 11-character video id out of any common YouTube URL shape."""
    match = re.search(
        r"(?:v=|/shorts/|/embed/|youtu\.be/)([A-Za-z0-9_-]{11})",
        url,
    )
    return match.group(1) if match else None


def fetch_video_metadata(video_url: str, video_id: str | None) -> dict:
    """Fetch title/channel/thumbnail via YouTube's public oEmbed endpoint.

    No API key needed. Falls back to the standard thumbnail CDN URL if the
    request fails (private/unlisted videos, no network, etc).
    """
    metadata = {
        "video_url": video_url,
        "video_id": video_id or "",
        "title": "Untitled video",
        "channel": "",
        "thumbnail_url": (
            f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" if video_id else ""
        ),
        "extracted_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        response = requests.get(
            "https://www.youtube.com/oembed",
            params={"url": video_url, "format": "json"},
            timeout=10,
        )
        if response.ok:
            data = response.json()
            metadata["title"] = data.get("title", metadata["title"])
            metadata["channel"] = data.get("author_name", metadata["channel"])
            metadata["thumbnail_url"] = data.get(
                "thumbnail_url", metadata["thumbnail_url"]
            )
        else:
            print(
                f"Could not fetch video info (HTTP {response.status_code}). "
                "Using fallback thumbnail."
            )
    except requests.RequestException as e:
        print(f"Could not fetch video info ({e}). Using fallback thumbnail.")

    return metadata


def main():
    video_url = input("Paste YouTube Video URL: ").strip()
    video_id = extract_video_id(video_url)

    if not video_id:
        print(
            "Warning: couldn't parse a video id from that URL. "
            "The dashboard will still work, but the thumbnail may be missing."
        )

    video_meta = fetch_video_metadata(video_url, video_id)

    comments = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(video_url, timeout=120000)

        print("Opening video...")
        page.wait_for_timeout(5000)
        page.mouse.wheel(0, 8000)
        page.wait_for_timeout(5000)

        previous_count = 0

        for scroll in range(30):
            comment_elements = page.locator("#content-text")
            count = comment_elements.count()

            for i in range(count):
                try:
                    comment = comment_elements.nth(i).inner_text().strip()
                    if len(comment) > 3:
                        comments.add(comment)
                except Exception:
                    pass

            print(f"Scroll {scroll + 1} | Comments: {len(comments)}")

            if len(comments) == previous_count:
                break

            previous_count = len(comments)
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(3000)

        browser.close()

    video_meta["comment_count"] = len(comments)

    df = pd.DataFrame(list(comments), columns=["comment"])
    df.to_csv(COMMENTS_FILE, index=False)

    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(video_meta, f, indent=2)

    print(f"Saved {len(comments)} comments to {COMMENTS_FILE}")
    print(f"Saved video info to {META_FILE}")


if __name__ == "__main__":
    main()
