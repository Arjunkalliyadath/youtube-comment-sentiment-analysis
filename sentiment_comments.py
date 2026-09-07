"""
Runs sentiment analysis on the cleaned comments.

Input:  cleaned_comments.csv (preferred, written by clean_data.py)
        comments.csv         (fallback, if cleaning was skipped)
Output: sentiment_results.csv, read by app.py
"""

import os
import sys

import pandas as pd
from transformers import pipeline

CLEANED_FILE = "cleaned_comments.csv"
RAW_FILE = "comments.csv"
OUTPUT_FILE = "sentiment_results.csv"


def load_comments() -> pd.DataFrame:
    if os.path.exists(CLEANED_FILE):
        return pd.read_csv(CLEANED_FILE)

    if os.path.exists(RAW_FILE):
        print(
            f"{CLEANED_FILE} not found, falling back to {RAW_FILE}. "
            "Run clean_data.py first for better results."
        )
        return pd.read_csv(RAW_FILE)

    sys.exit(
        f"Couldn't find {CLEANED_FILE} or {RAW_FILE}. Run extract_comments.py first."
    )


def main():
    df = load_comments()

    print("Loading model...")
    classifier = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    )

    results = []
    total = len(df)

    for i, comment in enumerate(df["comment"]):
        try:
            prediction = classifier(str(comment)[:512])[0]
            results.append({
                "comment": comment,
                "sentiment": prediction["label"],
                "score": round(prediction["score"], 4),
            })
            print(f"{i + 1}/{total} processed")
        except Exception:
            results.append({
                "comment": comment,
                "sentiment": "UNKNOWN",
                "score": 0,
            })

    result_df = pd.DataFrame(results)
    result_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
