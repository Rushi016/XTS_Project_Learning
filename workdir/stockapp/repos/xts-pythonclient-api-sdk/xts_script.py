import os
import logging
import pandas as pd
from io import StringIO
from sqlalchemy import create_engine
from Connect import XTSConnect
# from dotenv import load_dotenv


class XTSMarketDataHandler:
    """
    Class to handle XTS Market Data and PostgreSQL operations.
    """

    def __init__(self, API_KEY, API_SECRET, API_KEY_Market, API_SECRET_Market, SOURCE,
                 HOST, PORT, DBNAME, USER, PASSWORD, FILE_PATH):
        """
        Initialize with API credentials, database config, and file path.
        """
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.api_key_market = API_KEY_Market
        self.api_secret_market = API_SECRET_Market
        self.source = SOURCE

        self.host = HOST
        self.port = PORT
        self.dbname = DBNAME
        self.user = USER
        self.password = PASSWORD

        self.file_path = FILE_PATH

        self.xti = XTSConnect(self.api_key, self.api_secret, self.source)
        self.xtm = XTSConnect(self.api_key_market, self.api_secret_market, self.source)

    def login_interactive(self):
        """
        Perform interactive login using XTSConnect.
        """
        login_response = self.xti.interactive_login()
        assert login_response, "Interactive Login Response is empty"
        assert login_response.get("type") == "success", "Interactive Login Failed"
        logging.info("Interactive Login Successful")
        return True

    def login_marketdata(self):
        """
        Perform market data login using XTSConnect.
        """
        marketdata_response = self.xtm.marketdata_login()
        assert marketdata_response, "Marketdata Login Response is empty"
        assert marketdata_response.get("type") == "success", "Marketdata Login Failed"
        logging.info("Marketdata Login Successful")
        return True

    def fetch_master_data(self):
        """
        Fetch master data for exchange segments from the XTS API.
        """
        exchangesegments = [
            self.xtm.EXCHANGE_NSECM, 
            self.xtm.EXCHANGE_NSEFO
        ]
        response = self.xtm.get_master(exchangeSegmentList=exchangesegments)
        assert 'result' in response, "Error: 'result' not found in the master response."
        return response['result']

    def save_master_data_to_csv(self, data):
        """
        Save master data to a CSV file after processing it.
        """
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
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            master_df.rename(columns={ 
                "PriceBand.High": "PriceBandHigh", 
                "PriceBand.Low": "PriceBandLow"
            }, inplace=True)
            master_df.to_csv(self.file_path, index=False)
            logging.info(f"Master response data saved to {self.file_path}")
            return master_df
        except Exception as e:
            logging.error(f"Error processing or saving master response: {e}")
            return None

    def insert_data_to_postgres(self, df):
        """
        Insert data into PostgreSQL database.
        """
        try:
            engine = create_engine(
                f"postgresql://{self.user}:{self.password}@"
                f"{self.host}:{self.port}/{self.dbname}"
            )
            df.to_sql('master_instruments', engine, if_exists='replace', index=False)
            logging.info("Data inserted successfully.")
        except Exception as e:
            logging.error(f"Error inserting data to PostgreSQL: {e}")


def main():
    """
    Main function to execute the login, data fetch, and data processing pipeline.
    """
    # Interactive and MarketData Login Credentials
    API_KEY = "1afed370a1e58f2d831865"
    API_SECRET = "Qwnk201#P5"
    API_KEY_MARKET = "5575c6bfcff03735044479"
    API_SECRET_MARKET = "Iyqi743$bb"
    SOURCE = "WEBAPI"

    # Database Configuration
    HOST = "localhost"
    PORT = "5432"
    DBNAME = "MarketData"
    USER = "postgres"
    PASSWORD = "admin"

    FILE_PATH = "D:/XTS_Project_Learning/workdir/stockapp/repos/xts-pythonclient-api-sdk/master_response.csv"

    """
        # Access environment variables .env file path
        dotenv_path = "D:/XTS_Project_Learning/workdir/stockapp/repos/xts-pythonclient-api-sdk/xts.env"
        load_dotenv(dotenv_path)

        # Interactive and MarketData Login Credentials
        API_KEY = os.getenv("XTS_API_KEY")
        API_SECRET = os.getenv("XTS_API_SECRET")
        API_KEY_MARKET = os.getenv("XTS_API_KEY_MARKET")
        API_SECRET_MARKET = os.getenv("XTS_API_SECRET_MARKET")
        SOURCE = os.getenv("XTS_SOURCE")

        # Database Configuration
        HOST = os.getenv("XTS_HOST")
        PORT = os.getenv("XTS_PORT")
        DBNAME = os.getenv("XTS_DBNAME")
        USER = os.getenv("XTS_USER")
        PASSWORD = os.getenv("XTS_PASSWORD")

        # File path
        FILE_PATH = os.getenv("XTS_FILE_PATH")
    """

    # Initialize handler
    xts_handler = XTSMarketDataHandler(
        API_KEY, API_SECRET, API_KEY_MARKET, API_SECRET_MARKET, SOURCE,
        HOST, PORT, DBNAME, USER, PASSWORD, FILE_PATH
    )

    # Login and process data
    assert xts_handler.login_interactive(), "Interactive Login Failed"
    assert xts_handler.login_marketdata(), "Marketdata Login Failed"

    master_data = xts_handler.fetch_master_data()
    assert master_data, "Master data fetch failed"

    df = xts_handler.save_master_data_to_csv(master_data)
    assert df is not None, "Saving master data to CSV failed"

    xts_handler.insert_data_to_postgres(df)


if __name__ == "__main__":
    main()
