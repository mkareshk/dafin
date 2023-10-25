from pathlib import Path
from dafin import ReturnsData, Performance

def main():
    """
    Fetch returns data for assets, risk-free assets, and benchmark. Then compute and print the performance summary.
    
    Doctest:
    >>> isinstance(path, Path)
    True
    """
    
    # Define assets, risk-free assets, and benchmark tickers
    assets = ["AAPL", "AMZN", "SPY"]
    assets_rf = ["BND"]
    assets_benchmark = ["SPY"]

    # Define date range
    date_start = "2020-01-01"
    date_end = "2022-12-31"

    # Define path for saving results
    path = Path('experiments')

    # Fetch returns data for the defined assets
    returns = ReturnsData(assets=assets).get_returns(
        date_start=date_start, date_end=date_end
    )
    returns_rf = ReturnsData(assets=assets_rf).get_returns(
        date_start=date_start, date_end=date_end
    )
    returns_benchmark = ReturnsData(assets=assets_benchmark).get_returns(
        date_start=date_start, date_end=date_end
    )

    # Calculate performance metrics
    performance = Performance(
        returns_assets=returns, returns_rf=returns_rf, returns_benchmark=returns_benchmark
    )

    # Save performance metrics and associated figures to the specified path
    performance.save_figs(path)
    performance.save_data(path)
    performance.save_results(path)

    # Print the performance summary
    print(performance.summary)

if __name__ == "__main__":
    main()
