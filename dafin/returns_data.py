import datetime
import hashlib
from typing import List, Optional, Union

import pandas as pd
import yfinance as yf
from pyrate_limiter import Duration, Limiter, RequestRate
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


rate_limit = RequestRate(200, Duration.SECOND * 5)
SESSION = CachedLimiterSession(
    limiter=Limiter(rate_limit),
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)

from .utils import normalize_date, price_to_return


class ReturnsData:

    def __init__(
        self,
        assets: Union[List[str], str],
        col_price: str = "Adj Close",
    ) -> None:
        """
        Initializes the Data class with assets returns.
        It retrieves the prices and calculates the returns upon initialization.

        Parameters:
            assets (Union[List[str], str]): A list of asset symbols or a single asset symbol as a string.
            col_price (str, optional): The name of the column for price data. Defaults to "Adj Close".
        """

        # Convert to list if a single asset is passed
        self.assets = [assets] if isinstance(assets, str) else assets

        self.col_price = col_price

        # Creating a hash using the assets and column price to ensure data integrity
        footprint = ".".join(self.assets + [self.col_price])
        hash_object = hashlib.md5(footprint.encode("utf-8"))
        self._hash = int.from_bytes(hash_object.digest(), "big")

        # Retrieve the prices data
        price_df = yf.download(self.assets, session=SESSION)[self.col_price].dropna()
        self.prices = (
            price_df.to_frame() if isinstance(price_df, pd.Series) else price_df
        )

        # Calculate the returns from the prices data
        self.returns = price_to_return(self.prices)

    def get_returns(
        self,
        date_start: Optional[Union[str, datetime.datetime]] = None,
        date_end: Optional[Union[str, datetime.datetime]] = None,
    ) -> pd.DataFrame:
        """
        Retrieves the daily returns data for the specified date range. If no date range
        is provided, it returns all available data.

        Parameters:
            date_start (Union[str, datetime.datetime], optional): The start date. Defaults to None.
            date_end (Union[str, datetime.datetime], optional): The end date. Defaults to None.

        Returns:
            pd.DataFrame: The daily returns data within the specified date range or all available data if no dates are provided.
        """

        # If no date is passed, return all available data
        if not (date_start or date_end):
            return self.returns

        # If dates are provided, normalize them to ensure consistent formatting
        date_start, _ = normalize_date(date_start)
        date_end, _ = normalize_date(date_end)

        # Return the daily returns data for the specified date range
        return self.returns.loc[date_start:date_end]

    def __str__(self) -> str:
        """
        Returns the string representation of the class instance, providing detailed
        information on its current state including the assets, data signature,
        prices, and returns.

        Returns:
            str: The detailed string representation of the class instance.
        """

        # Creating a list of string segments to be concatenated into the final output
        str_segments = [
            "Returns Data:\n",
            f"- List of Assets: {self.assets}\n",
            f"- Price Column: {self.col_price}\n",
            f"- Data Signature: {self._hash}\n",
            f"- Prices:\n{self.prices}\n\n\n",
            f"- Returns:\n{self.returns}\n\n\n",
        ]

        # Joining all string segments into the final output string
        return "".join(str_segments)

    def __hash__(self) -> int:
        """
        Returns the hash of the class instance based on the `_hash` attribute.

        Returns:
            int: The hash value of the class instance.
        """
        return self._hash
