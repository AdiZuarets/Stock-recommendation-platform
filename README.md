
# 📈 Stock Recommendation Platform

A Python application that collects stock price data for the "Magnificent 7" tech companies, stores it in a local database, and analyzes them for the "cup and handle" pattern — a popular technical indicator in stock trading. The application exposes an API for querying results.

---

## ⚙️ Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/stock-recommendation-platform.git
   cd stock-recommendation-platform
   ```

2. Create a virtual environment (recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

### Running the Stock Sampler

The stock sampler collects data from Yahoo Finance every 5 minutes when the market is open:

```bash
python -m app.stock_sampler
```

This will:

- Create the database if it doesn't exist
- Collect initial data for all companies in the Magnificent 7
- Schedule data collection every 5 minutes
- Remove data older than 3 days (configurable in `app/config.py`)

### Running the API

Once the data collection is running, start the API server:

```bash
python -m app.API
```

The API will be available at:  
[http://localhost:5000](http://localhost:5000)

---

## 🔌 API Endpoints

| Endpoint | Method | Description | Example |
|---------|--------|-------------|---------|
| `/is-handle-and-cup/{company_symbol}` | GET | Checks if the given company's stock shows a cup and handle pattern | `/is-handle-and-cup/AAPL` |

### Example Response

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

- AI assistance (GPT) was used in development. Prompt history will be shared separately by email.
- Ensure `companies_stocks.db` is excluded from Git tracking using `.gitignore`.
