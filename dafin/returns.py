import glob
import datetime
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf


class Returns:
    def __init__(
        self,
        asset_list: list,
        date_start: str = "2000-01-01",
        date_end: str = "2020-12-31",
        col_price: str = "Close",
        path_data: Path = Path("data_returns"),
    ) -> None:

        # arguments
        self.asset_list = asset_list
        self.col_price = col_price
        self.path_data = path_data

        # make the dates standard

        fmt = "%Y-%m-%d"

        if type(date_start) != type(date_end):
            raise ValueError(
                f"date_start ({type(date_start)}) and "
                f"date_end ({type(date_end)}) should have the same type"
            )

        elif isinstance(date_start, str):
            self.date_start_str = date_start
            self.date_end_str = date_end
            self.date_start = datetime.datetime.strptime(date_start, fmt).date()
            self.date_end = datetime.datetime.strptime(date_end, fmt).date()

        elif isinstance(date_start, datetime.date):
            self.date_start = date_start.strftime(fmt)
            self.date_end = date_start.strftime(fmt)
            self.date_start_str = date_start
            self.date_end_str = date_end

        else:
            raise ValueError(
                "date_start and date_end types should be either datetime.date "
                "or str (e.g. '2014-03-24')"
            )

        # derived parameters
        self.business_day_num = int(np.busday_count(date_start, date_end))
        self.name = ".".join([self.date_start_str, self.date_end_str] + asset_list)
        self.signature = hashlib.md5(self.name.encode("utf-8")).hexdigest()[0:10]

        # retrieve the data
        self.collect()
        if self.__data_prices is None:
            raise ValueError("Error in data collection, self.__data_prices is not set")

        # calculate returns
        self.__returns = self.__data_prices.pct_change().dropna()
        self.__cum_returns = (self.__returns + 1).cumprod() - 1

        # mean-sd
        self.__mean_sd = pd.DataFrame(columns=["mean", "sd"])
        self.__mean_sd["mean"] = self.__returns.mean()
        self.__mean_sd["sd"] = self.__returns.std()

    def collect(self):

        self.path_data.mkdir(parents=True, exist_ok=True)
        price_file = glob.glob(
            str(self.path_data / Path(f"price_{self.signature}.pkl"))
        )

        if price_file:  # read the existing data
            self.__data_prices = pd.read_pickle(price_file[0])

        else:  # data collection using API

            # data retrieval
            raw_df = yf.Tickers(self.asset_list).history(period="max")

            # data refinement
            raw_df.dropna(inplace=True)
            col_names = [(self.col_price, ticker) for ticker in self.asset_list]
            price_df = raw_df[col_names]
            price_df.columns = [col[1] for col in price_df.columns.values]
            price_df.dropna(inplace=True)

            # data storage
            filename = self.path_data / Path(f"price_{self.signature}.pkl")
            price_df.to_pickle(filename)
            self.__data_prices = price_df

    @property
    def prices(self):
        return self.__data_prices

    @property
    def returns(self):
        return self.__returns

    @property
    def cum_returns(self):
        return self.__cum_returns

    @property
    def mean_sd(self):
        return self.__mean_sd

    def __str__(self):
        return (
            f"Asset List: {', '.join(self.asset_list)}\n"
            + f"Price Column: {self.col_price}\n"
            + f"Start Date: {self.date_start_str}\n"
            + f"End Date: {self.date_end_str}\n"
            + f"Business Days No.: {self.business_day_num}\n"
            + f"Data Signature: {self.signature}\n\n"
            + f"Prices:\n{self.prices}\n\n"
            + f"Returns:\n{self.returns}\n\n"
            + f"Cumulative Returns:\n{self.cum_returns}\n\n"
            + f"Mean-SD Returns:\n{self.mean_sd}\n"
        )
