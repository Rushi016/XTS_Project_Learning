from Connect import XTSConnect
import logging
#import json
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
        try:
            masterdf = pd.read_csv(
                StringIO(master_response['result']),
                sep='|', 
                usecols=range(19), 
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

            #logging.info(masterdf)

            # Define the folder and file name to save the CSV file
            folder_path = 'D:\\XTS_Project_Learning\\python_xts_env\\xts-pythonclient-api-sdk-main' 
            file_name = "master_response.csv"  
            file_path = os.path.join(folder_path, file_name)
            os.makedirs(folder_path, exist_ok=True)
            masterdf.to_csv(file_path, index=False)
            logging.info(f"Master response data saved to {file_path}")

        except Exception as e:
            logging.error(f"Error processing or saving master response: {e}")
    else:
        logging.error("Error: 'result' not found in the master response.")

    # Database connection details
    db_host = 'localhost'  
    db_port = '5432'       
    db_name = 'MarketData'  
    db_user = 'postgres'     
    db_password = 'admin'  

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
    csv_file_path ='D:\\XTS_Project_Learning\\python_xts_env\\xts-pythonclient-api-sdk-main\\master_response.csv'

    # Read the CSV into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Optionally, preview the first few rows of the DataFrame
    logging.info(df.head())

    # Using SQLAlchemy to simplify the connection and insertion
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

    # Insert the DataFrame into the PostgreSQL table
    try:
        df.to_sql('master_instruments', engine, if_exists='replace', index=False)
        logging.info("Data inserted successfully.")
    except Exception as e:
        logging.info(f"Error: {e}")

    # Close the connection
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()


# Output:
# (python_xts_env) D:\XTS_Learning\python_xts_env\xts-pythonclient-api-sdk-main>python New_script1.py 
# 2024-11-25 10:11:50,842 - INFO - Interactive Login Successful - New_script1.py:28
# 2024-11-25 10:11:51,173 - INFO - Marketdata Login Successful - New_script1.py:44
# 2024-11-25 10:11:55,099 - INFO - Master response data saved to D:\DJango\python_xts_env\xts-pythonclient-api-sdk-main\master_response.csv - New_script1.py:91
# D:\XTS_Learning\python_xts_env\xts-pythonclient-api-sdk-main\New_script1.py:121: DtypeWarning: Columns (14,17,18) have mixed types. Specify dtype option on import or set low_memory=False.
#   df = pd.read_csv(csv_file_path)
# 2024-11-25 10:11:55,508 - INFO -   ExchangeSegment  ExchangeInstrumentID  InstrumentType       Name  ... UnderlyingIndexName ContractExpiration StrikePrice                   OptionType
# 0           NSECM                 11705               8  XCHANGING  ...        INE692G01013                  1           1   XCHANGING SOLUTIONS LTD-EQ
# 1           NSECM                 24398               8     EMCURE  ...        INE168P01015                  1           1  EMCURE PHARMACEUTICALS L-EQ
# 2           NSECM                  4570               8    605RJ26  ...        IN2920210142                  1           1         SDL RJ 6.05% 2026-SG
# 3           NSECM                 11626               8     WELENT  ...        INE625G01013                  1           1  WELSPUN ENTERPRISES LTD.-EQ
# 4           NSECM                 24990               8    724MH39  ...        IN2220240195                  1           1         SDL MH 7.24% 2039-SG

# [5 rows x 19 columns] - New_script1.py:124
# 2024-11-25 10:12:03,860 - INFO - Data inserted successfully. - New_script1.py:132
