# Content Engagement & Retention Analytics Dashboard
## Complete Project Guide

---

## 1. What Is This Project?

This is a **full-stack analytics dashboard** that simulates how an audio OTT platform (like **Pocket FM**) tracks user behavior, content engagement, and retention.

It is built as a **portfolio project** for Growth Analyst / Data Analyst roles. It demonstrates:

- End-to-end data pipeline (generate → store → query → visualize)
- Product metrics that real growth teams use (DAU, MAU, cohort retention, A/B tests)
- SQL + Python analytics with statistical testing (chi-square)
- A clean, dark-themed dashboard for stakeholders

**Important:** All data is **synthetic** (fake but realistic). No real users or API keys are involved.

---

## 2. How to Run the Project

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1 — Install dependencies

Open a terminal in the project folder and run:

```powershell
cd c:\Users\aktri\Desktop\analytics_dashboard
pip install flask pandas numpy scipy
```

| Package | Purpose |
|---------|---------|
| `flask` | Web server and REST API |
| `pandas` | Data manipulation and SQL queries |
| `numpy` | Random number generation for synthetic data |
| `scipy` | Chi-square statistical test for A/B testing |

### Step 2 — Generate data and load the database

```powershell
python database/load_data.py
```

This command does two things:
1. Runs `data/generate_data.py` if CSV files don't exist yet
2. Creates `analytics.db` (SQLite database) and loads all data into it

**Expected output:**
```
Generated 10000 users, ~75000 sessions, 10000 notifications
Database loaded at ...\analytics_dashboard\analytics.db
```

### Step 3 — Start the web server

```powershell
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
```

### Step 4 — Open the dashboard

Go to your browser and visit:

```
http://localhost:5000
```

You should see the dark-themed dashboard with KPI cards, charts, and the retention heatmap.

---

## 3. What Happens When You Run It? (Data Flow)

```
┌─────────────────────┐
│  generate_data.py   │  Creates fake users, sessions, notifications
│  (data/)            │  Saves as CSV files in data/
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  load_data.py       │  Reads CSVs, applies schema.sql
│  (database/)        │  Writes everything into analytics.db
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  queries.py         │  Runs SQL + pandas analytics
│  (analytics/)       │  Returns JSON-ready metrics
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  app.py (Flask)     │  Serves /api/* endpoints
│                     │  Serves dashboard at /
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  index.html +       │  Fetches API data, renders Chart.js
│  dashboard.js       │  charts and heatmap table
└─────────────────────┘
```

**On first request:** If `analytics.db` doesn't exist, Flask automatically calls `load_data.py` before serving any page.

---

## 4. Project File Structure — What Each File Does

```
analytics_dashboard/
│
├── data/
│   ├── generate_data.py     ← Creates synthetic dataset
│   ├── users.csv            ← Generated (10,000 users)
│   ├── sessions.csv         ← Generated (~75,000 listening sessions)
│   └── notifications.csv    ← Generated (A/B test records)
│
├── database/
│   ├── schema.sql           ← SQL table definitions
│   └── load_data.py         ← Loads CSVs into SQLite
│
├── analytics/
│   └── queries.py           ← All analytics logic (SQL + stats)
│
├── templates/
│   └── index.html           ← Dashboard HTML + CSS
│
├── static/
│   └── dashboard.js         ← Fetches APIs, builds charts
│
├── app.py                   ← Flask web server + API routes
├── analytics.db             ← SQLite database (auto-created)
├── README.md                ← Quick setup guide
└── EXPLANATION.md           ← This file
```

---

## 5. Database Schema (3 Tables)

### `users` — Who signed up

| Column | Type | Description |
|--------|------|-------------|
| `user_id` | INTEGER | Unique user ID (1 to 10,000) |
| `signup_date` | TEXT | Date user joined (within 90-day window) |
| `preferred_genre` | TEXT | Romance, Thriller, Fantasy, Horror, or Comedy |
| `is_premium` | INTEGER | 0 = Free user, 1 = Premium subscriber |

### `sessions` — Each time a user listens

| Column | Type | Description |
|--------|------|-------------|
| `session_id` | INTEGER | Unique session ID |
| `user_id` | INTEGER | Which user listened |
| `session_date` | TEXT | Date of the session |
| `genre` | TEXT | Genre of content played |
| `episode_completion_rate` | REAL | 0.0 to 1.0 (how much of episode was finished) |
| `session_duration_mins` | REAL | Minutes spent listening |
| `episodes_played` | INTEGER | Number of episodes in that session |

