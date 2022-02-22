import matplotlib

ASSET_LIST = ["SPY", "GLD", "BND"]

DATE_START = "2020-11-01"
DATE_END = "2020-12-31"


def check_figure(fig, ax):
    assert isinstance(fig, matplotlib.figure.Figure)
    assert isinstance(ax, matplotlib.axes.Axes)
