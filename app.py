import json
import os

import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

DATA_FILE = "sentiment_results.csv"
META_FILE = "video_meta.json"
RANDOM_SAMPLE_SIZE = 20
TOP_N = 10

SENTIMENT_LABELS = ("positive", "neutral", "negative")

app = FastAPI(title="PulseScope")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def load_video_meta() -> dict:
    meta = {
        "video_url": "",
        "video_id": "",
        "title": "No video analyzed yet",
        "channel": "",
        "thumbnail_url": "",
    }
    if os.path.exists(META_FILE):
        try:
            with open(META_FILE, "r", encoding="utf-8") as f:
                meta.update(json.load(f))
        except (json.JSONDecodeError, OSError) as e:
            print(f"Could not read {META_FILE}: {e}")
    return meta


def top_comments(df: pd.DataFrame, label: str, n: int = TOP_N) -> list[dict]:
    subset = df[df["sentiment"] == label].sort_values("score", ascending=False)
    return subset.head(n).to_dict(orient="records")


@app.get("/")
def home(request: Request):
    total = positive = neutral = negative = 0
    positive_pct = neutral_pct = negative_pct = 0.0
    random_comments, top_positive, top_negative, top_neutral = [], [], [], []
    has_data = False

    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            df = df.dropna(subset=["comment"])
            df["sentiment"] = df["sentiment"].astype(str)
            df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)

            total = len(df)

            if total > 0:
                has_data = True
                positive = int((df["sentiment"] == "positive").sum())
                neutral = int((df["sentiment"] == "neutral").sum())
                negative = int((df["sentiment"] == "negative").sum())

                positive_pct = round((positive / total) * 100, 1)
                neutral_pct = round((neutral / total) * 100, 1)
                negative_pct = round((negative / total) * 100, 1)

                sample_size = min(RANDOM_SAMPLE_SIZE, total)
                random_comments = df.sample(n=sample_size).to_dict(orient="records")

                top_positive = top_comments(df, "positive")
                top_negative = top_comments(df, "negative")
                top_neutral = top_comments(df, "neutral")
        except Exception as e:
            print(f"Error reading {DATA_FILE}: {e}")

    video = load_video_meta()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "has_data": has_data,
            "total": total,
            "positive": positive,
            "neutral": neutral,
            "negative": negative,
            "positive_pct": positive_pct,
            "neutral_pct": neutral_pct,
            "negative_pct": negative_pct,
            "random_comments": random_comments,
            "top_positive": top_positive,
            "top_negative": top_negative,
            "top_neutral": top_neutral,
            "video": video,
        },
    )


@app.get("/download")
def download_comments():
    if not os.path.exists(DATA_FILE):
        return JSONResponse(
            status_code=404,
            content={"error": "No analyzed comments yet. Run the pipeline first."},
        )
    return FileResponse(
        path=DATA_FILE,
        filename="pulsescope_comments.csv",
        media_type="text/csv",
    )
