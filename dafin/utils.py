import datetime
from typing import Tuple, Union

import numpy as np
import pandas as pd
import pytz
import scipy as sp

DEFAULT_DATE_FMT = "%Y-%m-%d"  # ISO 8601
DEFAULT_DAYS_PER_YEAR = 252  # 252 trading days per year


def calculate_beta(
    returns: pd.DataFrame, returns_benchmark: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculates the beta of the assets given a benchmark.
    Beta = covariance(asset returns, benchmark returns) / variance(benchmark returns)

    Parameters:
        returns (pd.DataFrame): Daily returns of the assets.
        returns_benchmark (pd.DataFrame): Daily returns of the benchmark.

    Returns:
        pd.DataFrame: A DataFrame containing the beta of each asset relative to the benchmark.
    """

    beta_df = pd.DataFrame(index=returns.columns, columns=["beta"])

    for asset in returns.columns:
        cov_matrix = pd.concat([returns[asset], returns_benchmark], axis=1).cov()
        beta = cov_matrix.iloc[0, 1] / cov_matrix.iloc[1, 1]
        beta_df.loc[asset, "beta"] = beta

    return beta_df


def calculate_alpha(
    returns: pd.DataFrame, returns_rf: pd.DataFrame, returns_benchmark: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculates the alpha of the assets given a benchmark.
    Alpha = asset return - risk-free return - beta * (benchmark return - risk-free return)

    Parameters:
        returns (pd.DataFrame): Daily returns of the assets.
        returns_rf (pd.DataFrame): Daily returns of the risk-free asset.
        returns_benchmark (pd.DataFrame): Daily returns of the benchmark.

    Returns:
        pd.DataFrame: Alpha of the assets.
    """

    beta = calculate_beta(returns, returns_benchmark)

    ri = calc_annualized_returns(returns)
    rb = calc_annualized_returns(returns_benchmark).iloc[0]
    rf = calc_annualized_returns(returns_rf).iloc[0]

    alpha_data = ri - rf - beta.T * (rb - rf)

    return pd.DataFrame(index=beta.index, columns=["alpha"], data=alpha_data.T.values)


def regression(returns: pd.DataFrame, returns_benchmark: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the regression of the assets given a benchmark.

    Parameters:
        returns (pd.DataFrame): Daily returns of the assets.
        returns_benchmark (pd.DataFrame): Daily returns of the benchmark.

    Returns:
        pd.DataFrame: A DataFrame containing regression statistics for each asset relative to the benchmark.
    """

    df_cols = [
        "Slope",
        "Intercept",
        "Correlation",
        "R-Squared",
        "p-Value",
        "Standard Error",
    ]
    regression_results = pd.DataFrame(index=returns.columns, columns=df_cols)

    for asset in returns.columns:
        data = pd.concat([returns[asset], returns_benchmark], axis=1).dropna()
        slope, intercept, r_value, p_value, std_err = sp.stats.linregress(
            data.iloc[:, 0], data.iloc[:, 1]
        )
        regression_results.loc[asset] = (
            slope,
            intercept,
            r_value,
            r_value**2,
            p_value,
            std_err,
        )

    return regression_results


def calculate_sharpe_ratio(
    returns: pd.DataFrame, returns_rf: pd.DataFrame
) -> pd.Series:
    """
    Calculates the Sharpe ratio of the assets given a risk-free asset.

    Parameters:
        returns (pd.DataFrame): Daily returns of the assets.
        returns_rf (pd.DataFrame): Daily returns of the risk-free asset.

    Returns:
        pd.Series: Sharpe ratio of the assets.
    """

    ri = calc_annualized_returns(returns)
    rf = calc_annualized_returns(returns_rf).iloc[0]
    sd = calc_annualized_sd(returns)
    return (ri - rf) / sd


def calculate_treynor_ratio(
    returns: pd.DataFrame, returns_rf: pd.DataFrame, returns_benchmark: pd.DataFrame
) -> pd.Series:
    """
    Calculates the Treynor ratio of the assets given a risk-free asset and a benchmark.

    Parameters:
        returns (pd.DataFrame): Daily returns of the assets.
        returns_rf (pd.DataFrame): Daily returns of the risk-free asset.
        returns_benchmark (pd.DataFrame): Daily returns of the benchmark.

    Returns:
        pd.Series: Treynor ratio of the assets.
    """

    ri = calc_annualized_returns(returns)
    rf = calc_annualized_returns(returns_rf).iloc[0]
    beta = calculate_beta(returns, returns_benchmark)
    return (ri - rf).iloc[0] / beta


def calc_returns_cum(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the cumulative returns from the daily returns.

    Parameters:
        returns (pd.DataFrame): A DataFrame containing daily returns.

    Returns:
        pd.DataFrame: A DataFrame containing the cumulative returns, with the same structure as the input DataFrame.
    """
    return (returns + 1).cumprod() - 1


def calc_returns_total(returns: pd.DataFrame) -> pd.Series:
    """
    Calculates the total returns from the daily returns.

    Parameters:
        returns (pd.DataFrame): A DataFrame containing daily returns.

    Returns:
        pd.Series: A Series containing the total returns for each column in the input DataFrame.
    """
    return calc_returns_cum(returns).iloc[-1, :]


def calc_annualized_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the annualized returns from daily returns.

    Parameters:
        returns (pd.DataFrame): A DataFrame containing daily returns.

    Returns:
        pd.DataFrame: A DataFrame containing the annualized returns calculated from the daily returns.
    """
    returns_total = calc_returns_total(returns)
    days_factor = DEFAULT_DAYS_PER_YEAR / returns.shape[0]
    return (1 + returns_total) ** days_factor - 1


def calc_annualized_sd(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the annualized standard deviation from daily returns.

    Parameters:
        returns (pd.DataFrame): A DataFrame containing daily returns.

    Returns:
        pd.DataFrame: A DataFrame containing the annualized standard deviation for each column in the input DataFrame.
    """
    daily_std = returns.std()
    return daily_std * np.sqrt(DEFAULT_DAYS_PER_YEAR)


def price_to_return(prices_df: pd.DataFrame, log_return: bool = False) -> pd.DataFrame:
    """
    Converts price data into daily returns, either as regular or log returns.

    Parameters:
        prices_df (pd.DataFrame): A DataFrame containing price data.
        log_return (bool, optional): If True, calculates log returns; otherwise, calculates regular returns. Defaults to False.

    Returns:
        pd.DataFrame: A DataFrame containing the daily returns, with the same structure as the input DataFrame.
    """
    if log_return:
        returns_df = np.log(prices_df / prices_df.shift(1))
    else:
        returns_df = prices_df.pct_change()
    return returns_df.dropna()


def date_to_str(date: datetime.datetime) -> str:
    """
    Converts a datetime object to a string in the format "YYYY-MM-DD".

    Parameters:
        date (datetime.datetime): The date as a datetime object.

    Returns:
        str: The formatted date as a string.
    """
    return date.strftime(DEFAULT_DATE_FMT)


def str_to_date(date_str: str) -> datetime.datetime:
    """
    Converts a date string in the format "YYYY-MM-DD" to a datetime object.

    Parameters:
        date_str (str): The date as a string in the format "YYYY-MM-DD".

    Returns:
        datetime.datetime: The converted date as a datetime object.
    """
    return datetime.datetime.strptime(date_str, DEFAULT_DATE_FMT).replace(
        tzinfo=pytz.UTC
    )


def normalize_date(
    date: Union[datetime.datetime, str]
) -> Tuple[datetime.datetime, str]:
    """
    Converts a date to both a datetime object and a string, and returns them as a tuple.

    Parameters:
        date (Union[datetime.datetime, str]): The date, either as a datetime object or a string.

    Raises:
        ValueError: If the provided date is neither a datetime object nor a string.

    Returns:
        Tuple[datetime.datetime, str]: The date represented as a datetime object and a string.
    """

    if isinstance(date, str):
        date_str = date
        date_dt = str_to_date(date)
    elif isinstance(date, datetime.datetime):
        date_str = date_to_str(date)
    elif isinstance(date, datetime.date):
        date_dt = datetime.datetime.combine(date, datetime.time.min)
        date_str = date_to_str(date)
    else:
        raise ValueError(
            "The date type should be either datetime.datetime "
            f"or str (e.g. '2014-03-24'). The provided date {date} type is {type(date)}."
        )

    return date_dt, date_str