### `notifications` — Push notification A/B test

| Column | Type | Description |
|--------|------|-------------|
| `user_id` | INTEGER | User who received notification |
| `ab_group` | TEXT | "A" = generic message, "B" = cliffhanger message |
| `sent_date` | TEXT | When notification was sent |
| `re_engaged` | INTEGER | 1 = user came back, 0 = did not return |

---

## 6. Synthetic Data — How It's Generated

File: `data/generate_data.py`

| Setting | Value |
|---------|-------|
| Users | 10,000 |
| Time window | 90 days (Jan 1 – Mar 31, 2024) |
| Genres | Romance, Thriller, Fantasy, Horror, Comedy |
| Premium split | 30% premium, 70% free |
| Sessions per user | Random 1–14 sessions each |
| Completion rate | Beta distribution (realistic bell curve around 50%) |
| A/B groups | Even split: even user_ids → Group A, odd → Group B |
| Re-engagement rates | Group A: ~12%, Group B: ~18% (cliffhanger wins) |

**Random seed is fixed (`42`)** so the same data is generated every time — useful for demos and reproducibility.

---

## 7. Dashboard Layout — What You See on Screen

```
┌──────────────────────────────────────────────────────────────────┐
│  ROW 1: KPI Cards                                                │
│  [Total Sessions] [Avg DAU] [Avg Completion %] [Churn %]         │
├─────────────────────────────┬────────────────────────────────────┤
│  ROW 2: DAU Line Chart      │  Genre Engagement Bar Chart        │
├─────────────────────────────┼────────────────────────────────────┤
│  ROW 3: Churn Bar Chart     │  A/B Test Results                  │
├─────────────────────────────┼────────────────────────────────────┤
│  ROW 4: MAU Trend Line        │  Premium vs Free Bar Chart         │
├─────────────────────────────┴────────────────────────────────────┤
│  ROW 5: Genre Completion Funnel (full width)                     │
├──────────────────────────────────────────────────────────────────┤
│  ROW 6: Retention Cohort Heatmap (full width)                    │
└──────────────────────────────────────────────────────────────────┘
```

**Color theme:**
- Background: `#0f172a` (dark navy)
- Cards: `#1e293b` (slate gray)
- Accent: `#3b82f6` (blue)
- MAU chart: `#8b5cf6` (purple)

---

## 8. Every Metric Explained

### KPI Cards (top row)

| KPI | What it means | How it's calculated |
|-----|---------------|---------------------|
| **Total Sessions** | Platform activity volume | `COUNT(*)` from sessions table |
| **Avg DAU** | Average daily active users | Average of daily distinct user counts |
| **Avg Completion %** | How much content users finish | Average of `episode_completion_rate × 100` |
| **Churn %** | Sessions where user dropped off early | % of sessions with completion rate < 25% |

### DAU Line Chart
- **DAU** = Daily Active Users
- Counts **unique users** who had at least one session each day
- Shows platform health over the 90-day period
- Growth teams watch this daily for spikes or drops

### Genre Engagement Bar Chart
- Average episode completion rate (%) per genre
- Answers: *"Which genres keep users listening longest?"*
- Used for content commissioning decisions

### Churn by Genre Bar Chart
- % of sessions per genre where completion was below 25%
- High churn = users started but quickly stopped
- Answers: *"Which genres lose listeners fastest?"*

### A/B Test — Notifications
- **Group A:** Generic push notifications (~12% re-engagement)
- **Group B:** Cliffhanger notifications (~18% re-engagement)
- Uses **chi-square test** (from SciPy) to check if the difference is statistically significant (p < 0.05)
- Green badge = significant result; yellow = not significant

### MAU Trend Line Chart
- **MAU** = Monthly Active Users
- Unique users per calendar month
- Shows longer-term growth vs DAU's daily view

### Premium vs Free Bar Chart
Compares three metrics between subscription tiers:
- Average completion rate (%)
- Average session duration (minutes)
- Average episodes played per session

Answers: *"Do premium users engage more deeply with content?"*

### Genre Completion Funnel
For each genre, shows how many sessions reached each stage:
```
Total Plays → 25% complete → 50% → 75% → 100% (Completed)
```
Shows drop-off at each stage — like a marketing funnel but for content consumption.

### Retention Cohort Heatmap
- **Rows:** User cohorts grouped by signup week
- **Columns:** Weeks since signup (W0, W1, W2 … W8)
- **Cell color:** Green = high retention, Red = low retention
- **W0 always = 100%** (by definition, all users are "active" in their signup week)
- Answers: *"Are newer cohorts retaining better or worse than older ones?"*

