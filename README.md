# dafin



![Build Status](https://github.com/mkareshk/dafin/actions/workflows/ci.yaml/badge.svg)

dafin is an open-source Python package to collect, store and visualize financial data. It provides an easy-to-use set of APIs to access the data as Pandas dataframes and visualize them using standard matplotlib methods. 

# install

dafin is available on [PyPI](https://pypi.org/), and you can install it by running the following command:

```bash
pip install dafin
```

Note that dafin needs python>=3.10 and it is tested on Ubuntu 22.04.

# Usage

## Asset Returns

The `ReturnsData` class provides the returns data. In our illustrative example here, we aim to collect the _Adj Close_ returns data of SPDR S&P 500 ETF Trust (_SPY_), Vanguard Total Bond Market Index Fund (_BND_), and SPDR Gold Shares (_GLD_) between _2010-01-01_ and _2019-12-31_. 


```python
from dafin import ReturnsData, Performance

# tickers
assets = ['SPY', 'BND', 'GLD']

# date
date_start = "2010-01-01"
date_end = "2019-12-31"

# retrieve asset returns
returns_data = ReturnsData(assets)
returns = returns_data.get_returns(date_start, date_end)

print(returns)
```

The returns would be:

```bash
                                SPY       BND       GLD
Date                                                   
2010-01-04 00:00:00-05:00  0.016960  0.001146  0.023204
2010-01-05 00:00:00-05:00  0.002647  0.002923 -0.000911
2010-01-06 00:00:00-05:00  0.000704 -0.000381  0.016500
2010-01-07 00:00:00-05:00  0.004221 -0.000761 -0.006188
2010-01-08 00:00:00-05:00  0.003328  0.001015  0.004963
...                             ...       ...       ...
2019-12-24 00:00:00-05:00  0.000031  0.000955  0.009432
2019-12-26 00:00:00-05:00  0.005323  0.000955  0.007857
2019-12-27 00:00:00-05:00 -0.000248  0.001431 -0.000351
2019-12-30 00:00:00-05:00 -0.005513 -0.000357  0.002108
2019-12-31 00:00:00-05:00  0.002429 -0.001072  0.001893

[2516 rows x 3 columns]
```

## Asset Performance
The `Performance` class provides utilities to calculate the assets' performance.


```python
# risk-free asset returns
returns_rf = ReturnsData(assets = 'SHY')
returns_rf = returns_rf.get_returns(date_start, date_end)

# benchmark returns
returns_benchmark = ReturnsData('IVV')
returns_benchmark = returns_benchmark.get_returns(date_start, date_end)

# create the performance object
performance = Performance(returns, returns_rf, returns_benchmark)


## Performance summary
print(performance.summary)
```


Here is the performance summary:
```bash
     Total Returns  Expected Returns  Standard Deviation     Alpha      Beta  ...  Intercept Correlation R-Squared  p-Value Standard Error
SPY       2.527579          0.146296            0.146694  0.000581  0.995586  ...  -0.000001    0.998551  0.997105      0.0       0.001076
BND       0.427878          0.036720            0.032511  0.035299  -0.07045  ...   0.000751   -0.318825  0.101649      0.0       0.085549
GLD       0.331656          0.041410            0.154716  0.032854 -0.017742  ...   0.000547   -0.016872  0.000285  0.39758       0.018964

[3 rows x 13 columns]
```