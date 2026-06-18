import pandas as pd

df = pd.read_csv("raw_comments.csv")

print("Original Rows:", len(df))

# Remove duplicates
df.drop_duplicates(inplace=True)

# Remove empty rows
df.dropna(inplace=True)

# Remove extra spaces
df["comment"] = df["comment"].str.strip()

# Remove very short comments
df = df[df["comment"].str.len() > 3]

print("Cleaned Rows:", len(df))

df.to_csv(
    "cleaned_comments.csv",
    index=False
)

print("Cleaning completed.")