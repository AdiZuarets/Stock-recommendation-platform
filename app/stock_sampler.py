import yfinance as yf
import schedule
from time import sleep
import database
import config


def is_market_open() -> bool:
    """
    Checks if the stock market is currently open based on NY time.
    
    Returns:
        bool: True if the market is open, False if the market is closed
    """
    # Check the day
    if config.DAY_IN_NY >= config.WORK_DAYS:
        return False

    # Check the hour
    open_hour = config.OPEN_HOUR
    close_hour = config.CLOSE_HOUR
    if config.TIME_IN_NY < open_hour or config.TIME_IN_NY > close_hour:
        return False

    return True

def make_the_job():
    """
    Fetches current stock data from Yahoo Finance, stores it in the database,
    and removes old data older than the configured retention period.
    
    Returns:
        None
    """
    # If the market is close return
    if not is_market_open():
        print("Market closed. Skipping.")
        return

    database.delete_old_data()

    companies = config.COMPANIES

    for company in companies:
        ticker = yf.Ticker(company)
        price = ticker.history(period="1d", interval="5m")
        # if something went wrong with the website
        if price.empty:
            print(f"{company}: No data.")
            continue

        # we want the last price in the interval
        last_price = price["Close"].iloc[-1]
        # the time to save also
        last_time = price.index[-1]

        data = (company, last_price, str(last_time))
        database.insert_row(data)
        print(f"{company} at {last_time}: {last_price}")


if __name__ == "__main__":
    """
    Main function that initializes the database and schedules regular data collection.
    """
    database.creat_table()
    make_the_job()
    schedule.every(config.FETCH_INTERVAL_MINUTES).minutes.do(make_the_job)

    while True:
        schedule.run_pending()
        sleep(1)