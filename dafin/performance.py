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
        Initializes the Performance object with provided asset, risk-free, and benchmark returns.

        Parameters:
        - returns_assets: A DataFrame containing the returns of multiple assets.
        - returns_rf: A DataFrame containing the returns of the risk-free asset (optional).
        - returns_benchmark: A DataFrame containing the returns of the benchmark asset (optional).

        Raises:
        - ValueError: If returns_assets DataFrame is empty.

        Examples:
        >>> returns_assets = pd.DataFrame({"Asset1": [0.01, 0.02, -0.01], "Asset2": [-0.01, 0.03, 0.02]})
        >>> performance = Performance(returns_assets)
        >>> performance.returns_assets
           Asset1  Asset2
        0    0.01   -0.01
        1    0.02    0.03
        2   -0.01    0.02
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

    @property
    def returns_cum(self) -> pd.DataFrame:
        """Returns the cumulative returns of the assets.

        Returns:
            pd.DataFrame: Cumulative returns.
        """

        return calc_returns_cum(self.returns_assets)

    @property
    def returns_total(self) -> pd.DataFrame:
        """Returns the total returns of the assets.

        Returns:
            pd.DataFrame: Total returns.
        """

        return calc_returns_total(self.returns_assets)

    @property
    def cov(self) -> pd.DataFrame:
        """Returns the covariance matrix of the assets.

        Returns:
            pd.DataFrame: Covariance matrix.
        """

        return self.returns_assets.cov()

    @property
    def corr(self) -> pd.DataFrame:
        """Returns the correlation matrix of the assets.

        Returns:
            pd.DataFrame: Correlation matrix.
        """

        return self.returns_assets.corr()

    @property
    def returns_assets_annualized(self) -> pd.DataFrame:
        """Returns the annualized returns of the assets.

        Returns:
            pd.DataFrame: Annualized returns.
        """

        return calc_annualized_returns(self.returns_assets)

    @property
    def sd_assets_annualized(self) -> pd.DataFrame:
        """Returns the annualized standard deviation of the assets.

        Returns:
            pd.DataFrame: Annualized standard deviation.
        """

        return calc_annualized_sd(self.returns_assets)

    @property
    def returns_rf_annualized(self) -> pd.DataFrame:
        """Returns the annualized returns of the risk-free asset.

        Returns:
            pd.DataFrame: Annualized returns of the risk-free asset.
        """

        return calc_annualized_returns(self.returns_rf).iloc[0]

    @property
    def returns_benchmark_annualized(self) -> pd.DataFrame:
        """Returns the annualized returns of the benchmark.

        Returns:
            pd.DataFrame: Annualized returns of the benchmark.
        """

        return calc_annualized_returns(self.returns_benchmark).iloc[0]

    @property
    def mean_sd(self) -> pd.DataFrame:
        """Returns the mean and standard deviation of the assets.

        Returns:
            pd.DataFrame: Mean and standard deviation of the assets.
        """

        mean_sd = pd.DataFrame(index=self.assets, columns=["mean", "sd"])
        mean_sd["mean"] = self.returns_assets_annualized
        mean_sd["sd"] = self.sd_assets_annualized
        return mean_sd

    @property
    def beta(self) -> pd.DataFrame:
        """Returns the beta of the assets.

        Returns:
            pd.DataFrame: Beta of the assets.
        """

        return calculate_beta(self.returns_assets, self.returns_benchmark)

    @property
    def alpha(self) -> pd.DataFrame:
        """Returns the alpha of the assets.

        Returns:
            pd.DataFrame: Alpha of the assets.
        """

        return calculate_alpha(
            self.returns_assets,
            self.returns_rf,
            self.returns_benchmark,
        )

    @property
    def regression(self) -> pd.DataFrame:
        """Returns the regression of the assets.

        Returns:
            pd.DataFrame: Regression of the assets.
        """

        return regression(self.returns_assets, self.returns_benchmark)

    @property
    def sharpe_ratio(self) -> pd.DataFrame:
        return calculate_sharpe_ratio(
            self.returns_assets,
            self.returns_rf,
        )

    @property
    def treynor_ratio(self) -> pd.DataFrame:
        return calculate_treynor_ratio(
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
            + f"\t- List of Assets: {self.assets}\n"
            + f"\t- Risk-Free Asset: {self.asset_rf}\n"
            + f"\t- Benchmark Asset: {self.asset_benchmark}\n"
            # date
            + f"\t- Start Date: {self.date_start_str}\n"
            + f"\t- End Date: {self.date_end_str}\n"
            # performance
            + f"\t - Performance Summary:\n{self.summary}\n\n\n"
        )

    @property
    def summary(self) -> pd.DataFrame:
        """Returns a summary of the performance.

        Returns:
            pd.DataFrame: Summary of the performance.
        """

        s = pd.DataFrame()
        s.index = self.returns_assets.columns

        s["total_returns"] = self.returns_total
        s["expected_returns"] = self.returns_assets_annualized
        s["standard_deviation"] = self.sd_assets_annualized
        s["alpha"] = self.alpha
        s["beta"] = self.beta
        s["sharpe_ratio"] = self.sharpe_ratio
        s["treynor_ratio"] = self.treynor_ratio

        s = pd.concat([s, self.regression], axis=1)

        return s

    def plot_returns(
        self, alpha: float = 1, legend: bool = True, yscale: str = "linear"
    ):

        fig, ax = self.plot.plot_trend(
            df=self.returns_assets,
            title="",
            xlabel="Date",
            ylabel="Expected Annual Returns",
            alpha=alpha,
            marker="o",
            legend=legend,
            yscale=yscale,
        )
        return fig, ax

    def plot_cum_returns(self):
        fig, ax = self.plot.plot_trend(
            df=self.returns_cum,
            title="",
            xlabel="Date",
            marker=None,
            ylabel="Cumulative Returns",
            yscale="linear",
        )
        return fig, ax

    def plot_total_returns(self, legend: bool = False):
        fig, ax = self.plot.plot_bar(
            df=self.returns_total,
            title="",
            xlabel="Assets",
            ylabel=f"Total Returns ({self.date_start_str} to {self.date_end_str})",
            legend=legend,
        )
        return fig, ax

    def plot_dist_returns(self, yscale: str = "symlog"):
        fig, ax = self.plot.plot_box(
            df=self.returns_assets,
            title=f"",
            xlabel="Assets",
            ylabel=f"Daily Returns",
            figsize=(15, 8),
            yscale=yscale,
        )
        return fig, ax

    def plot_corr(self):
        fig, ax = self.plot.plot_heatmap(
            df=self.returns_assets,
            relation_type="corr",
            title="",
            annotate=True,
        )
        return fig, ax

    def plot_cov(self):
        fig, ax = self.plot.plot_heatmap(
            df=self.returns_assets,
            relation_type="cov",
            title="",
            annotate=True,
        )
        return fig, ax

    def plot_mean_sd(
        self,
        colour="tab:blue",
        fig=None,
        ax=None,
    ):

        xlabel = "Standard Deviation"
        ylabel = "Expected Returns"

        fig, ax = self.plot.plot_scatter(
            df=self.mean_sd,
            title="",
            xlabel=xlabel,
            ylabel=ylabel,
            colour=colour,
            fig=fig,
            ax=ax,
        )
        return fig, ax

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
        self.save_data(prefix=prefix, path=path)
        self.save_figs(prefix=prefix, path=path)
