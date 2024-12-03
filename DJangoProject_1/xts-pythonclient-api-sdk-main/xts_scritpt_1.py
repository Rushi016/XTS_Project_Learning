import os
import logging
import psycopg2
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine
from Connect import XTSConnect

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d"
)


class XTSImportData:
    """
    Class to handle interactions with XTS APIs and PostgreSQL database,
    including data fetching, saving to CSV, and database insertion.
    """

    def __init__(self,API_KEY,API_SECRET,API_KEY_MARKET,API_SECRET_MARKET,SOURCE,
                       DB_HOST,DB_PORT,DB_NAME,DB_USER,DB_PASSWORD,
                       FILE_PATH):
        """
        Initialize XTSImortData with API credentials, database connection
        details, and file path for saving data.
        """
        
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.api_key_market = API_KEY_MARKET
        self.api_secret_market = API_SECRET_MARKET
        self.source = SOURCE
        
        self.db_host = DB_HOST
        self.db_port = DB_PORT
        self.db_name = DB_NAME
        self.db_user = DB_USER
        self.db_password = DB_PASSWORD

        self.file_path = FILE_PATH

        # Initialize API connections
        self.xts_interactive = XTSConnect(self.api_key,self.api_secret,self.source)
        self.xts_marketdata = XTSConnect(self.api_key_market,self.api_secret_market,self.source)

    def xts_login_interactive(self):
        """
        Perform login to the interactive XTS API and log the status.
        """

        response = self.xts_interactive.interactive_login()
        if response and response.get('type') == 'success':
            logging.info("Interactive login successful...")
            return True
        logging.error("Interactive login faild...")
        return False
    
    
    def xts_login_maketdata(self):
        """
        Perform login to the market data XTS API and log the status.
        """

        response = self.xts_marketdata.marketdata_login()
        if response and response.get('type') == 'success':
            logging.info("Marketdata login successful...")
            return True
        logging.error("Marketdata login faild...")
        return False

    def fetch_master_instruments(self):
        """
        Fetch master instruments data from the XTS MarketData API for specified exchange segments.
        """

        exchangesegments = [self.xts_marketdata.EXCHANGE_NSECM,self.xts_marketdata.EXCHANGE_NSEFO]
        response = self.xts_marketdata.get_master(exchangeSegmentList=exchangesegments)
        if 'result' in response:
            return response['result']
        logging.error("Error : 'result' not found in the marekt response")
        return None
    
    def save_master_data_to_csv(self,data):
        """
        Save the fetched master instruments data to a CSV file and return a pandas DataFrame.

        Args:
            data (str): Data returned from the API.

        Returns:
            pandas.DataFrame: DataFrame containing the master data.
        """
        assert data is not None, "data should not be none"

        try:
            master_df = pd.read_csv(
                StringIO(data),
                sep='|',
                usecols=range(19),
                header=None,
                low_memory=False
            )
            master_df.columns = [
                "ExchangeSegment", "ExchangeInstrumentID", "InstrumentType", "Name", "Description", "Series",
                "NameWithSeries", "InstrumentID", "PriceBand.High", "PriceBand.Low", "FreezeQty", "TickSize",
                "LotSize", "Multiplier", "UnderlyingInstrumentId", "UnderlyingIndexName", "ContractExpiration",
                "StrikePrice", "OptionType",
            ]
            master_df.rename(columns={'PriceBand.Low': 'PriceBandLow', 'PriceBand.High': 'PriceBandHigh'}, inplace=True)
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            master_df.to_csv(self.file_path, index=False)
            logging.info(f"Master response data saved to {self.file_path}")
            return master_df
        except Exception as e:
            logging.error(f"Error processing or saving master response: {e}")
            return None

    def insert_data_to_db(self,df):
        """
        Insert the DataFrame into the PostgreSQL database.

        Args:
            df (pandas.DataFrame): DataFrame to insert into the database.
        """
        assert df is not None, "df should not be none"

        try: 
            engine = create_engine(
                f"postgresql://{self.db_user}:{self.db_password}@"
                f"{self.db_host}:{self.db_port}/{self.db_name}"
            )
            df.to_sql('master_instruments', engine, if_exists='replace', index=False)
            logging.info("Data inserted successfully.")
            return True
        except Exception as e:
            logging.error(f"Error inserting data to PostgreSQL: {e}")
        return False
    

def main():
    """
    Main function to initialize the XTSImportData class, perform API logins,
    fetch data, save to CSV, and insert into the database.
    """

    # API and Marketdata Credentials
    API_KEY = "1afed370a1e58f2d831865"
    API_SECRET = "Qwnk201#P5"
    API_KEY_MARKET = "5575c6bfcff03735044479"
    API_SECRET_MARKET = "Iyqi743$bb"
    SOURCE = "WEBAPI"

    # Database connection details
    DB_HOST = 'localhost'  
    DB_PORT = '5432'       
    DB_NAME = 'MarketData'  
    DB_USER = 'postgres'     
    DB_PASSWORD = 'admin' 

    # File path for saving the fetch data
    FILE_PATH = "D:/XTS_Project_Learning/xts-pythonclient-api-sdk-main/master_response.csv"

    # Initialize the XTSImportData class
    xts = XTSImportData(API_KEY,API_SECRET,API_KEY_MARKET,API_SECRET_MARKET,SOURCE,
                       DB_HOST,DB_PORT,DB_NAME,DB_USER,DB_PASSWORD,
                       FILE_PATH)
    
    # Perform interactive and market data logins
    if xts.xts_login_interactive() and xts.xts_login_maketdata():
        # Fetch the master instruments data
        master_data = xts.fetch_master_instruments()

        # Save the fetched data to a csv file
        df = xts.save_master_data_to_csv(master_data)

        # Insert data into postgreSQL database 
        xts.insert_data_to_db(df) 

if __name__ == "__main__":
    main()
