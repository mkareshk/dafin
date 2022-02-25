from tabulate import tabulate
from dafin import Returns


def print_table(df):
    print(tabulate(df.head(3), headers=["Date"] + list(df.columns), tablefmt="html"))


## Parameters

# tickers
asset_list = ["SPY", "BND", "GLD"]

# date
date_start = "2008-01-01"
date_end = "2020-12-31"

## Create the market instance
returns_data = Returns(
    asset_list=asset_list,
    date_start=date_start,
    date_end=date_end,
)

# prices
print_table(returns_data.prices)
fig, ax = returns_data.plot_prices(figsize=(8, 4))
fig.savefig("prices.png")

exit()
# cum_returns
returns_data.cum_returns
fig, ax = returns_data.plot_cum_returns()

# total returns
returns_data
fig, ax = returns_data.plot_total_returns()

# dist
fig, ax = returns_data.plot_dist_returns()

# cov
fig, ax = returns_data.plot_cov()

# corr
fig, ax = returns_data.plot_corr()

# mean-sd
fig, ax = returns_data.plot_mean_sd(annualized=True)
