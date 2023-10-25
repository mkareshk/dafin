import pickle
import hashlib
import datetime
from typing import List, Union, Optional
from functools import reduce
from pathlib import Path

import pandas as pd
import yfinance as yf

from .utils import DEFAULT_CACHE_DIR, price_to_return, normalize_date


class ReturnsData:

    def __init__(
        self,
        assets: Union[List[str], str],
        col_price: str = "Adj Close",
        path_cache: Path = DEFAULT_CACHE_DIR
    ) -> None:
        """
        Initializes the Data class with assets, column for price, and the path for cache.
        It retrieves the prices and calculates the returns upon initialization.

        Parameters:
            assets (Union[List[str], str]): A list of asset symbols or a single asset symbol as a string.
            col_price (str, optional): The name of the column for price data. Defaults to "Adj Close".
            path_cache (Path, optional): The path where cache files are stored. Defaults to DEFAULT_CACHE_DIR.

        Example:
            Assuming that `price_to_return` and `_get_price_df` methods and DEFAULT_CACHE_DIR are defined elsewhere,
            >>> data_instance = Data(['AAPL', 'GOOGL'], col_price="Close")
            >>> isinstance(data_instance, Data)
            True
        """

        # Convert to list if a single asset is passed
        self.assets = [assets] if isinstance(assets, str) else assets
        
        self.col_price = col_price
        self.path_prices = path_cache / "prices"

        # Creating a hash using the assets and column price to ensure data integrity or for caching purposes
        footprint = ".".join(self.assets + [self.col_price])
        hash_object = hashlib.md5(footprint.encode("utf-8"))
        self._hash = int.from_bytes(hash_object.digest(), "big")

        # Create the cache directory if it does not exist
        self.path_prices.mkdir(parents=True, exist_ok=True)

        # Retrieve the prices data
        self.prices = self._get_price_df()

        # Calculate the returns from the prices data
        self.returns = price_to_return(self.prices)

    def get_returns(
        self,
        date_start: Optional[Union[str, datetime.datetime]] = None,
        date_end: Optional[Union[str, datetime.datetime]] = None
    ) -> pd.DataFrame:
        """
        Retrieves the daily returns data for the specified date range. If no date range 
        is provided, it returns all available data.

        Parameters:
            date_start (Union[str, datetime.datetime], optional): The start date. Defaults to None.
            date_end (Union[str, datetime.datetime], optional): The end date. Defaults to None.

        Returns:
            pd.DataFrame: The daily returns data within the specified date range or all available data if no dates are provided.

        Example:
            Assuming an instance has a `returns` attribute as a DataFrame and 
            `normalize_date` function is defined:
            >>> instance.get_returns('2022-01-01', '2022-01-10')
            <DataFrame with the daily returns data between '2022-01-01' and '2022-01-10'>
        """
        
        # If no date is passed, return all available data
        if not (date_start or date_end):
            return self.returns

        # If dates are provided, normalize them to ensure consistent formatting
        date_start, _ = normalize_date(date_start)
        date_end, _ = normalize_date(date_end)

        # Return the daily returns data for the specified date range
        return self.returns.loc[date_start:date_end]


    def _get_price_df(self) -> pd.DataFrame:
        """
        Returns the aggregated price data for all assets specified in self.assets.
        The method first tries to load the price data from a file. If the file doesn't exist,
        it downloads the data using yfinance and then stores it for future use.

        Raises:
        ValueError: If the data is unavailable or if the aggregated price data is empty.

        Returns:
        pd.DataFrame: Aggregated price data of all assets.

        Usage example:
        Assuming `self.assets`, `self.path_prices`, and `self.col_price` are defined and
        the method is within a class with these attributes, simply call:
        >>> price_df = self._get_price_df()
        """

        prices_list = []

        for asset in self.assets:
            # Construct the file path where the asset's price data should be stored
            path_asset = self.path_prices / Path(f"{asset}.pkl")

            # If data already exists at the path, load it
            if path_asset.is_file():
                with open(path_asset, "rb") as fin:
                    price_df = pickle.load(fin)
            # If data does not exist, download it using yfinance and save it to the path
            else:
                price_df = yf.download(asset)
                with open(path_asset, "wb") as fout:
                    pickle.dump(price_df, fout)

            # If price_df is not empty, process and add it to prices_list
            if not price_df.empty:
                price_df = price_df[self.col_price].to_frame()
                price_df.rename(columns={self.col_price: asset}, inplace=True)
                prices_list.append(price_df)
            else:
                raise ValueError(f"The price data of {asset} is empty.")

        # Aggregate all price data DataFrames in prices_list into a single DataFrame
        merge_func = lambda df1, df2: pd.merge(df1, df2, on="Date", how="inner")
        aggregated_price_df = reduce(merge_func, prices_list)

        # Raise an error if the aggregated data is empty
        if aggregated_price_df.empty:
            raise ValueError("Error in data collection, aggregated price data is empty.")

        return aggregated_price_df

    def __str__(self) -> str:
        """
        Returns the string representation of the class instance, providing detailed 
        information on its current state including the assets, cache path, data signature,
        prices, and returns.

        Returns:
            str: The detailed string representation of the class instance.
            
        Example:
            Assuming an instance of the class is already created, the method can be used
            as follows:
            >>> str(instance)
            'Returns Data:\n\t- List of Assets: [...]\n\t- Price Column: ...\n...'
        """
        
        # Creating a list of string segments to be concatenated into the final output
        str_segments = [
            "Returns Data:\n",
            f"\t- List of Assets: {self.assets}\n",
            f"\t- Price Column: {self.col_price}\n",
            # Removed redundant 'Prices Path' line to clean up the output
            f"\t- Cache Path: {self.path_prices}\n",
            f"\t- Data Signature: {self._hash}\n",
            f"\t- Prices:\n{self.prices}\n\n\n",
            f"\t- Returns:\n{self.returns}\n\n\n"
        ]
        
        # Joining all string segments into the final output string
        return ''.join(str_segments)


def __hash__(self) -> int:
    """
    Computes and returns the hash of the class instance based on the `_hash` attribute.

    Returns:
        int: The hash value of the class instance.
        
    Doctest:
        Assuming the '_hash' attribute is properly set, you can get the hash as follows:
        >>> class Example:
        ...     def __init__(self, hash_value):
        ...         self._hash = hash_value
        ...     __hash__ = __hash__
        ...
        >>> e = Example(1234)
        >>> hash(e)
        1234
    """
    # Returning the precomputed hash value stored in the `_hash` attribute
    return self._hash
