"""
Cleans the raw scraped comments so sentiment_comments.py has good input.

Input:  comments.csv          (written by extract_comments.py)
Output: cleaned_comments.csv  (read by sentiment_comments.py)
"""

import sys

import pandas as pd

INPUT_FILE = "comments.csv"
OUTPUT_FILE = "cleaned_comments.csv"


def main():
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        sys.exit(
            f"Couldn't find {INPUT_FILE}. Run extract_comments.py first."
        )

    print("Original Rows:", len(df))

    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    df["comment"] = df["comment"].str.strip()
    df = df[df["comment"].str.len() > 3]

    print("Cleaned Rows:", len(df))

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Cleaning completed. Saved {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
