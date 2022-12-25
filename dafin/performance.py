from pathlib import Path

import scipy as sc
import numpy as np
import pandas as pd

from dafin.utils import *
from dafin.plot import Plot


class Performance:
    def __init__(
        self,
        returns_assets: pd.DataFrame,
        returns_rf: pd.DataFrame = None,
        returns_benchmark: pd.DataFrame = None,
        returns_period: int = None,
    ) -> None:

        # check values and types of the asset returns
        self.returns_assets = returns_assets
        check_type(self.returns_assets, "returns_assets", pd.DataFrame)
        if returns_assets.empty:
            raise ValueError("returns_assets cannot be empty")

        # use a zero vector as the risk-free asset if it is not passed
        if returns_rf is None:
            idx = self.returns_assets.index
            data = np.zeros(self.returns_assets.shape[0])
            self.returns_rf = pd.DataFrame(index=idx, data=data)
        else:
            self.returns_rf = returns_rf
        check_type(self.returns_assets, "returns_assets", pd.DataFrame)

        # use the risk-free returns as benchmark if it is not passed
        if returns_benchmark is None:
            self.returns_benchmark = self.returns_rf.copy()
        else:
            self.returns_benchmark = returns_benchmark
        check_type(self.returns_benchmark, "returns_benchmark", pd.DataFrame)

        # if data_period id not passed, assume that the data is daily by default
        if not returns_period:
            self.returns_period = get_days_per_year(self.returns_assets)
        else:
            self.returns_period = returns_period
        check_type(self.returns_period, "returns_period", int)

        # derived parameters
        self.assets = list(self.returns_assets.columns)
        self.asset_rf = list(self.returns_rf.columns)[0]
        self.asset_benchmark = list(self.returns_benchmark.columns)[0]
        self.date_start_str = date_to_str(self.returns_assets.index[0])
        self.date_end_str = date_to_str(self.returns_assets.index[-1])

        # plot
        self.plot = Plot()

    @property
    def returns_cum(self) -> pd.DataFrame:
        return (self.returns_assets + 1).cumprod() - 1

    @property
    def returns_total(self) -> pd.DataFrame:
        return self.returns_cum.iloc[-1, :].to_frame()

    @property
    def cov(self) -> pd.DataFrame:
        return self.returns_assets.cov()

    @property
    def corr(self) -> pd.DataFrame:
        return self.returns_assets.corr()

    @property
    def returns_assets_annualized(self) -> pd.DataFrame:
        return annualize_returns(self.returns_assets, self.returns_period)

    @property
    def sd_assets_annualized(self) -> pd.DataFrame:
        return annualize_sd(self.returns_assets, self.returns_period)

    @property
    def returns_rf_annualized(self) -> pd.DataFrame:
        return annualize_returns(self.returns_rf, self.returns_period).iloc[0]

    @property
    def returns_benchmark_annualized(self) -> pd.DataFrame:
        return annualize_returns(self.returns_benchmark, self.returns_period).iloc[0]

    @property
    def mean_sd(self) -> pd.DataFrame:
        mean_sd = pd.DataFrame(index=self.assets, columns=["mean", "sd"])
        mean_sd["mean"] = self.returns_assets_annualized
        mean_sd["sd"] = self.sd_assets_annualized
        return mean_sd

    @property
    def beta(self) -> pd.DataFrame:
        # beta = cov(asset, benchmark) / var(benchmark)

        rb = self.returns_benchmark
        beta = pd.DataFrame(index=self.returns_assets.columns, columns=["beta"])

        for asset in self.returns_assets.columns:
            cov = pd.concat([self.returns_assets[asset], rb], axis=1).cov()
            beta.loc[asset, "beta"] = cov.iloc[0, 1] / cov.iloc[1, 1]

        return beta

    @property
    def alpha(self) -> pd.DataFrame:
        # Alpha = asset – rf – beta * (benchmark - rf)

        beta = self.beta
        b = beta.to_numpy()
        n_assets = self.returns_assets.shape[1]
        ri = self.returns_assets_annualized.to_numpy().reshape(n_assets, -1)
        rb = self.returns_benchmark_annualized
        rf = self.returns_rf_annualized
        alpha_data = ri - rf - b * (rb - rf)
        alpha = pd.DataFrame(index=beta.index, columns=["alpha"], data=alpha_data)

        return alpha

    @property
    def regression(self) -> pd.DataFrame:

        df_index = self.returns_assets.columns
        df_cols = [
            "Slope",
            "Intercept",
            "Correlation",
            "R-Squared",
            "p-Value",
            "Standard Error",
        ]

        regression = pd.DataFrame(index=df_index, columns=df_cols)
        b = self.returns_benchmark

        for i in regression.index:
            X = pd.concat([self.returns_assets[i], b], axis=1).to_numpy()
            slope, intercept, r_value, p_value, std_err = sc.stats.linregress(X)
            regression.loc[i, :] = (
                slope,
                intercept,
                r_value,
                r_value**2,
                p_value,
                std_err,
            )

        return regression

    @property
    def sharpe_ratio(self) -> pd.DataFrame:
        excess_returns = self.returns_assets_annualized - self.returns_rf_annualized
        sharpe_ratio = excess_returns / self.sd_assets_annualized
        return sharpe_ratio

    @property
    def treynor_ratio(self) -> pd.DataFrame:
        excess_returns = self.returns_assets_annualized - self.returns_rf_annualized
        treynor_ratio = excess_returns / self.beta["beta"]
        return treynor_ratio

    def __str__(self) -> str:
        return (
            "Performance:\n"
            # assets
            + f"\t- List of Assets: {self.assets}\n"
            + f"\t- Risk-Free Asset: {self.asset_rf}\n"
            + f"\t- Benchmark Asset: {self.asset_benchmark}\n"
            # date
            + f"\t- Start Date: {self.date_start_str}\n"
            + f"\t- End Date: {self.date_end_str}\n"
            + f"\t- Days Per Year: {self.returns_period}\n"
            # performance
            + f"\t - Performance Summary:\n{self.summary}\n\n\n"
        )

    @property
    def summary(self) -> pd.DataFrame:

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
