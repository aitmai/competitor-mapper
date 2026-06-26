# Competitor Mapper

AI-powered competitive intelligence dashboard. Reads startups from Google Sheets, maps their top 5 competitors using Claude, and displays results in a live dark web dashboard.

## Prerequisites

- Python 3.10+
- A Google account
- An Anthropic API key — get one at [console.anthropic.com](https://console.anthropic.com)

---

## Setup

### Step 1 — Clone the repo

```bash
git clone https://github.com/tmaiwebai/competitor-mapper.git
cd competitor-mapper
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Add your Anthropic API key

Create a `.env` file in the project folder:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Step 4 — Set up Google Sheets credentials

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project
3. Enable **Google Sheets API** and **Google Drive API**
4. Go to **APIs & Services → Credentials → Create Credentials → Service Account**
5. Click the service account → **Keys tab → Add Key → Create new key → JSON**
6. Rename the downloaded file to `credentials.json`
7. Move it into the project folder

### Step 5 — Create Google Sheets

Go to [sheets.google.com](https://sheets.google.com) and create two sheets:

- `Competitor-Input` — where you enter startup data
- `Competitor-Map` — where results are written

Share **both sheets** with the service account email from inside `credentials.json` (it looks like `name@project.iam.gserviceaccount.com`) and give it **Editor** access.

### Step 6 — Add data to Competitor-Input

Row 1 must have these exact headers:

```
Company Name | Sector | Description | Website | Stage
```

Add your startups in the rows below. Example:

```
Harvey | AI | AI platform for legal professionals | harvey.ai | Series B
Brex | Fintech | Financial services for startups | brex.com | Series C
Retool | SaaS | Low-code platform for internal tools | retool.com | Series C
```

### Step 7 — Run the app

```bash
python app.py
```

Open your browser at **http://localhost:5000** and click **Run Analysis**.

---

## What It Does

- Reads startups from your `Competitor-Input` Google Sheet
- For each startup, web searches the competitive landscape and sends data to Claude
- Claude identifies the top 5 competitors with funding amounts and threat levels
- Results display in a live dark dashboard with filter by sector and search by company
- Writes all results to your `Competitor-Map` Google Sheet automatically

---

## Project Structure

```
competitor-mapper/
├── app.py                       # Flask web server
├── agents/
│   └── competitor_agent.py      # Web search + Claude analysis
├── sheets/
│   ├── sheets_reader.py         # Reads from Competitor-Input
│   └── sheets_writer.py         # Writes to Competitor-Map
├── templates/
│   └── index.html               # Dashboard UI
├── static/
│   └── style.css                # Dark theme styles
├── requirements.txt
└── .gitignore
```

---

## Security

Never push these files to GitHub — they are already in `.gitignore`:

```
credentials.json
.env
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `No module named sheets` | Make sure `sheets/__init__.py` exists |
| `SpreadsheetNotFound` | Check sheet name matches exactly and service account has Editor access |
| `ANTHROPIC_API_KEY not set` | Check `.env` file exists with correct key |
| `credentials.json not found` | Move file to project root folder |
