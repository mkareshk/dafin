import pickle
from pathlib import Path, PosixPath

import pandas as pd
import yfinance as yf

from .utils import check_type, DEFAULT_CACHE_DIR


class FundamentalData:
    def __init__(
        self, assets: list | str, path_cache: Path = DEFAULT_CACHE_DIR
    ) -> None:

        # arguments
        if isinstance(assets, str):
            assets = [assets]

        self.assets = assets
        self.path_fundamental = path_cache / Path("fundamental")

        # check types
        check_type(self.assets, "assets", list)
        check_type(self.path_fundamental, "path_fundamental", PosixPath)

        # create the cache directory
        self.path_fundamental.mkdir(parents=True, exist_ok=True)

        # raw info
        self._info = self._get_raw_tickers_data()

    @property
    def info(self) -> pd.DataFrame:
        return self._info

    def _get_raw_tickers_data(self):

        info_list = [self._get_raw_ticker_data(t) for t in self.assets]
        info_df = pd.DataFrame(info_list)
        info_df.set_index("symbol", inplace=True)

        return info_df

    def _get_raw_ticker_data(self, ticker: str) -> pd.DataFrame:

        path_asset = self.path_fundamental / Path(f"{ticker}.pkl")

        if path_asset.exists():

            with open(path_asset, "rb") as fin:
                asset_info = pickle.load(fin)

        else:

            asset_info = yf.Ticker(ticker).info

            with open(path_asset, "wb") as fout:
                pickle.dump(asset_info, fout)

        return asset_info
