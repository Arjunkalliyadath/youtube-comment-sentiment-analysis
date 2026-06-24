# Social Media Data Collection & Sentiment Analysis

## Project Overview

This project collects user comments from social media platforms and performs sentiment analysis using Natural Language Processing (NLP).

Currently implemented:

- YouTube Comment Extraction
- Twitter/X Comment Extraction
- Data Cleaning
- Sentiment Analysis
- Dashboard Visualization using FastAPI

The system helps organizations understand public opinion, customer feedback, and social media engagement.

---

## Technologies Used

### Backend

- Python
- FastAPI
- Playwright

### Data Processing

- Pandas

### NLP

- Hugging Face Transformers
- CardiffNLP Twitter RoBERTa Sentiment Model

### Frontend

- HTML
- CSS
- Jinja2 Templates

---

## Project Structure

```text
social_media_data_collection/
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
├── extract_comments.py
├── clean_data.py
├── sentiment_comments.py
├── app.py
│
├── comments.csv
├── sentiment_results.csv
│
├── requirements.txt
└── README.md
```

---

## Workflow

### Step 1 – Data Collection

Comments are collected using Playwright.

Supported Platforms:

- YouTube
- Twitter / X

Future Platforms:

- Google Reviews
- Instagram

---

### Step 2 – Data Cleaning

The collected comments are cleaned by:

- Removing duplicates
- Removing empty values
- Removing extra spaces
- Filtering short comments

---

### Step 3 – Sentiment Analysis

Each comment is analyzed using:

```python
cardiffnlp/twitter-roberta-base-sentiment-latest
```

Predicted Classes:

- Positive
- Neutral
- Negative

---

### Step 4 – Dashboard

FastAPI displays:

- Total Comments
- Positive Comments
- Neutral Comments
- Negative Comments
- Sentiment Percentages
- Comment Table

---

## Installation

Clone repository:

```bash
git clone <repository-url>
cd social_media_data_collection
```

Create virtual environment:

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright Browser:

```bash
playwright install
```

---

## Run Comment Extraction

```bash
python extract_comments.py
```

Output:

```text
comments.csv
```

---

## Run Sentiment Analysis

```bash
python sentiment_comments.py
```

Output:

```text
sentiment_results.csv
```

---

## Run Dashboard

```bash
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## Sample Output

Dashboard displays:

- Total Comments Analyzed
- Positive Percentage
- Neutral Percentage
- Negative Percentage
- Individual Comment Sentiments

---

## Future Enhancements

- Instagram Comment Extraction
- Google Reviews Extraction
- Unified Multi-Platform Dashboard
- Data Export to Excel
- Sentiment Trend Visualization
- Company Reputation Monitoring

---

## Author

Arjun K
