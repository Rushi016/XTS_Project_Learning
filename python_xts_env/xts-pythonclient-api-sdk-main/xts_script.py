from Connect import XTSConnect
import logging
import json
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine
import psycopg2
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d"
)

def main():
    # Interactive API Credentials
    API_KEY = "1afed370a1e58f2d831865"
    API_SECRET = "Qwnk201#P5"
    source = "WEBAPI"

    """Make XTSConnect object by passing your interactive API appKey, secretKey and source"""
    xt = XTSConnect(API_KEY, API_SECRET, source)

    """Using the xt object we created call the interactive login Request"""
    login_response = xt.interactive_login()

    if login_response and login_response.get('type') == 'success':
        logging.info("Interactive Login Successful")
        # logging.info(f"Interactive Login Response:\n{json.dumps(login_response, indent=4)}")
    else:
        logging.error("Interactive Login Failed")

    # Marketdata API Credentials
    API_KEY_Market = "5575c6bfcff03735044479"
    API_SECRET_Market = "Iyqi743$bb"

    """Make the XTSConnect Object with Marketdata API appKey, secretKey and source"""
    xtm = XTSConnect(API_KEY_Market, API_SECRET_Market, source)

    """Using the object we call the login function Request"""
    marketdata_response = xtm.marketdata_login()

    if marketdata_response and marketdata_response.get('type') == 'success':
        logging.info("Marketdata Login Successful")
        # logging.info(f"Marketdata Login Response:\n{json.dumps(marketdata_response, indent=4)}")
        # logging.info(marketdata_response)
    else:
        logging.error("Marketdata Login Failed")

    """Get Master Instruments Request"""
    exchangesegments = [xtm.EXCHANGE_NSECM, xtm.EXCHANGE_NSEFO]
    master_response = xtm.get_master(exchangeSegmentList=exchangesegments)
    # logging.info(f"Master List Response:\n{json.dumps(master_response, indent=10)}")
    # logging.info(master_response)

    # Check if the response contains the 'result' key
    if 'result' in master_response:
        # Read the master response data (assuming it's a CSV-like string)
        try:
            # Read the CSV data into a DataFrame using pandas
            masterdf = pd.read_csv(
                StringIO(master_response['result']),
                sep='|', 
                usecols=range(19),  # Use the first 19 columns, adjust if needed
                header=None, 
                low_memory=False
            )

            # Assign column names to the DataFrame
            masterdf.columns = [
                "ExchangeSegment", "ExchangeInstrumentID", "InstrumentType", "Name", "Description", "Series", 
                "NameWithSeries", "InstrumentID", "PriceBand.High", "PriceBand.Low", "FreezeQty", "TickSize", 
                "LotSize", "Multiplier", "UnderlyingInstrumentId", "UnderlyingIndexName", "ContractExpiration", 
                "StrikePrice", "OptionType",
            ]

            # logging.info(masterdf)

            # Define the folder and file name to save the CSV file
            folder_path = r"D:\DJango\python_xts_env\xts-pythonclient-api-sdk-main"  # Specify your folder path
            file_name = "master_response.csv"  # Name of the CSV file
            file_path = os.path.join(folder_path, file_name)

            # Ensure the folder exists
            os.makedirs(folder_path, exist_ok=True)

            # Save the DataFrame to a CSV file
            masterdf.to_csv(file_path, index=False)

            # Log confirmation
            print(f"Master response data saved to {file_path}")

        except Exception as e:
            print(f"Error processing or saving master response: {e}")
    else:
        print("Error: 'result' not found in the master response.")

    # Database connection details
    db_host = 'localhost'  # PostgreSQL host
    db_port = '5432'       # PostgreSQL port
    db_name = 'MarketData'  # Database name
    db_user = 'postgres'     # Your database user
    db_password = 'admin'  # Your database password

    # Create a connection to PostgreSQL using psycopg2
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Path to the CSV file
    csv_file_path = r'D:\DJango\python_xts_env\xts-pythonclient-api-sdk-main\master_response.csv'

    # Read the CSV into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Optionally, preview the first few rows of the DataFrame
    print(df.head())

    # Using SQLAlchemy to simplify the connection and insertion
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

    # Insert the DataFrame into the PostgreSQL table
    try:
        df.to_sql('master_instruments', engine, if_exists='replace', index=False)
        print("Data inserted successfully.")
    except Exception as e:
        print(f"Error: {e}")

    # Close the connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()