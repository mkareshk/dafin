from pathlib import Path

import numpy as np
import pandas as pd

from .plot import Plot
from .utils import *


class Performance:
    def __init__(
        self,
        returns_assets: pd.DataFrame,
        returns_rf: pd.DataFrame = None,
        returns_benchmark: pd.DataFrame = None,
    ) -> None:
        """
        Initializes the Performance object with provided assets, risk-free, and benchmark returns.

        Parameters:
        - returns_assets: A DataFrame containing the returns of multiple assets.
        - returns_rf: A DataFrame containing the returns of the risk-free asset (optional).
        - returns_benchmark: A DataFrame containing the returns of the benchmark asset (optional).

        Raises:
        - ValueError: If returns_assets DataFrame is empty.
        """

        if returns_assets.empty:
            raise ValueError("returns_assets cannot be empty")

        self.returns_assets = returns_assets

        # If risk-free returns are not provided, create a DataFrame with zeros
        if returns_rf is None:
            self.returns_rf = pd.DataFrame(
                data=np.zeros(len(returns_assets)),
                index=returns_assets.index,
                columns=["RiskFree"],
            )
        else:
            self.returns_rf = returns_rf

        # If benchmark returns are not provided, use the risk-free returns as benchmark
        self.returns_benchmark = (
            returns_benchmark
            if returns_benchmark is not None
            else self.returns_rf.copy()
        )

        self.assets = self.returns_assets.columns.tolist()
        self.asset_rf = self.returns_rf.columns[0]
        self.asset_benchmark = self.returns_benchmark.columns[0]
        self.date_start_str = date_to_str(self.returns_assets.index[0])
        self.date_end_str = date_to_str(self.returns_assets.index[-1])

        # Initialize plotting object
        self.plot = Plot()

        # Calculate cumulative returns
        self.returns_cum = calc_returns_cum(self.returns_assets)

        # Calculate total returns
        self.returns_total = calc_returns_total(self.returns_assets)

        # Calculate covariance and correlation matrices
        self.cov = self.returns_assets.cov()
        self.corr = self.returns_assets.corr()

        # Calculate annualzied returns
        self.returns_assets_annualized = calc_annualized_returns(self.returns_assets)

        # Calculate annualized standard deviation
        self.sd_assets_annualized = calc_annualized_sd(self.returns_assets)

        # Calculate annualized returns of the risk-free asset
        self.returns_rf_annualized = calc_annualized_returns(self.returns_rf)

        # Calculate annualized returns of the benchmark
        self.returns_benchmark_annualized = calc_annualized_returns(
            self.returns_benchmark
        )

        # Calculate the mean and standard deviation of the assets
        self.mean_sd = pd.DataFrame(index=self.assets, columns=["mean", "sd"])
        self.mean_sd["mean"] = self.returns_assets_annualized
        self.mean_sd["sd"] = self.sd_assets_annualized

        # Calculate the beta of the assets
        self.beta = calculate_beta(self.returns_assets, self.returns_benchmark)

        # Calculate the alpha of the assets
        self.alpha = calculate_alpha(
            self.returns_assets,
            self.returns_rf,
            self.returns_benchmark,
        )

        # Calculate the regression of the assets
        self.regression = regression(self.returns_assets, self.returns_benchmark)

        # Calculate the sharpe ratio of the assets
        self.sharpe_ratio = calculate_sharpe_ratio(
            self.returns_assets,
            self.returns_rf,
        )

        # Calculate the treynor ratio of the assets
        self.treynor_ratio = calculate_treynor_ratio(
            self.returns_assets,
            self.returns_rf,
            self.returns_benchmark,
        )

    def __str__(self) -> str:
        """Returns a string representation of the object.

        Returns:
            str: String representation of the object.
        """

        return (
            "Performance:\n"
            # assets
            + f"- List of Assets: {self.assets}\n"
            + f"- Risk-Free Asset: {self.asset_rf}\n"
            + f"- Benchmark Asset: {self.asset_benchmark}\n"
            # date
            + f"- Start Date: {self.date_start_str}\n"
            + f"- End Date: {self.date_end_str}\n"
            # performance
            + f"- Performance Summary:\n{self.summary}\n\n\n"
        )

    @property
    def summary(self) -> pd.DataFrame:
        """Returns a summary of the performance.

        Returns:
            pd.DataFrame: Summary of the performance.
        """

        s = pd.DataFrame()
        s.index = self.returns_assets.columns

        s["Total Returns"] = self.returns_total
        s["Expected Returns"] = self.returns_assets_annualized
        s["Standard Deviation"] = self.sd_assets_annualized
        s["Alpha"] = self.alpha
        s["Beta"] = self.beta
        s["Sharpe Ratio"] = self.sharpe_ratio
        s["Treynor Ratio"] = self.treynor_ratio

        s = pd.concat([s, self.regression], axis=1)

        return s

    def plot_returns(
        self,
        alpha: float = 1,
        legend: bool = True,
        yscale: str = "linear",
        title="Returns",
    ):

        return self.plot.plot_trend(
            df=self.returns_assets,
            title=title,
            xlabel="Date",
            ylabel="Expected Annual Returns",
            alpha=alpha,
            marker="o",
            legend=legend,
            yscale=yscale,
        )

    def plot_cum_returns(self, title="Cumulative Returns"):
        return self.plot.plot_trend(
            df=self.returns_cum,
            title=title,
            xlabel="Date",
            marker=None,
            ylabel="Cumulative Returns",
            yscale="linear",
        )

    def plot_total_returns(self, title="Total Returns", legend: bool = False):
        return self.plot.plot_bar(
            df=self.returns_total,
            title=title,
            xlabel="Assets",
            ylabel=f"Total Returns ({self.date_start_str} to {self.date_end_str})",
            legend=legend,
        )

    def plot_dist_returns(
        self, title: str = "Distribution of Returns", yscale: str = "symlog"
    ):
        return self.plot.plot_box(
            df=self.returns_assets,
            title=title,
            xlabel="Assets",
            ylabel=f"Daily Returns",
            figsize=(15, 8),
            yscale=yscale,
        )

    def plot_corr(self, title: str = "Correlation Matrix"):
        return self.plot.plot_heatmap(
            df=self.returns_assets,
            relation_type="corr",
            title=title,
            annotate=True,
        )

    def plot_cov(self, title: str = "Covariance Matrix"):
        return self.plot.plot_heatmap(
            df=self.returns_assets,
            relation_type="cov",
            title=title,
            annotate=True,
        )

    def plot_mean_sd(
        self,
        colour="tab:blue",
        fig=None,
        ax=None,
        title: str = "Mean vs. Standard Deviation",
        xlabel: str = "Standard Deviation",
        ylabel: str = "Expected Returns",
    ):

        return self.plot.plot_scatter(
            df=self.mean_sd,
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            colour=colour,
            fig=fig,
            ax=ax,
        )

    def save_figs(self, path: Path, prefix: str = "experiment"):

        path.mkdir(parents=True, exist_ok=True)
        prefix = f"{prefix}_plot"

        fig, _ = self.plot_returns()
        fig.savefig(path / Path(f"{prefix}_returns.png"))

        fig, _ = self.plot_cum_returns()
        fig.savefig(path / Path(f"{prefix}_cum_returns.png"))

        fig, _ = self.plot_total_returns()
        fig.savefig(path / Path(f"{prefix}_total_returns.png"))

        fig, _ = self.plot_dist_returns()
        fig.savefig(path / Path(f"{prefix}_dist_returns.png"))

        fig, _ = self.plot_corr()
        fig.savefig(path / Path(f"{prefix}_corr.png"))

        fig, _ = self.plot_cov()
        fig.savefig(path / Path(f"{prefix}_cov.png"))

        fig, _ = self.plot_mean_sd()
        fig.savefig(path / Path(f"{prefix}_mean_sd.png"))

    def save_data(self, path: Path, prefix: str = "experiment"):

        path.mkdir(parents=True, exist_ok=True)
        prefix = f"{prefix}_data"

        self.returns_assets.to_csv(path / Path(f"{prefix}_returns.csv"))
        self.returns_cum.to_csv(path / Path(f"{prefix}_cum_returns.csv"))
        self.returns_total.to_csv(path / Path(f"{prefix}_total_returns.csv"))
        self.corr.to_csv(path / Path(f"{prefix}__corr.csv"))
        self.cov.to_csv(path / Path(f"{prefix}__cov.csv"))
        self.mean_sd.to_csv(path / Path(f"{prefix}__mean_sd.csv"))

    def save_results(self, path: Path, prefix: str = "experiment"):

        self.save_data(path=path, prefix=prefix)
        self.save_figs(path=path, prefix=prefix)
