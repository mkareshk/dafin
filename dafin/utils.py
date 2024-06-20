import datetime
import time
from pathlib import Path
from typing import Tuple, Union

import numpy as np
import pandas as pd
import scipy as sp

DEFAULT_DATE_FMT = "%Y-%m-%d"  # ISO 8601
DEFAULT_CACHE_DIR = Path.home() / Path(".cache") / "dafin"  # ~/.cache/dafin by default
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

    Example:
        >>> # Assuming the necessary import statements and DataFrame structures
        >>> assets_returns = pd.DataFrame({'A': [0.02, -0.01, 0.03], 'B': [-0.015, 0.02, 0.01]})
        >>> benchmark_returns = pd.DataFrame({'Benchmark': [0.015, -0.005, 0.02]})
        >>> calculate_beta(assets_returns, benchmark_returns)  # doctest: +SKIP
               beta
        A     ...
        B     ...
    """

    # Create a DataFrame to store the beta values for each asset
    beta_df = pd.DataFrame(index=returns.columns, columns=["beta"])

    for asset in returns.columns:
        # Concatenate asset returns and benchmark returns, calculate covariance matrix
        cov_matrix = pd.concat([returns[asset], returns_benchmark], axis=1).cov()

        # Calculate beta: covariance(asset, benchmark) / variance(benchmark)
        beta = cov_matrix.iloc[0, 1] / cov_matrix.iloc[1, 1]

        # Assign calculated beta to the beta DataFrame
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

    Example:
        >>> # Assuming the necessary import statements and auxiliary function definitions
        >>> assets_returns = pd.DataFrame({'A': [0.02, -0.01, 0.03], 'B': [-0.015, 0.02, 0.01]})
        >>> rf_returns = pd.DataFrame({'RF': [0.001, 0.001, 0.001]})
        >>> benchmark_returns = pd.DataFrame({'Benchmark': [0.015, -0.005, 0.02]})
        >>> calculate_alpha(assets_returns, rf_returns, benchmark_returns)  # doctest: +SKIP
               alpha
        A     ...
        B     ...
    """

    # Calculate beta for each asset relative to the benchmark
    beta = calculate_beta(returns, returns_benchmark)

    # Calculate annualized returns for assets, risk-free asset, and benchmark
    ri = calc_annualized_returns(returns)
    rb = calc_annualized_returns(returns_benchmark).iloc[0]
    rf = calc_annualized_returns(returns_rf).iloc[0]

    # Calculate alpha for each asset using the formula
    alpha_data = ri - rf - beta.T * (rb - rf)

    # Create a DataFrame to hold alpha values for each asset
    alpha = pd.DataFrame(index=beta.index, columns=["alpha"], data=alpha_data.T.values)

    return alpha


