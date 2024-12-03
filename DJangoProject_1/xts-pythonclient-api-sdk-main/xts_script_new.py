import os
import logging
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine
import psycopg2
from Connect import XTSConnect

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d"
)


def xts_login(api_key, api_secret, source, is_market_data=False):
    """
    Log in to the XTSConnect API and return the connection object.

    Args:
        api_key (str): API key for authentication.
        api_secret (str): API secret for authentication.
        source (str): Source identifier (e.g., 'WEBAPI').
        is_market_data (bool): Indicates if it is a market data login.

    Returns:
        XTSConnect: The connected object or None if login fails.
    """
    xt = XTSConnect(api_key, api_secret, source)
    login_func = xt.marketdata_login if is_market_data else xt.interactive_login
    login_response = login_func()

    if login_response and login_response.get('type') == 'success':
        logging.info(f"{'Marketdata' if is_market_data else 'Interactive'} login successful.")
        return xt
    else:
        logging.error(f"{'Marketdata' if is_market_data else 'Interactive'} login failed.")
        return None


def get_master_instruments(xtm, exchange_segments, output_path):
    """
    Fetch master instruments data and save it as a CSV file.

    Args:
        xtm (XTSConnect): The connected XTSConnect object.
        exchange_segments (list): List of exchange segment identifiers.
        output_path (str): Path to save the CSV file.
    """
    master_response = xtm.get_master(exchangeSegmentList=exchange_segments)

    if 'result' in master_response:
        try:
            master_df = pd.read_csv(
                StringIO(master_response['result']),
                sep='|',
                usecols=range(19),
                header=None,
                low_memory=False
            )

            # Assign column names to the DataFrame
            master_df.columns = [
                "ExchangeSegment", "ExchangeInstrumentID", "InstrumentType", "Name", "Description", "Series",
                "NameWithSeries", "InstrumentID", "PriceBand.High", "PriceBand.Low", "FreezeQty", "TickSize",
                "LotSize", "Multiplier", "UnderlyingInstrumentId", "UnderlyingIndexName", "ContractExpiration",
                "StrikePrice", "OptionType",
            ]

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            master_df.to_csv(output_path, index=False)
            logging.info(f"Master response data saved to {output_path}")
        except Exception as e:
            logging.error(f"Error processing or saving master response: {e}")
    else:
        logging.error("Error: 'result' not found in the master response.")


def insert_data_to_db(csv_path, db_details, table_name):
    """
    Insert data from a CSV file into a PostgreSQL database.

    Args:
        csv_path (str): Path to the CSV file.
        db_details (dict): Database connection details.
        table_name (str): Name of the table to insert data into.
    """
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(csv_path)
        logging.info(df.head())

        # Using SQLAlchemy for database insertion
        engine = create_engine(
            f"postgresql://{db_details['user']}:{db_details['password']}"
            f"@{db_details['host']}:{db_details['port']}/{db_details['dbname']}"
        )
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info("Data inserted successfully.")
    except Exception as e:
        logging.error(f"Error inserting data to the database: {e}")


def main():
    # API Credentials
    API_KEY = "1afed370a1e58f2d831865"
    API_SECRET = "Qwnk201#P5"
    API_KEY_MARKET = "5575c6bfcff03735044479"
    API_SECRET_MARKET = "Iyqi743$bb"
    SOURCE = "WEBAPI"

    # Database details
    DB_DETAILS = {
        'host': 'localhost',
        'port': '5432',
        'dbname': 'MarketData',
        'user': 'postgres',
        'password': 'admin'
    }

    # File paths
    OUTPUT_PATH = 'D:\\XTS_Project_Learning\\python_xts_env\\xts-pythonclient-api-sdk-main\\master_response.csv'

    # Login to Interactive API
    xt = xts_login(API_KEY, API_SECRET, SOURCE)
    if not xt:
        return

    # Login to Marketdata API
    xtm = xts_login(API_KEY_MARKET, API_SECRET_MARKET, SOURCE, is_market_data=True)
    if not xtm:
        return

    # Fetch and save master instruments
    exchange_segments = [xtm.EXCHANGE_NSECM, xtm.EXCHANGE_NSEFO]
    get_master_instruments(xtm, exchange_segments, OUTPUT_PATH)

    # Insert data into the database
    insert_data_to_db(OUTPUT_PATH, DB_DETAILS, 'master_instruments')


if __name__ == "__main__":
    main()



# Output:
# D:\XTS_Project_Learning\python_xts_env\xts-pythonclient-api-sdk-main>python xts_script_new.py
# 2024-11-29 16:40:57,439 - INFO - Interactive login successful. - xts_script_new.py:34
# 2024-11-29 16:40:57,862 - INFO - Marketdata login successful. - xts_script_new.py:34
# 2024-11-29 16:41:02,787 - INFO - Master response data saved to D:\XTS_Project_Learning\python_xts_env\xts-pythonclient-api-sdk-main\master_response.csv - xts_script_new.py:72
# D:\XTS_Project_Learning\python_xts_env\xts-pythonclient-api-sdk-main\xts_script_new.py:90: DtypeWarning: Columns (14,17,18) have mixed types. Specify dtype option on import or set low_memory=False.
# df = pd.read_csv(csv_path)
# 2024-11-29 16:41:02,990 - INFO -   ExchangeSegment  ExchangeInstrumentID  InstrumentType        Name  ... UnderlyingIndexName ContractExpiration StrikePrice                    OptionType
# 0           NSECM                  1153               8       GLAXO  ...        INE159A01016                  1           1  GLAXOSMITHKLINE PHARMA LT-EQ
# 1           NSECM                 25170               8  NAMOEWASTE  ...        INE08NZ01012                  1           1   NAMO EWASTE MANAGEMENT L-ST
# 2           NSECM                 23583               8     755PN32  ...        IN2820240033                  1           1          SDL PN 7.55% 2032-SG
# 3           NSECM                 21074               8  SUPREMEPWR  ...        INE0QHG01026                  1           1  SUPREME POWER EQUIPMENT L-ST
# 4           NSECM                  2665               8     593RJ25  ...        IN2920200770                  1           1          SDL RJ 5.93% 2025-SG

# [5 rows x 19 columns] - xts_script_new.py:91
# 2024-11-29 16:41:07,819 - INFO - Data inserted successfully. - xts_script_new.py:99

# D:\XTS_Project_Learning\python_xts_env\xts-pythonclient-api-sdk-main>