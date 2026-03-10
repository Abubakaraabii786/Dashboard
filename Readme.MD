# MWF Financial Dashboard

A full-featured, interactive financial dashboard for Muslim Welfare Foundation built with Streamlit and Plotly.

---

## 🚀 Deploy to Streamlit Cloud (FREE — 5 minutes)

### Step 1 — Push to GitHub
1. Create a new repo at https://github.com/new (e.g. `mwf-dashboard`)
2. Upload both files: `app.py` and `requirements.txt`

### Step 2 — Deploy on Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repo → branch `main` → file `app.py`
5. Click **Deploy** → your dashboard will be live at:
   `https://<your-app-name>.streamlit.app`

---

## 🔗 Connect Your Google Sheet

1. Open your Google Sheet
2. Click **Share** → **Anyone with the link** → **Viewer**
3. Copy the share URL
4. Paste it into the **"Google Sheet URL"** box in the sidebar

> The URL should look like:
> `https://docs.google.com/spreadsheets/d/1AbCdEfG.../edit?usp=sharing`

### Required Column Names
Your Google Sheet must have these columns (same as the sample data):
- `TRANSACTION PRIMARY KEY`
- `DATE` (format: DD-Mon-YYYY, e.g. 14-Mar-2023)
- `YEAR`, `MONTH`
- `CONVERTED AMOUNT (GBP)`
- `ITEM`, `ITEM HEAD 1`, `ITEM HEAD 2`
- `TRANSACTION FORUM`
- `POSTCODE ZONE`, `LINK CLUSTER CITY`
- `HIJRI MONTH NAME`, `HIJRI DATE`

---

## 📊 Dashboard Features

| Feature | Details |
|---|---|
| 📋 **Data Source** | Switch between sample data and live Google Sheet |
| 📅 **Year Filter** | Select any year in the data |
| 🗓️ **Month Filter** | Filter by calendar month |
| 🏷️ **Category Filter** | Filter by donation category |
| 📍 **Zone Filter** | Filter by geographic zone |
| 🏛️ **Forum Filter** | Filter by transaction forum |
| 💷 **KPI Cards** | Total, Count, Average, Max with YoY delta |
| 📈 **Trend Line** | Monthly donations vs previous year |
| 🥧 **Category Pie** | Donation breakdown by category |
| 📊 **Year Comparison** | Side-by-side bar charts same period last year |
| 🕌 **Hijri Analysis** | Donations by Islamic calendar month |
| 🔍 **Search** | Full-text search across transactions |
| ⬇️ **CSV Export** | Download filtered data |

---

## 🖥️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## 🎨 Tech Stack
- **Streamlit** — Web framework
- **Plotly** — Interactive charts
- **Pandas** — Data processing
- **Google Sheets** — Live data source (public CSV export)