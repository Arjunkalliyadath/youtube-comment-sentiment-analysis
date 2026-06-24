from playwright.sync_api import sync_playwright
import pandas as pd

video_url = input("Paste YouTube Video URL: ")

comments = set()

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(
        video_url,
        timeout=120000
    )

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

                comment = (
                    comment_elements
                    .nth(i)
                    .inner_text()
                    .strip()
                )

                if len(comment) > 3:
                    comments.add(comment)

            except:
                pass

        print(
            f"Scroll {scroll+1} | Comments: {len(comments)}"
        )

        if len(comments) == previous_count:
            break

        previous_count = len(comments)

        page.mouse.wheel(0, 10000)

        page.wait_for_timeout(3000)

    browser.close()

df = pd.DataFrame(
    list(comments),
    columns=["comment"]
)

df.to_csv(
    "comments.csv",
    index=False
)

print(
    f"Saved {len(comments)} comments"
)