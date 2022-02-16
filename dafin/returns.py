import glob
import datetime
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

from dafin.plot import Plot
from dafin.performance import AssetPerformance


class Returns:
    def __init__(
        self,
        asset_list: list,
        date_start: str = "2000-01-01",
        date_end: str = "2020-12-31",
        col_price: str = "Close",
        cache=True,
        cache_path: Path = Path("cache_dafin"),
    ) -> None:

        # arguments
        self.asset_list = asset_list
        self.col_price = col_price
        self.cache = cache
        self.cache_path = cache_path

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
            self.date_start = date_start
            self.date_end = date_end
            self.date_start_str = date_start.strftime(fmt)
            self.date_end_str = date_end.strftime(fmt)

        else:
            raise ValueError(
                "date_start and date_end types should be either datetime.date "
                "or str (e.g. '2014-03-24')"
            )

        # derived parameters
        self.business_day_num = int(np.busday_count(date_start, date_end))
        footprint = (
            [self.date_start_str, self.date_end_str] + asset_list + ["col_price"]
        )
        self.name = ".".join(footprint)
        self.signature = hashlib.md5(self.name.encode("utf-8")).hexdigest()[0:10]

        # retrieve the data
        self.collect()

        if self.__data_prices is None:
            raise ValueError("Error in data collection, self.__data_prices is not set")

        self.__data_prices = self.__data_prices.loc[self.date_start : self.date_end]
        self.__returns = self.__data_prices.pct_change().dropna()

        # performance
        self.__performance = AssetPerformance(self.__returns)
        self.returns = self.__performance.returns
        self.cum_returns = self.__performance.cum_returns
        self.total_returns = self.__performance.total_returns
        self.mean_sd = self.__performance.mean_sd

        # plot
        self.plot = Plot()

    def collect(self):

        filename = self.cache_path / Path(f"price_{self.signature}.pkl")
        price_file = glob.glob(str(filename))

        if self.cache and price_file:
            self.__data_prices = pd.read_pickle(price_file[0])

        else:

            # data retrieval
            raw_df = yf.Tickers(self.asset_list).history(period="max")

            # data refinement
            raw_df = raw_df.dropna(inplace=False)
            col_names = [(self.col_price, ticker) for ticker in self.asset_list]
            price_df = raw_df[col_names]
            price_df.columns = [col[1] for col in price_df.columns.values]
            price_df = price_df.dropna(inplace=False)

            # data storage
            self.cache_path.mkdir(parents=True, exist_ok=True)
            price_df.to_pickle(filename)
            self.__data_prices = price_df

    @property
    def prices(self):
        return self.__data_prices

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

    def plot_prices(self):
        fig, ax = self.plot.plot_trend(
            df=self.prices,
            title="",
            xlabel="Date",
            ylabel="Price (US$)",
        )
        return fig, ax

    def plot_returns(self, alpha=1):
        fig, ax = self.plot.plot_trend(
            df=self.returns,
            title="",
            xlabel="Date",
            ylabel="Daily Returns",
            alpha=alpha,
        )
        return fig, ax

    def plot_cum_returns(self):
        fig, ax = self.plot.plot_trend(
            df=self.cum_returns,
            title="",
            xlabel="Date",
            ylabel="Cumulative Returns",
        )
        return fig, ax

    def plot_dist_returns(self):
        fig, ax = self.plot.plot_box(
            df=self.returns,
            title=f"",
            xlabel="Assets",
            ylabel=f"Returns",
            figsize=(15, 8),
            yscale="symlog",
        )
        return fig, ax

    def plot_corr(self):
        fig, ax = self.plot.plot_heatmap(
            df=self.returns,
            relation_type="corr",
            title="",
            annotate=True,
        )
        return fig, ax

    def plot_cov(self):
        fig, ax = self.plot.plot_heatmap(
            df=self.returns,
            relation_type="cov",
            title="",
            annotate=True,
        )
        return fig, ax

    def plot_mean_sd(
        self,
        annualized=True,
        colour="tab:blue",
        fig=None,
        ax=None,
    ):
        ms = self.mean_sd.copy()

        if annualized:
            ms["mean"] *= 252
            ms["sd"] *= np.sqrt(252)

        fig, ax = self.plot.plot_scatter(
            df=ms,
            title="",
            xlabel="Volatility (SD)",
            ylabel="Expected Returns",
            colour=colour,
            fig=fig,
            ax=ax,
        )
        return fig, ax
