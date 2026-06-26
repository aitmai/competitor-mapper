# Competitor Mapper

AI-powered competitive intelligence dashboard. Reads startups from Google Sheets, maps their top 5 competitors using Claude, and displays results in a live dark web dashboard.

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add credentials
- Copy `credentials.json` from your Google Cloud service account into this folder
- Copy `.env` and set your `ANTHROPIC_API_KEY`

### 3. Create Google Sheets
Create two sheets and share both with your service account email (Editor):
- `Competitor-Input` — input data
- `Competitor-Map` — output results

### 4. Add headers to Competitor-Input
Row 1 must have exactly:
Company Name | Sector | Description | Website | Stage

### 5. Run the app
```bash
python app.py
```

Open your browser at: http://localhost:5000

Click Run Analysis to start.

## Project Structure
```
competitor-mapper/
├── app.py
├── agents/competitor_agent.py
├── sheets/sheets_reader.py
├── sheets/sheets_writer.py
├── templates/index.html
├── static/style.css
├── requirements.txt
└── .gitignore
```
