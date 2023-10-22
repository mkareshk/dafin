from dafin import ReturnsData, Performance

## Parameters

# tickers
assets = ["ORCL", "AAPL", "AMZN", "SPY"]
assets_rf = ["BND"]
assets_benchmark = ["SPY"]
# date
date_start = "2020-01-01"
date_end = "2022-12-31"

## Print the Returns Data
returns = ReturnsData(assets=assets).get_returns(
    date_start=date_start, date_end=date_end
)
returns_rf = ReturnsData(assets=assets_rf).get_returns(
    date_start=date_start, date_end=date_end
)
returns_benchmark = ReturnsData(assets=assets_benchmark).get_returns(
    date_start=date_start, date_end=date_end
)
performance = Performance(
    returns_assets=returns, returns_rf=returns_rf, returns_benchmark=returns_benchmark
)

print(performance.summary)
