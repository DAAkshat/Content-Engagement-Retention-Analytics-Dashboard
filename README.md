# Content Engagement & Retention Analytics Dashboard

Portfolio project simulating audio platform analytics (Pocket FM-style).

## Stack

- **Backend:** Python, Flask, SQLite, Pandas, NumPy, SciPy
- **Frontend:** HTML, CSS, JavaScript, Chart.js

## Setup

```bash
pip install flask pandas numpy scipy
python database/load_data.py   # generate data + load SQLite
python app.py                  # http://localhost:5000
```

## Structure

```
├── data/generate_data.py      # Synthetic dataset (10k users, 90 days)
├── database/schema.sql        # users, sessions, notifications
├── database/load_data.py      # Load CSVs into SQLite
├── analytics/queries.py       # DAU, MAU, churn, A/B test, cohorts
├── app.py                     # Flask API + dashboard
├── templates/index.html       # Dark-themed dashboard
└── static/dashboard.js        # Chart.js visualizations
```

## API Endpoints

| Endpoint | Description |
|---|---|
| `/api/kpis` | Summary KPI cards |
| `/api/dau` | Daily active users |
| `/api/mau` | Monthly active users |
| `/api/genre` | Genre completion rates |
| `/api/churn` | High-churn % by genre |
| `/api/abtest` | Notification A/B test + chi-square |
| `/api/mau-trend` | MAU over time |
| `/api/premium-vs-free` | Premium vs free comparison |
| `/api/genre-funnel` | Completion funnel by genre |
| `/api/cohort-heatmap` | Week-by-week retention heatmap |
