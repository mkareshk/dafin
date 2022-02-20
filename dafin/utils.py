import numpy as np


def annualize_returns(returns, days_per_year):

    return (1 + returns.mean()) ** days_per_year - 1


def annualize_sd(returns, days_per_year):

    return returns.std() * np.sqrt(days_per_year)


def get_days_per_year(date_start, date_end):

    date_diff = date_end - date_start
    busday_num = np.busday_count(date_start, date_end)

    return int(365.25 * (busday_num / date_diff.days))
