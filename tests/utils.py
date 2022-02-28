import datetime

import matplotlib

ASSET_LIST = ["SPY", "GLD", "BND"]

DATE_START_STR = "2020-11-01"
DATE_END_STR = "2020-12-31"

date_fmt = "%Y-%m-%d"
DATE_START = datetime.datetime.strptime(DATE_START_STR, date_fmt)
DATE_END = datetime.datetime.strptime(DATE_END_STR, date_fmt)


def check_figure(fig, ax):
    assert isinstance(fig, matplotlib.figure.Figure)
    assert isinstance(ax, matplotlib.axes.Axes)