---

## 9. API Endpoints Reference

All endpoints return JSON. Base URL: `http://localhost:5000`

| Endpoint | Returns |
|----------|---------|
| `GET /` | Dashboard HTML page |
| `GET /api/kpis` | `{ total_sessions, avg_dau, avg_completion, churn_pct }` |
| `GET /api/dau` | `[{ session_date, dau }, ...]` |
| `GET /api/mau` | `{ mau: number }` |
| `GET /api/genre` | `[{ genre, avg_completion, sessions }, ...]` |
| `GET /api/churn` | `[{ genre, churn_pct }, ...]` |
| `GET /api/abtest` | `{ groups, chi2, p_value, significant }` |
| `GET /api/retention` | `[{ signup_date, week, user_id, retention }, ...]` |
| `GET /api/mau-trend` | `[{ month, mau }, ...]` |
| `GET /api/cohort-heatmap` | `{ cohorts, weeks, values }` |
| `GET /api/genre-funnel` | `{ "Romance": [total, 25%, 50%, 75%, done], ... }` |
| `GET /api/premium-vs-free` | `[{ label, avg_completion, avg_duration, avg_episodes }, ...]` |

**Test an endpoint in browser or terminal:**
```
http://localhost:5000/api/kpis
```

---

## 10. How the Frontend Works

File: `static/dashboard.js`

1. On page load, calls `init()`
2. Fetches all 9 API endpoints in parallel using `Promise.all`
3. Renders KPI cards as HTML
4. Creates Chart.js charts (line, bar) on `<canvas>` elements
5. Builds the cohort heatmap as an HTML table with color-coded cells

File: `templates/index.html`

- Contains all CSS styling (dark theme, grid layout)
- Defines the HTML structure for cards and chart containers
- Loads Chart.js from CDN (no local install needed)
- Basic mobile responsiveness (single column on screens < 768px)

---

## 11. Business Context — Why Each Feature Matters

This maps directly to real growth team workflows at audio/content platforms:

| Dashboard Feature | Real-World Use Case |
|-------------------|---------------------|
| DAU / MAU | Platform health monitoring, board reporting |
| Genre engagement | Content commissioning — which genres to produce more of |
| Churn by genre | Identify underperforming content categories |
| Cohort heatmap | Retention strategy — are product changes improving stickiness? |
| A/B test | Notification campaign optimization |
| Premium vs Free | Subscription conversion insights — justify premium pricing |
| Completion funnel | Episode-level drop-off analysis for content editors |

---

## 12. How to Talk About This in an Interview

**One-liner:**
> "I built a full-stack analytics dashboard simulating an audio OTT platform, with synthetic data for 10K users over 90 days, SQL analytics, chi-square A/B testing, and a Chart.js dashboard."

**Key points to mention:**
1. **Data pipeline:** Python generates data → SQLite stores it → Pandas queries it → Flask serves it → JS visualizes it
2. **Metrics choice:** Chose DAU/MAU, cohorts, and A/B tests because they're standard growth team KPIs
3. **Statistical rigor:** A/B test uses chi-square, not just raw rate comparison
4. **Product thinking:** Every chart answers a specific business question
5. **Tech choices:** SQLite for simplicity (no server setup), Flask for lightweight API, Chart.js for quick visualizations

---

## 13. Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install flask pandas numpy scipy` |
| Dashboard shows empty charts | Check terminal for errors; ensure `analytics.db` exists |
| Port 5000 already in use | Stop other Flask apps or change port in `app.py` |
| Want fresh data | Delete `data/*.csv` and `analytics.db`, then run `python database/load_data.py` |
| `&&` doesn't work in PowerShell | Use `;` instead: `pip install flask; python app.py` |

---

## 14. Regenerating Data

To create a completely new dataset:

```powershell
# Delete old files
Remove-Item data\*.csv
Remove-Item analytics.db

# Regenerate
python database/load_data.py
python app.py
```

---

## 15. Tech Stack Summary

| Layer | Technology |
|-------|------------|
| Language | Python 3 |
| Web framework | Flask |
| Database | SQLite |
| Data processing | Pandas, NumPy |
| Statistics | SciPy (chi-square) |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js (CDN) |
| Data | Synthetic (10K users, 90 days, 5 genres) |

---

*Built as a portfolio project demonstrating growth analytics for audio/content platforms.*
