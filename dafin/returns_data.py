import pickle
import hashlib
import datetime
from functools import reduce
from pathlib import Path, PosixPath

import pandas as pd
import yfinance as yf

from .utils import *


class ReturnsData:
    def __init__(
        self,
        assets: list | str,
        col_price: str = "Adj Close",
        path_cache: Path = DEFAULT_CACHE_DIR,
    ) -> None:

        # arguments
        if isinstance(assets, str):
            assets = [assets]

        self.assets = assets
        self.col_price = col_price
        self.path_prices = path_cache / Path("prices")

        # check types
        check_type(self.assets, "assets", list)
        check_type(self.col_price, "col_price", str)
        check_type(self.path_prices, "path_prices", PosixPath)

        # derived parameters
        attrs = self.assets + [self.col_price]
        footprint = ".".join(attrs)
        hash = hashlib.md5(footprint.encode("utf-8"))
        self._hash = int.from_bytes(hash.digest(), "big")

        # create the cache directory
        self.path_prices.mkdir(parents=True, exist_ok=True)

        # retrieve the prices and calculate the returns
        self.prices = self._get_price_df()
        self.returns = price_to_return(self.prices)

    def get_returns(
        self,
        date_start: str | datetime.datetime = None,
        date_end: str | datetime.datetime = None,
    ) -> pd.DataFrame:

        # no date is passed, returns the whole available data
        if not (date_start or date_end):
            return self.returns

        # normalize the dates
        date_start, _ = normalize_date(date_start)
        date_end, _ = normalize_date(date_end)

        check_type(date_start, "date_start", datetime.datetime)
        check_type(date_end, "date_end", datetime.datetime)

        return self.returns.loc[date_start:date_end]

    def _get_price_df(self) -> pd.DataFrame:

        prices_list = []

        for asset in self.assets:

            path_asset = self.path_prices / Path(f"{asset}.pkl")

            # data already exists in the given path
            if path_asset.is_file():

                with open(path_asset, "rb") as fin:
                    price_df = pickle.load(fin)

            # retrieve price data if data does not exists in the cache
            else:
                price_df = yf.download(asset)

                with open(path_asset, "wb") as fout:
                    pickle.dump(price_df, fout)

            if not price_df.empty:
                price_df = price_df[self.col_price].to_frame()
                price_df = price_df.rename(columns={self.col_price: asset})
                prices_list.append(price_df)

            else:
                raise ValueError(f"The price_df of {asset} is empty.")

        # data aggregation
        merge_func = lambda df1, df2: pd.merge(df1, df2, on="Date", how="inner")
        price_df = reduce(merge_func, prices_list)

        if price_df.empty:
            raise ValueError("Error in data collection, price_df is empty.")

        return price_df

    def __str__(self):

        return (
            "Returns Data:\n"
            # assets
            + f"\t- List of Assets: {self.assets}\n"
            # column
            + f"\t- Price Column: {self.col_price}\n"
            # path
            + f"\t- Cache Path: {self.path_prices}\n"
            + f"\t- Prices Path: {self.path_prices}\n"
            # signature
            + f"\t- Data Signature: {self._hash}\n"
            # prices
            + f"\t - Prices:\n{pretty_table(self.prices)}\n\n\n"
            # returns
            + f"\t - Returns:\n{pretty_table(self.returns)}\n\n\n"
        )

    def __hash__(self):
        return self._hash
