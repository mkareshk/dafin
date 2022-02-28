import datetime
from typing import List
import unittest
import pandas as pd
from parameterized import parameterized

from dafin import Returns

from .utils import *


returns_data_str = Returns(
    asset_list=ASSET_LIST, date_start=DATE_START_STR, date_end=DATE_END_STR
)
returns_data = Returns(asset_list=ASSET_LIST, date_start=DATE_START, date_end=DATE_END)
testcases = [
    ["date_str", returns_data_str],
    ["date_datetime", returns_data],
]


class TypeTest(unittest.TestCase):
    @parameterized.expand(testcases)
    def test_type_asset_list(self, name, returns_data):
        assert isinstance(returns_data.asset_list, List)

    @parameterized.expand(testcases)
    def test_type_col_price(self, name, returns_data):
        assert isinstance(returns_data.col_price, str)

    @parameterized.expand(testcases)
    def test_type_asset_date_start_str(self, name, returns_data):
        assert isinstance(returns_data.date_start_str, str)

    @parameterized.expand(testcases)
    def test_type_date_end_str(self, name, returns_data):
        assert isinstance(returns_data.date_end_str, str)

    @parameterized.expand(testcases)
    def test_type_asset_date_start(self, name, returns_data):
        assert isinstance(returns_data.date_start, datetime.datetime)

    @parameterized.expand(testcases)
    def test_type_date_end(self, name, returns_data):
        assert isinstance(returns_data.date_end, datetime.datetime)

    @parameterized.expand(testcases)
    def test_type_business_day_num(self, name, returns_data):
        assert isinstance(returns_data.business_day_num, int)

    @parameterized.expand(testcases)
    def test_type_signature(self, name, returns_data):
        assert isinstance(returns_data.signature, str)

    @parameterized.expand(testcases)
    def test_type_prices(self, name, returns_data):
        assert isinstance(returns_data.prices, pd.DataFrame)

    @parameterized.expand(testcases)
    def test_type_returns(self, name, returns_data):
        assert isinstance(returns_data.returns, pd.DataFrame)

    @parameterized.expand(testcases)
    def test_type_cum_returns(self, name, returns_data):
        assert isinstance(returns_data.cum_returns, pd.DataFrame)

    @parameterized.expand(testcases)
    def test_type_total_returns(self, name, returns_data):
        assert isinstance(returns_data.total_returns, pd.Series)

    @parameterized.expand(testcases)
    def test_type_mean_sd(self, name, returns_data):
        assert isinstance(returns_data.mean_sd, pd.DataFrame)

    @parameterized.expand(testcases)
    def test_type_annualized_mean_sd(self, name, returns_data):
        assert isinstance(returns_data.annualized_mean_sd, pd.DataFrame)

    @parameterized.expand(testcases)
    def test_type_days_per_year(self, name, returns_data):
        assert isinstance(returns_data.days_per_year, int)

    @parameterized.expand(testcases)
    def test_type_plot_prices(self, name, returns_data):
        fig, ax = returns_data.plot_prices()
        check_figure(fig, ax)

    @parameterized.expand(testcases)
    def test_type_plot_returns(self, name, returns_data):
        fig, ax = returns_data.plot_returns()
        check_figure(fig, ax)

    @parameterized.expand(testcases)
    def test_type_plot_cum_returns(self, name, returns_data):
        fig, ax = returns_data.plot_cum_returns()
        check_figure(fig, ax)

    @parameterized.expand(testcases)
    def test_type_plot_dist_returns(self, name, returns_data):
        fig, ax = returns_data.plot_dist_returns()
        check_figure(fig, ax)

    @parameterized.expand(testcases)
    def test_type_plot_corr(self, name, returns_data):
        fig, ax = returns_data.plot_corr()
        check_figure(fig, ax)

    @parameterized.expand(testcases)
    def test_type_plot_cov(self, name, returns_data):
        fig, ax = returns_data.plot_cov()
        check_figure(fig, ax)

    @parameterized.expand(testcases)
    def test_type_plot_cov(self, name, returns_data):
        fig, ax = returns_data.plot_cov()
        check_figure(fig, ax)

    @parameterized.expand(testcases)
    def test_type_plot_cov(self, name, returns_data):
        fig, ax = returns_data.plot_cov()
        check_figure(fig, ax)

    @parameterized.expand(testcases)
    def test_type_plot_cov(self, name, returns_data):
        fig, ax = returns_data.plot_cov()
        check_figure(fig, ax)

    @parameterized.expand(testcases)
    def test_type_plot_mean_sd(self, name, returns_data):
        fig, ax = returns_data.plot_mean_sd(annualized=True)
        check_figure(fig, ax)

    @parameterized.expand(testcases)
    def test_type_plot_mean_sd(self, name, returns_data):
        fig, ax = returns_data.plot_mean_sd(annualized=False)
        check_figure(fig, ax)
