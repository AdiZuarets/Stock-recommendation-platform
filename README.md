# 📈 Stock Recommendation Platform

A Python application that collects stock price data for the "Magnificent 7" tech companies, stores it in a local SQLite database, and analyzes it for the **cup and handle** pattern — a popular technical indicator in stock trading. The application exposes an API for querying detection results.

---

## ⚙️ Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/AdiZuarets/stock-recommendation-platform.git
   cd stock-recommendation-platform
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

### Running the Stock Sampler

The stock sampler collects data from Yahoo Finance every 5 minutes during U.S. market hours.

```bash
python -m app.stock_sampler
```

This will:
- Create the database if it doesn't exist
- Collect initial data for all companies in the Magnificent 7
- Schedule automatic data collection every 5 minutes
- Remove data older than 3 days (configurable in `app/config.py`)

---

### Running the API

Once the data collection is running (by running the stock sampler in another terminal), start the API server:

```bash
python -m app.API
```

This will launch a local API server on your machine.

🔎 To test it, open your browser and visit:

```
http://127.0.0.1:5000/is-handle-and-cup/AAPL
```

If that doesn’t work, try:

```
http://localhost:5000/is-handle-and-cup/AAPL
```

This will ask the API:  
“Does the stock for AAPL match the cup-and-handle pattern?”

---

## 🔌 API Endpoints

| Endpoint                          | Method | Description                                                  | Example                     |
|-----------------------------------|--------|--------------------------------------------------------------|-----------------------------|
| `/is-handle-and-cup/{symbol}`    | GET    | Checks if the stock for `{symbol}` shows a cup & handle pattern | `/is-handle-and-cup/AAPL`  |

### Example Response:
```json
{
  "Company": "AAPL",
  "is cup and handle": true
}
```

---

## 🛠 Configuration

Edit `app/config.py` to modify:
- Market open/close hours
- Data retention period (in days)
- Minimum number of data points required for pattern detection
- List of companies to track

---

## 📁 Project Structure

```
stock-recommendation-platform/
├── app/
│   ├── stock_sampler.py       # Data collection from Yahoo Finance
│   ├── API.py                 # REST API with Flask
│   ├── config.py              # Configuration for timing, companies, etc.
│   ├── cup_and_handle.py      # Pattern detection logic
│   ├── Database.py            # SQLite interaction
│   └── __init__.py
│
├── data/
│   └── companies_stocks.db    # Local SQLite database (gitignored)
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧠 Notes

- The database file `companies_stocks.db` is excluded from Git tracking via `.gitignore`.
- This app is designed to run **completely locally** — no cloud or third-party storage involved.
