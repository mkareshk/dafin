# dafin
dafin is an open-source Python package designed for collecting, storing, and visualizing financial data from any source. It offers user-friendly APIs that present data in Pandas dataframes, making it easy to visualize with standard Matplotlib methods.

# install

dafin is available on [PyPI](https://pypi.org/), so you can install it by running the following command:

```bash
pip install dafin
```

## Usage

### Usage Manual for `ReturnsData` Class

The `ReturnsData` class is designed for managing and retrieving asset return data. It allows users to initialize the data with asset symbols, specify a column for price data, and provide a cache path. The class also offers a method to retrieve daily return data for a specific date range.

#### 1. Initializing the ReturnsData Class

You can initialize the `ReturnsData` class by passing a list of asset symbols or a single asset symbol as a string. You can also specify the column name for price data and the path where cache files will be stored.

Here is an example of how to create an instance of the `ReturnsData` class:

```python
from dafin import ReturnsData

# Create an instance of ReturnsData with a list of asset symbols and specify the column for price data
data_instance = ReturnsData(['AAPL', 'GOOGL'], col_price="Close")

# Verify the instance is created
print(isinstance(data_instance, ReturnsData))  # This should print: True
```

##### Parameters:

- `assets`: A list of asset symbols or a single asset symbol as a string. This parameter is required.
- `col_price`: The name of the column for price data. This parameter is optional and defaults to "Close".
- `path_cache`: The path where cache files are stored. This parameter is optional and defaults to DEFAULT_CACHE_DIR.

#### 2. Retrieving Daily Returns Data

The `get_returns` method allows you to retrieve the daily returns data for a specified date range. If no date range is provided, it will return all available data.

Here is an example of how to use the `get_returns` method:

```python
# Assuming that the instance has a 'returns' attribute as a DataFrame and the 'normalize_date' function is defined

# Retrieve daily returns data for a specific date range
returns_data = data_instance.get_returns('2022-01-01', '2022-01-10')

# Print the retrieved data
print(returns_data)  # This will print the DataFrame with the daily returns data between '2022-01-01' and '2022-01-10'
```

##### Parameters:

- `date_start`: The start date as a string or `datetime.datetime` object. This parameter is optional and defaults to None, in which case all available data will be returned.
- `date_end`: The end date as a string or `datetime.datetime` object. This parameter is optional and defaults to None, in which case all available data will be returned.

## Example

```python
from pathlib import Path

from dafin import Performance, ReturnsData


def main():
    """
    Fetch returns data for assets, risk-free assets, and benchmark. Then compute and print the performance summary.
    """

    # Define assets, risk-free assets, and benchmark tickers
    assets = ["AAPL", "AMZN", "SPY"]
    assets_rf = ["BND"]
    assets_benchmark = ["SPY"]

    # Define date range
    date_start = "2015-01-01"
    date_end = "2019-12-31"

    # Define path for saving results
    path = Path("experiments")

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
        returns_assets=returns,
        returns_rf=returns_rf,
        returns_benchmark=returns_benchmark,
    )

    # Save performance metrics and associated figures to the specified path
    performance.save_figs(path)
    performance.save_data(path)
    performance.save_results(path)

    # Print the performance summary
    print(performance.summary)


if __name__ == "__main__":
    main()
```
