
# PulseScope

**See how viewers really feel about a YouTube video, at a glance.**

PulseScope scrapes the comments off a YouTube video, runs each one through a sentiment model, and shows you the result on a single dashboard: the video itself, an overall positive/neutral/negative breakdown, and a curated set of comments worth actually reading — not a giant table of everything.

https://github.com/user-attachments/assets/846364f8-5f8f-4e3e-9004-a9d7a583a2e3

---

## What it does

1. **Extract** — paste a YouTube link, and a Playwright-driven browser scrolls through the comment section, collecting every comment it can find. It also grabs the video's title, channel, and thumbnail.
2. **Clean** — duplicates, blank rows, and junk comments (anything under 4 characters) get filtered out.
3. **Analyze** — every remaining comment is scored as positive, neutral, or negative using [`cardiffnlp/twitter-roberta-base-sentiment-latest`](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest), a RoBERTa model fine-tuned specifically on social-media text.
4. **Explore** — a FastAPI dashboard shows the video, the sentiment split, and four curated views: a random sample, and the top 10 most confident comments in each sentiment category. The full result set is one click away as a CSV.

---

## Dashboard

- The video you analyzed — thumbnail, title, channel, and a link back to YouTube
- Total comments analyzed, plus a spectrum bar showing the positive / neutral / negative split
- A comment explorer with four tabs: **Random sample (20)**, **Top positive (10)**, **Top negative (10)**, **Top neutral (10)** — each comment tagged with the model's confidence score
- A **Download all comments** button that exports the complete analyzed set as CSV

---

## Project structure

```text
PulseScope/
│
├── static/
│   ├── style.css              # dashboard styling
│   └── script.js               # tabs, load-in animation, particle field
│
├── templates/
│   └── index.html               # dashboard template
│
├── extract_comments.py          # scrapes comments + fetches video info
├── clean_data.py                 # dedupes and filters raw comments
├── sentiment_comments.py        # runs the sentiment model
├── app.py                        # FastAPI dashboard
│
├── comments.csv                  # generated: raw scraped comments
├── cleaned_comments.csv          # generated: cleaned comments
├── sentiment_results.csv         # generated: comments + sentiment + score
├── video_meta.json                # generated: video title/channel/thumbnail
│
├── requirements.txt
└── README.md
```

The four generated files aren't checked into the repo — they're created the first time you run the pipeline, and overwritten each time you analyze a new video.

---

## Setup

Clone the repository and move into it:

```bash
git clone <repository-url>
cd PulseScope
```

Create and activate a virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install the Playwright browser (one-time):

```bash
playwright install chromium
```

---

## Running it

Run these three scripts in order, then start the dashboard.

**1. Scrape a video's comments**

```bash
python extract_comments.py
```

You'll be prompted to paste a YouTube video URL. A browser window opens, scrolls through the comment section, and closes when it stops finding new comments. This writes `comments.csv` and `video_meta.json`.

**2. Clean the comments**

```bash
python clean_data.py
```

Removes duplicates, blanks, and very short comments. Writes `cleaned_comments.csv`.

**3. Run sentiment analysis**

```bash
python sentiment_comments.py
```

Downloads the sentiment model on first run, then scores every comment. Writes `sentiment_results.csv`. This step can take a few minutes depending on comment count and hardware — a GPU speeds it up considerably, but it runs fine on CPU too.

**4. Launch the dashboard**

```bash
uvicorn app:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

If you open the dashboard before running the pipeline, it shows setup instructions instead of an error.

---

## Tech stack

| Layer | Tools |
|---|---|
| Scraping | Playwright |
| Data processing | Pandas |
| Sentiment model | Hugging Face Transformers · CardiffNLP Twitter RoBERTa |
| Backend | FastAPI · Jinja2 |
| Frontend | HTML, CSS, vanilla JS (no framework, no build step) |

---

## Notes on the sentiment model

The classifier returns one of three labels — `positive`, `neutral`, `negative` — along with a confidence score between 0 and 1. Comments that fail to classify (rare, usually due to unusual characters) are labeled `UNKNOWN` and excluded from the top-10 lists, though they still count toward the total.

The scraper works on any public YouTube video with comments enabled. Very large comment sections (tens of thousands of comments) will take proportionally longer to scroll through and analyze.

---

## Future enhancements

- Support for additional platforms (Instagram, Google Reviews)
- Sentiment trend over time, for videos with a long comment history
- Multi-video comparison view
- Keyword/topic extraction alongside sentiment

---

## Author

Arjun K
