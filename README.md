# dafin

# dafin

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

```python
from dafin import Returns

returns_data = Returns(
    asset_list=["AAPL", "GOOGL"],
    date_start="2015-01-01",
    date_end="2020-12-31",
    col_price="Close",
)
```

Here is the available data:

- List of assets. (`list`)

    ```python
    returns_data.asset_list
    ```

    ```bash
    ['AAPL', 'GOOGL']
    ```

- The price column. (`str`)

    ```python
    returns_data.col_price
    ```

    ```bash
    'Close'
    ```

- The starting date. (`str`)

    ```python
    returns_data.date_start_str
    ```

    ```bash
    '2000-01-01'
    ```

- The ending data. (`str`)

    ```python
    returns_data.date_end_str
    ```

    ```bash
    '2020-12-31'
    ```

- The number of business days. (`int`)

    ```python
    returns_data.business_day_num
    ```

    ```bash
    5478
    ```

- The data signature that can be used as a unique identifier. (`str`)

    ```python
    returns_data.signature
    ```

    ```bash
    'cfdd9b6cc8'
    ```

- Asset prices. (`pandas.DataFrame`)

    ```python
    returns_data.prices
    ```

    ```bash
                    AAPL        GOOGL
    Date                               
    2004-08-19    0.470173    50.220219
    2004-08-20    0.471551    54.209209
    2004-08-23    0.475838    54.754753
    2004-08-24    0.489158    52.487488
    2004-08-25    0.505999    53.053055
    ...                ...          ...
    2021-12-27  180.330002  2958.129883
    2021-12-28  179.289993  2933.739990
    2021-12-29  179.380005  2933.100098
    2021-12-30  178.199997  2924.010010
    2021-12-31  177.570007  2897.040039

    [4374 rows x 2 columns]
    ```

- Asset returns. (`pandas.DataFrame`)

    ```python
    returns_data.returns
    ```

    ```bash
                    AAPL     GOOGL
    Date                          
    2004-08-20  0.002930  0.079430
    2004-08-23  0.009091  0.010064
    2004-08-24  0.027993 -0.041408
    2004-08-25  0.034429  0.010775
    2004-08-26  0.048714  0.018019
    ...              ...       ...
    2021-12-27  0.022975  0.006738
    2021-12-28 -0.005767 -0.008245
    2021-12-29  0.000502 -0.000218
    2021-12-30 -0.006578 -0.003099
    2021-12-31 -0.003535 -0.009224

    [4373 rows x 2 columns]
    ```

- Cumulative asset returns. (`pandas.DataFrame`)

    ```python
    returns_data.cum_returns
    ```

    ```bash
                    AAPL      GOOGL
    Date                             
    2004-08-20    0.002930   0.079430
    2004-08-23    0.012048   0.090293
    2004-08-24    0.040378   0.045147
    2004-08-25    0.076197   0.056408
    2004-08-26    0.128623   0.075444
    ...                ...        ...
    2021-12-27  382.539581  57.903166
    2021-12-28  380.327612  57.417507
    2021-12-29  380.519056  57.404766
    2021-12-30  378.009325  57.223761
    2021-12-31  376.669415  56.686727

    [4373 rows x 2 columns]
    ```

- Mean-SD of returns.  (`pandas.DataFrame`)

    ```python
    returns_data.mean_sd
    ```
    
    ```bash
            mean        sd
    AAPL   0.001576  0.020908
    GOOGL  0.001107  0.019029
    ```


