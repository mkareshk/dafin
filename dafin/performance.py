import numpy as np
import pandas as pd


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
        date_start = self.__returns.index[0].date()
        date_end = self.__returns.index[-1].date()
        date_diff = date_end - date_start

        busday_num = np.busday_count(date_start, date_end)
        days_num = int(365.25 * (busday_num / date_diff.days))

        self.__annualized_mean_sd = pd.DataFrame(columns=["mean", "sd"])
        self.__annualized_mean_sd["mean"] = (1 + self.__returns.mean()) ** days_num - 1
        self.__annualized_mean_sd["sd"] = self.__returns.std() * np.sqrt(days_num)

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
