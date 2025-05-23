from datetime import timedelta
import sqlite3
import config


def creat_table():
    """
    Opens a database connection and creates the necessary table if it doesn't exist.
    
    Returns:
        None
    """
    con = sqlite3.connect("companies_stocks.db")
    c = con.cursor()

    create_table_command = """
    CREATE TABLE IF NOT EXISTS company_stock_price(
                        company_symbol NOT NULL,
                        price REAL NOT NULL,
                        date_and_time TEXT NOT NULL,
                        PRIMARY KEY (company_symbol,date_and_time)
                        );
                        """
    c.execute(create_table_command)
    con.commit()
    con.close()

def insert_row(data):
    """
    Adds a row of data to the database with stock price information.
    
    Args:
        data (tuple): A tuple containing (company_symbol, price, date_and_time)
    
    Returns:
        None
    """
    con = sqlite3.connect("companies_stocks.db")
    c = con.cursor()
    c.execute("INSERT OR IGNORE INTO company_stock_price VALUES(?, ?, ?)", data)
    con.commit()
    con.close()


def delete_old_data():
    """
    Erases data older than the configured number of days from the database.
    
    Returns:
        None
    """
    con = sqlite3.connect("companies_stocks.db")
    c = con.cursor()

    # Calculate the cutoff date (3 days ago in NY time)
    cutoff_date = config.DATE_AND_TIME_NY - timedelta(days=config.DAYS_TO_RETAIN)
    cutoff_str = cutoff_date.strftime("%Y-%m-%d %H:%M:%S%z")

    # Delete data older than the cutoff
    c.execute("""
            DELETE FROM company_stock_price
            WHERE date_and_time < ?
        """, (cutoff_str,))

    con.commit()
    con.close()


def get_price_data(company_symbol) -> list:
    """
    Retrieves stock price history for a specific company.
    
    Args:
        company_symbol (str): The stock symbol of the company (one of the magnificent 7)
    
    Returns:
        list: A list of all stock prices collected for this company, ordered by date
    """
    con = sqlite3.connect("companies_stocks.db")
    c = con.cursor()
    c.execute("""
                SELECT price FROM company_stock_price
                WHERE company_symbol = ?
                ORDER BY date_and_time ASC
        """,(company_symbol,))

    list_of_prices_tupels = c.fetchall()
    con.close()
    list_of_prices =[row[0] for row in list_of_prices_tupels]
    return list_of_prices


