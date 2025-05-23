from datetime import datetime, time
import pytz

# Market Configuration
# -------------------
# Time settings for when the market is open (New York time)
OPEN_HOUR = time(9, 30)  # Market opens at 9:30 AM
CLOSE_HOUR = time(16, 00)  # Market closes at 4:00 PM
WORK_DAYS = 5  # Trading days per week (Monday-Friday)

# Data Management
# ---------------
DAYS_TO_RETAIN = 3  # Keep data for this many days before deletion
MINIMUM_DATA_POINTS = 5  # Minimum data points required for pattern detection
FETCH_INTERVAL_MINUTES = 5  # Interval (in minutes) between stock data fetches

# Time Zone Configuration
# ----------------------
TIME_ZONE_NY = pytz.timezone("America/New_York")
DATE_AND_TIME_NY = datetime.now(TIME_ZONE_NY)
TIME_IN_NY = DATE_AND_TIME_NY.time()
DAY_IN_NY = datetime.now(TIME_ZONE_NY).weekday()

# Companies to Track
# -----------------
# The "Magnificent 7" tech companies
COMPANIES = {
    "AAPL",  # Apple
    "MSFT",  # Microsoft
    "GOOGL", # Alphabet (Google)
    "AMZN",  # Amazon
    "NVDA",  # NVIDIA
    "META",  # Meta Platforms (Facebook)
    "TSLA"   # Tesla
}
