import datetime
from typing import List

import pandas as pd

from dafin import Returns

from .utils import check_figure, ASSET_LIST


returns_data = Returns(asset_list=ASSET_LIST)


def test_type_asset_list():
    assert isinstance(returns_data.asset_list, List)


def test_type_col_price():
    assert isinstance(returns_data.col_price, str)


def test_type_asset_date_start_str():
    assert isinstance(returns_data.date_start_str, str)


def test_type_date_end_str():
    assert isinstance(returns_data.date_end_str, str)


def test_type_asset_date_start():
    assert isinstance(returns_data.date_start, datetime.datetime)


def test_type_date_end():
    assert isinstance(returns_data.date_end, datetime.datetime)


def test_type_business_day_num():
    assert isinstance(returns_data.business_day_num, int)


def test_type_signature():
    assert isinstance(returns_data.signature, str)


def test_type_prices():
    assert isinstance(returns_data.prices, pd.DataFrame)


def test_type_returns():
    assert isinstance(returns_data.returns, pd.DataFrame)


def test_type_cum_returns():
    assert isinstance(returns_data.cum_returns, pd.DataFrame)


def test_type_total_returns():
    assert isinstance(returns_data.total_returns, pd.Series)


def test_type_mean_sd():
    assert isinstance(returns_data.mean_sd, pd.DataFrame)


def test_type_annualized_mean_sd():
    assert isinstance(returns_data.annualized_mean_sd, pd.DataFrame)


def test_type_days_per_year():
    assert isinstance(returns_data.days_per_year, int)


def test_type_plot_prices():
    fig, ax = returns_data.plot_prices()
    check_figure(fig, ax)


def test_type_plot_returns():
    fig, ax = returns_data.plot_returns()
    check_figure(fig, ax)


def test_type_plot_cum_returns():
    fig, ax = returns_data.plot_cum_returns()
    check_figure(fig, ax)


def test_type_plot_dist_returns():
    fig, ax = returns_data.plot_dist_returns()
    check_figure(fig, ax)


def test_type_plot_corr():
    fig, ax = returns_data.plot_corr()
    check_figure(fig, ax)


def test_type_plot_cov():
    fig, ax = returns_data.plot_cov()
    check_figure(fig, ax)


def test_type_plot_cov():
    fig, ax = returns_data.plot_cov()
    check_figure(fig, ax)


def test_type_plot_cov():
    fig, ax = returns_data.plot_cov()
    check_figure(fig, ax)


def test_type_plot_cov():
    fig, ax = returns_data.plot_cov()
    check_figure(fig, ax)


def test_type_plot_mean_sd():
    fig, ax = returns_data.plot_mean_sd(annualized=True)
    check_figure(fig, ax)


def test_type_plot_mean_sd():
    fig, ax = returns_data.plot_mean_sd(annualized=False)
    check_figure(fig, ax)
