import pandas as pd

from dafin.utils import annualize_returns, annualize_sd, get_days_per_year


class AssetPerformance:
    def __init__(self, returns) -> None:

        # returns
        self.__returns = returns

        # cum returns
        self.__cum_returns = (self.__returns + 1).cumprod() - 1

        # total returns
        self.__total_returns = self.__cum_returns.iloc[-1, :]

        # mean-sd
        self.__mean_sd = pd.DataFrame(columns=["mean", "sd"])
        self.__mean_sd["mean"] = self.__returns.mean()
        self.__mean_sd["sd"] = self.__returns.std()

        # annualized
        days_per_year = get_days_per_year(
            date_start=self.__returns.index[0].date(),
            date_end=self.__returns.index[-1].date(),
        )

        self.__annualized_mean_sd = pd.DataFrame(columns=["mean", "sd"])
        self.__annualized_mean_sd["mean"] = annualize_returns(
            returns=self.__returns, days_per_year=days_per_year
        )
        self.__annualized_mean_sd["sd"] = annualize_sd(
            returns=self.__returns, days_per_year=days_per_year
        )

        self.__days_per_year = days_per_year

    @property
    def returns(self):
        return self.__returns

    @property
    def cum_returns(self):
        return self.__cum_returns

    @property
    def total_returns(self):
        return self.__total_returns

    @property
    def mean_sd(self):
        return self.__mean_sd

    @property
    def annualized_mean_sd(self):
        return self.__annualized_mean_sd

    @property
    def days_per_year(self):
        return self.__days_per_year
