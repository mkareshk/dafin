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
