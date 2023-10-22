# dafin

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
- `col_price`: The name of the column for price data. This parameter is optional and defaults to "Adj Close".
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






```python
from dafin import ReturnsData, Performance

# tickers
assets = ['SPY', 'BND', 'GLD']

# date
date_start = "2010-01-01"
date_end = "2019-12-31"

# retrieve asset returns
returns_data = ReturnsData(assets = assets)
returns = returns_data.get_returns(date_start = date_start, date_end = date_end)

returns_rf = ReturnsData(assets = 'SHY')
returns_rf = returns_rf.get_returns(date_start = date_start, date_end = date_end)

returns_benchmark = ReturnsData(assets = 'IVV')
returns_benchmark = returns_benchmark.get_returns(date_start = date_start, date_end = date_end)

# calculate performance metrics
performance = Performance(returns_assets=returns, returns_rf=returns_rf, returns_benchmark=returns_benchmark)

```



df =  performance.summary
df = df.reset_index()
df['Date'] = df['Date'].dt.strftime('%Y/%m/%d')

print(tabulate(df.head(3), headers=df.columns, tablefmt="double_outline", floatfmt=".2f", showindex=True))

formatters={'Date': lambda x: x.strftime('%Y/%m/%d')}
print(df.reset_index().head(3).to_string(index=False, float_format=lambda x: '%0.2f' % x, formatters=formatters))



### Prices

```python
returns_data.prices
```

```
╔════════════╦════════╦═══════╦═══════╗
║ Date       ║    SPY ║   BND ║   GLD ║
╠════════════╬════════╬═══════╬═══════╣
║ 2007/04/10 ║ 106.68 ║ 46.94 ║ 67.16 ║
║ 2007/04/11 ║ 106.24 ║ 46.82 ║ 67.08 ║
║ 2007/04/12 ║ 106.71 ║ 46.81 ║ 66.99 ║
╚════════════╩════════╩═══════╩═══════╝
```

### retruns

```python
returns_data.get_returns(date_start = date_start, date_end = date_end)
```

```
╔════════════╦═══════╦═══════╦═══════╗
║ Date       ║   SPY ║   BND ║   GLD ║
╠════════════╬═══════╬═══════╬═══════╣
║ 2010/01/04 ║  0.02 ║  0.00 ║  0.02 ║
║ 2010/01/05 ║  0.00 ║  0.00 ║ -0.00 ║
║ 2010/01/06 ║  0.00 ║ -0.00 ║  0.02 ║
╚════════════╩═══════╩═══════╩═══════╝
```

### Cumulative Returns
```python
performance.returns_cum
```

```
╔════════════╦═══════╦═══════╦═══════╗
║ Date       ║   SPY ║   BND ║   GLD ║
╠════════════╬═══════╬═══════╬═══════╣
║ 2010/01/04 ║  0.02 ║  0.00 ║  0.02 ║
║ 2010/01/05 ║  0.02 ║  0.00 ║  0.02 ║
║ 2010/01/06 ║  0.02 ║  0.00 ║  0.04 ║
╚════════════╩═══════╩═══════╩═══════╝
```

### Total Returns
```python
performance.returns_total
```

```
╔═════════╦══════════════╗
║ index   ║   2019-12-31 ║
╠═════════╬══════════════╣
║ SPY     ║         2.53 ║
║ BND     ║         0.43 ║
║ GLD     ║         0.33 ║
╚═════════╩══════════════╝
```


### Distributions of Returns


## Relationships of Assets

```python
performance.cov
```
```
╔══════════╦══════════╦══════════╗
║      SPY ║      BND ║      GLD ║
╠══════════╬══════════╬══════════╣
║  0.00009 ║ -0.00001 ║ -0.00000 ║
║ -0.00001 ║  0.00000 ║  0.00001 ║
║ -0.00000 ║  0.00001 ║  0.00010 ║
╚══════════╩══════════╩══════════╝
```


