# Logistics Insight Engine

An automated fleet performance analysis system that helps transport 
and logistics businesses identify operational inefficiencies, reduce 
fuel costs, and improve delivery reliability using Python and AI.

## The Problem

Most small and mid-sized transport companies manage fleet performance 
through spreadsheets. Managers manually calculate delivery rates, 
compare routes one by one, and try to spot trends across dozens of 
trips. This takes hours, invites errors, and makes it easy to miss 
critical issues like a consistently delayed driver or an 
underperforming route draining fuel costs.

## The Solution

Logistics Insight Engine automates the entire analysis process. 
Feed it your fleet data and it produces a complete performance 
report with AI-generated recommendations in seconds.

## What You Get

- Overall delivery rate and fuel cost summary
- Route performance breakdown identifying best and worst routes
- Driver performance ranking with delay analysis
- Vehicle efficiency comparison
- AI-generated executive insight with specific operational recommendations
- Professional PDF report ready to share with management

## Tech Stack
- Python
- Pandas
- Groq AI API (LLaMA 3.3)
- ReportLab (PDF generation)

## Project Structure
```text
logistics-insight-engine/
│
├── analyzer.py        # Core fleet performance engine
├── ai_insights.py     # Groq AI consultant integration
├── report.py          # Report orchestrator
├── pdf_exporter.py    # PDF generation
├── config.py          # Credentials (excluded from Git)
│
├── templates/
│   └── ai_insights_template.py
│
└── data/
    └── logistics_data.csv
```

## How To Run

Install dependencies:
```bash
pip install pandas reportlab groq
```

Add your credentials to `config.py`:
```python
GROQ_API_KEY = "your_key_here"
GROQ_MODEL = "llama-3.3-70b-versatile"
```

Run the full report:
```bash
python report.py
```

## Sample Output
```text
==================================================
   LOGISTICS PERFORMANCE ANALYSIS
==================================================
  Delivery Rate         : 90.5%
  Total Fuel Cost       : KES 89,100
  Total Distance        : 4,230 km
  Avg Delay             : 20.3 mins
  Best Route            : Mombasa-Malindi
  Worst Route           : Nairobi-Eldoret
  Best Driver           : Peter Otieno
  Most Delayed Driver   : Samuel Kamau
==================================================
```

## Security
Credentials are stored in `config.py` which is excluded 
from version control via `.gitignore`. Never commit API 
keys or passwords to GitHub.

## Business Use Case
Built specifically for SME transport and logistics operators 
in East Africa where manual fleet tracking creates operational 
blind spots and unnecessary cost overruns.