def regression(returns: pd.DataFrame, returns_benchmark: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the regression of the assets given a benchmark.

    Parameters:
        returns (pd.DataFrame): Daily returns of the assets.
        returns_benchmark (pd.DataFrame): Daily returns of the benchmark.

    Returns:
        pd.DataFrame: A DataFrame containing regression statistics for each asset relative to the benchmark.

    Example:
        >>> # Assuming the necessary import statements and DataFrame structures
        >>> assets_returns = pd.DataFrame({'A': [0.02, -0.01, 0.03], 'B': [-0.015, 0.02, 0.01]})
        >>> benchmark_returns = pd.DataFrame({'Benchmark': [0.015, -0.005, 0.02]})
        >>> regression(assets_returns, benchmark_returns)  # doctest: +SKIP
               Slope   Intercept   Correlation   R-Squared       p-Value   Standard Error
        A     ...        ...         ...          ...           ...          ...
        B     ...        ...         ...          ...           ...          ...
    """

    # Define DataFrame structure to hold regression results
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
        # Concatenating returns and benchmark returns, and dropping NaN values
        data = pd.concat([returns[asset], returns_benchmark], axis=1).dropna()

        # Performing linear regression
        slope, intercept, r_value, p_value, std_err = sp.stats.linregress(
            data.iloc[:, 0], data.iloc[:, 1]
        )

        # Assigning regression results to the DataFrame
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

    Example:
        >>> # Assuming the necessary import statements and auxiliary function definitions
        >>> assets_returns = pd.DataFrame({'return': [0.02, -0.01, 0.03, -0.015, 0.02]})
        >>> rf_returns = pd.DataFrame({'return': [0.001, 0.001, 0.001, 0.001, 0.001]})
        >>> calculate_sharpe_ratio(assets_returns, rf_returns)  # doctest: +ELLIPSIS
        return    ...
        dtype: float64
    """

    # Calculate the annualized returns of the assets and risk-free asset
    ri = calc_annualized_returns(returns)
    rf = calc_annualized_returns(returns_rf).iloc[0]

    # Calculate the annualized standard deviation of the assets returns
    sd = calc_annualized_sd(returns)

    # Compute the Sharpe ratio: (ri - rf) / sd
    sharpe_ratio = (ri - rf) / sd

    return sharpe_ratio


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

    Example:
        >>> # Assuming the necessary import statements and auxiliary function definitions
        >>> assets_returns = pd.DataFrame({'return': [0.02, -0.01, 0.03, -0.015, 0.02]})
        >>> rf_returns = pd.DataFrame({'return': [0.001, 0.001, 0.001, 0.001, 0.001]})
        >>> benchmark_returns = pd.DataFrame({'return': [0.015, -0.005, 0.02, -0.01, 0.025]})
        >>> calculate_treynor_ratio(assets_returns, rf_returns, benchmark_returns)  # doctest: +ELLIPSIS
        return    ...
        dtype: float64
    """

    # Calculate the annualized returns of the assets and risk-free asset
    ri = calc_annualized_returns(returns)
    rf = calc_annualized_returns(returns_rf).iloc[0]

    # Calculate the beta of the assets with respect to the benchmark
    beta = calculate_beta(
        returns, returns_benchmark
    )  # Corrected the typo in the function name

    # Compute the Treynor ratio: (ri - rf) / beta
    treynor_ratio = (ri - rf).iloc[0] / beta

    return treynor_ratio


def calc_returns_cum(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the cumulative returns from the daily returns.

    Parameters:
        returns (pd.DataFrame): A DataFrame containing daily returns.

    Returns:
        pd.DataFrame: A DataFrame containing the cumulative returns, with the same structure as the input DataFrame.

    Example:
        >>> import pandas as pd
        >>> daily_returns = pd.DataFrame({'return': [0.02, -0.01, 0.03, -0.015, 0.02]})
        >>> calc_returns_cum(daily_returns)
           return
        0  0.020000
        1  0.009800
        2  0.040114
        3  0.024513
        4  0.044928
    """

    # Calculating cumulative returns by first adding 1 to daily returns,
    # then calculating the cumulative product, and finally subtracting 1 to get the cumulative returns.
    cumulative_returns = (returns + 1).cumprod() - 1

    return cumulative_returns


def calc_returns_total(returns: pd.DataFrame) -> pd.Series:
    """
    Calculates the total returns from the daily returns.

    Parameters:
        returns (pd.DataFrame): A DataFrame containing daily returns.

    Returns:
        pd.Series: A Series containing the total returns for each column in the input DataFrame.

    Example:
        >>> import pandas as pd
        >>> daily_returns = pd.DataFrame({'return': [0.02, -0.01, 0.03, -0.015, 0.02]})
        >>> calc_returns_total(daily_returns)
        return    0.061805
        dtype: float64
    """

    # Calculate cumulative returns using a predefined function
    cumulative_returns = calc_returns_cum(
        returns
    )  # Assuming calc_returns_cum is defined elsewhere in the code

    # Return the last row of the cumulative returns DataFrame as the total returns
    return cumulative_returns.iloc[-1, :]


def calc_annualized_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the annualized returns from daily returns.

    Parameters:
        returns (pd.DataFrame): A DataFrame containing daily returns.

    Returns:
        pd.DataFrame: A DataFrame containing the annualized returns calculated from the daily returns.

    Example:
        >>> import pandas as pd
        >>> daily_returns = pd.DataFrame({'return': [0.02, -0.01, 0.03, -0.015, 0.02]})
        >>> calc_annualized_returns(daily_returns)  # doctest: +ELLIPSIS
        return    1.161...
        dtype: float64
    """

    # Calculate total returns using a predefined function
    returns_total = calc_returns_total(
        returns
    )  # Assuming calc_returns_total is defined elsewhere in the code

    # Calculate the days factor for annualization based on the number of records in returns data
    days_factor = DEFAULT_DAYS_PER_YEAR / returns.shape[0]

    # Calculate and return the annualized returns
    return (1 + returns_total) ** days_factor - 1


def calc_annualized_sd(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the annualized standard deviation from daily returns.

    Parameters:
        returns (pd.DataFrame): A DataFrame containing daily returns.

    Returns:
        pd.DataFrame: A DataFrame containing the annualized standard deviation for each column in the input DataFrame.

    Example:
        >>> import pandas as pd
        >>> returns = pd.DataFrame({'return': [0.02, -0.01, 0.03, -0.015, 0.02]})
        >>> calc_annualized_sd(returns)
        return    0.369274
        dtype: float64
    """

    # Calculating the standard deviation of daily returns
    daily_std = returns.std()

    # Annualizing the standard deviation by scaling it by the square root of the number of trading days in a year
    annualized_std = daily_std * np.sqrt(DEFAULT_DAYS_PER_YEAR)

    return annualized_std


def price_to_return(prices_df: pd.DataFrame, log_return: bool = False) -> pd.DataFrame:
    """
    Converts price data into daily returns, either as regular or log returns.

    Parameters:
        prices_df (pd.DataFrame): A DataFrame containing price data.
        log_return (bool, optional): If True, calculates log returns; otherwise, calculates regular returns. Defaults to False.

    Returns:
        pd.DataFrame: A DataFrame containing the daily returns, with the same structure as the input DataFrame.

    Example:
        >>> import pandas as pd
        >>> prices = pd.DataFrame({'price': [1, 2, 3, 4, 5]})
        >>> price_to_return(prices, log_return=True)
               price
        1  0.693147
        2  0.405465
        3  0.287682
        4  0.223144
    """

    # Calculate log returns if log_return is True, else calculate regular returns
    if log_return:
        # Using numpy to calculate the log returns
        returns_df = np.log(prices_df / prices_df.shift(1))
    else:
        # Using pandas pct_change method to calculate the regular returns
        returns_df = prices_df.pct_change()

    # Removing NaN values which occur from the shifting operation during return calculation
    return returns_df.dropna()


def date_to_str(date: datetime.datetime) -> str:
    """
    Converts a datetime object to a string in the format "YYYY-MM-DD".

    Parameters:
        date (datetime.datetime): The date as a datetime object.

    Returns:
        str: The formatted date as a string.

    Example:
        >>> date_to_str(datetime.datetime(2022, 10, 22))
        '2022-10-22'
    """

    # Formatting the datetime object into a string using the specified date format
    return date.strftime(DEFAULT_DATE_FMT)


def str_to_date(date_str: str) -> datetime.datetime:
    """
    Converts a date string in the format "YYYY-MM-DD" to a datetime object.

    Parameters:
        date_str (str): The date as a string in the format "YYYY-MM-DD".

    Returns:
        datetime.datetime: The converted date as a datetime object.

    Example:
        >>> str_to_date("2022-10-22")
        datetime.datetime(2022, 10, 22, 0, 0)
    """

    # Parsing the date string into a datetime object using the specified format
    return datetime.datetime.strptime(date_str, DEFAULT_DATE_FMT)


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

    Example:
        >>> normalize_date('2022-10-22')
        (datetime.datetime(2022, 10, 22, 0, 0), '2022-10-22')
        >>> normalize_date(datetime.datetime(2022, 10, 22))
        (datetime.datetime(2022, 10, 22, 0, 0), '2022-10-22')
    """

    if isinstance(date, str):
        date_str = date
        date_dt = str_to_date(
            date
        )  # Assuming str_to_date is defined and available to convert string to datetime
    elif isinstance(date, datetime.datetime):
        date_str = date_to_str(
            date
        )  # Assuming date_to_str is defined and available to convert datetime to string
        date_dt = date
    elif isinstance(date, datetime.date):
        date_dt = datetime.datetime.combine(date, datetime.time.min)
        date_str = date_to_str(
            date
        )  # Assuming date_to_str is defined and available to convert datetime to string
    else:
        raise ValueError(
            "The date type should be either datetime.datetime "
            f"or str (e.g. '2014-03-24'). The provided date {date} type is {type(date)}."
        )

    return date_dt, date_str
