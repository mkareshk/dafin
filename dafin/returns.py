import glob
import datetime
import json
import hashlib
from pathlib import Path
from functools import reduce
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
        path_cache: Path = Path("cache_dafin"),
    ) -> None:

        # arguments
        self.asset_list = asset_list
        self.col_price = col_price
        self.cache = cache
        self.path_cache = path_cache

        self.path_price = self.path_cache / Path("returns")
        self.path_price.mkdir(parents=True, exist_ok=True)

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
            self.date_start = datetime.datetime.strptime(date_start, fmt)
            self.date_end = datetime.datetime.strptime(date_end, fmt)

        elif isinstance(date_start, datetime.date):
            self.date_start = date_start
            self.date_end = date_end
            self.date_start_str = date_start.strftime(fmt)
            self.date_end_str = date_end.strftime(fmt)

        else:
            raise ValueError(
                "date_start and date_end types should be either datetime.date "
                f"or str (e.g. '2014-03-24'). {type(date_start)} is given"
            )

        # derived parameters
        self.business_day_num = int(np.busday_count(date_start, date_end))
        footprint = (
            [self.date_start_str, self.date_end_str] + asset_list + ["col_price"]
        )
        self.name = ".".join(footprint)
        self.signature = hashlib.md5(self.name.encode("utf-8")).hexdigest()[0:10]

        # retrieve the data
        self.__data_prices = self.get_price_df()

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
        self.annualized_mean_sd = self.__performance.annualized_mean_sd
        self.days_per_year = self.__performance.days_per_year

        # plot
        self.plot = Plot()

        # stats
        self.cov = self.returns.cov()
        self.corr = self.returns.corr()
        self.stats = self.returns.describe()

    def get_price_df(self):

        prices_list = []
        for ticker in self.asset_list:
            path_asset = self.path_price / Path(f"{ticker}.json")

            # retrieve price data if it have not retrieved yet in the cache
            if not path_asset.is_file():
                price_df = self.retrieve_price_external_api(ticker)

                price_str = json.dumps(price_df.to_json())
                with open(path_asset, "wt") as fout:
                    fout.write(price_str)

            # data already exists
            else:
                with open(path_asset, "rt") as fin:
                    price_str = fin.read()
                    price_df = pd.read_json(json.loads(price_str))

            if not price_df.empty:
                price_df = price_df.rename(
                    columns={self.col_price: ticker}, inplace=False
                )[ticker].to_frame()
                price_df.index.rename("Date", inplace=True)
                prices_list.append(price_df)

        merge_func = lambda df1, df2: pd.merge(df1, df2, on="Date", how="inner")

        return reduce(merge_func, prices_list)

    def retrieve_price_external_api(self, ticker):
        return yf.Ticker(ticker).history(period="max")

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
            ylabel="Asset Prices",
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

    def prot_total_returns(self):
        fig, ax = self.plot.plot_bar(
            df=self.total_returns,
            title="",
            xlabel="Assets",
            ylabel=f"Total Returns ({self.date_start_str} to {self.date_end_str})",
        )
        return fig, ax

    def plot_dist_returns(self):
        fig, ax = self.plot.plot_box(
            df=self.returns,
            title=f"",
            xlabel="Assets",
            ylabel=f"Daily Returns",
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

        if annualized:
            ms = self.annualized_mean_sd * 100.00
            xlabel = "Annualized Standard Deviation (%)"
            ylabel = "Annualized Expected Returns (%)"
        else:
            ms = self.mean_sd
            xlabel = "Standard Deviation"
            ylabel = "Expected Returns"

        fig, ax = self.plot.plot_scatter(
            df=ms,
            title="",
            xlabel=xlabel,
            ylabel=ylabel,
            colour=colour,
            fig=fig,
            ax=ax,
        )
        return fig, ax