```python
performance.corr
```
```
╔═══════╦═══════╦═══════╗
║   SPY ║   BND ║   GLD ║
╠═══════╬═══════╬═══════╣
║  1.00 ║ -0.32 ║ -0.02 ║
║ -0.32 ║  1.00 ║  0.30 ║
║ -0.02 ║  0.30 ║  1.00 ║
╚═══════╩═══════╩═══════╝
```


## Expected Returns vs. Volatility

```python
performance.mean_sd
```
```
╔═════╦════════╦══════╗
║     ║   mean ║   sd ║
╠═════╬════════╬══════╣
║ SPY ║   0.15 ║ 0.15 ║
║ BND ║   0.04 ║ 0.03 ║
║ GLD ║   0.04 ║ 0.15 ║
╚═════╩════════╩══════╝
```

### Performance Summary
```python
performance.summary
```

```
╔═════╦═════════════════╦════════════════════╦══════════════════════╦═════════╦════════╦════════════════╦═════════════════╦═════════╦═════════════╦═══════════════╦═════════════╦═══════════╦══════════════════╗
║     ║   Total Returns ║   Expected Returns ║   Standard Deviation ║   Alpha ║   Beta ║   Sharpe Ratio ║   Treynor Ratio ║   Slope ║   Intercept ║   Correlation ║   R-Squared ║   p-Value ║   Standard Error ║
╠═════╬═════════════════╬════════════════════╬══════════════════════╬═════════╬════════╬════════════════╬═════════════════╬═════════╬═════════════╬═══════════════╬═════════════╬═══════════╬══════════════════╣
║ SPY ║            2.53 ║               0.15 ║                 0.15 ║    0.00 ║   1.00 ║           0.92 ║            0.14 ║    1.00 ║       -0.00 ║          1.00 ║        1.00 ║      0.00 ║             0.00 ║
║ BND ║            0.43 ║               0.04 ║                 0.03 ║    0.04 ║  -0.07 ║           0.79 ║           -0.37 ║   -1.44 ║        0.00 ║         -0.32 ║        0.10 ║      0.00 ║             0.09 ║
║ GLD ║            0.33 ║               0.04 ║                 0.15 ║    0.03 ║  -0.02 ║           0.20 ║           -1.72 ║   -0.02 ║        0.00 ║         -0.02 ║        0.00 ║      0.40 ║             0.02 ║
╚═════╩═════════════════╩════════════════════╩══════════════════════╩═════════╩════════╩════════════════╩═════════════════╩═════════╩═════════════╩═══════════════╩═════════════╩═══════════╩══════════════════╝
```



### 






![Build Status](https://github.com/mkareshk/dafin/actions/workflows/ci.yaml/badge.svg)

dafin is an open-source Python package to collect, store and visualize financial data regardless of the data source. It provides an easy-to-use set of APIs to access the data as Pandas dataframes and visualize them using standard matplotlib methods. The current version of dafin uses [yfinance](https://github.com/ranaroussi/yfinance), but in case of any changes in the APIs of yfinance or Yahoo Finance, dafin still remains backward compatible.

## Financial data

Here are different types of financial data that dafin collects and visualizes:

1. `Returns`: The data of asset prices and returns. This includes raw daily prices, daily returns, cumulative returns, and correlations and covariance matrix of the returns.
2. `Fundamental`: The fundamental data of assets including financial reports. 

# install

dafin is available on [PyPI](https://pypi.org/), so you can install it by running the following command:

```bash
pip install dafin
```

Note that dafin needs python>=3.8 and it is tested on Ubuntu 20.04.

# Usage

## Asset Returns

The `Returns` class provides the returns data. Let's first create a `Returns` object. In our illustrative example, we aim to collect the _close_ returns data of Apple (_AAPL_) and Google (_GOOGL_) between _2015/01/01_ and _2020/12/31_. 

