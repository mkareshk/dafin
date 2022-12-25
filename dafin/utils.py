import datetime
from pathlib import Path

import numpy as np
import yahoo_fin.stock_info as si

DEFAULT_DATE_FMT = "%Y-%m-%d"
DEFAULT_CACHE_DIR = Path.home() / Path(".cache") / "dafin"

SUPPROTED_INDECES = [
    "dow",
    "ftse100",
    "ftse250",
    "ibovespa",
    "nasdaq",
    "nifty50",
    "niftybank",
    "other",
    "sp500",
]


def get_days_per_year(returns):

    try:

        annual_counts = returns.resample("Y").count().iloc[:, 0]

        if annual_counts.shape[0] > 1:
            days_per_year = int(annual_counts[annual_counts > 245].mean())
        else:
            days_per_year = 252

        check_type(days_per_year, "days_per_year", int)

        return days_per_year

    except:
        return 252


def annualize_returns(returns, days_per_year=None):

    if not days_per_year:
        days_per_year = get_days_per_year(returns)

    return (1 + returns.mean()) ** days_per_year - 1


def annualize_sd(returns, days_per_year=None):

    if not days_per_year:
        days_per_year = get_days_per_year(returns)

    return returns.std() * np.sqrt(days_per_year)


def price_to_return(prices_df, log_return=False):

    if log_return:
        return np.log(prices_df / prices_df.shift(1)).dropna()
    else:
        return prices_df.pct_change().dropna()


def date_to_str(date: datetime.datetime):

    return date.strftime(DEFAULT_DATE_FMT)


def str_to_date(date_str: str):

    return datetime.datetime.strptime(date_str, DEFAULT_DATE_FMT)


def normalize_date(date):

    if isinstance(date, str):
        date_str = date
        date = str_to_date(date)

    elif isinstance(date, datetime.datetime):
        date_str = date_to_str(date)

    else:
        raise ValueError(
            "date type should be either datetime.date "
            f"or str (e.g. '2014-03-24'). {date} type is {type(date)}."
        )

    return date, date_str


def check_type(var, var_name: str, expected_type):

    if type(var) != expected_type:
        msg = f"Type {var_name} should be {expected_type}, but a {type(var)} is passed."
        raise TypeError(msg)


def get_index_tickers(index: list):

    if index not in SUPPROTED_INDECES:
        raise ValueError(f"Index {index} is not supported: {SUPPROTED_INDECES}.")

    tickers = eval(f"si.tickers_{index}()")
    return [item.replace(".", "-") for item in tickers]
