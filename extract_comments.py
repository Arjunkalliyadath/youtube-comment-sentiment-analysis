from playwright.sync_api import sync_playwright
import pandas as pd
import time

comments = set()   # avoid duplicates

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto(
        "https://www.youtube.com/watch?v=mach2g2oLTA"
    )

    print("Opening video...")

    page.wait_for_timeout(5000)

    # Scroll to load comments section
    page.mouse.wheel(0, 8000)

    page.wait_for_timeout(5000)

    previous_count = 0

    for _ in range(30):   # number of scroll rounds

        comment_elements = page.locator("#content-text")

        count = comment_elements.count()

        print(f"Comments loaded: {count}")

        for i in range(count):

            try:
                comment = comment_elements.nth(i).inner_text()

                if comment.strip():
                    comments.add(comment)

            except:
                pass

        # Stop if no new comments are appearing
        if len(comments) == previous_count:
            print("No new comments found.")
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
    "raw_comments.csv",
    index=False
)

print(f"{len(comments)} comments saved.")