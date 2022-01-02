# dafin

# Install

```bash
pip install dafin
```

# Returns Data

Create a `Returns` object:

```python
from dafin import Returns

returns_data = Returns(asset_list=["AAPL", "GOOGL"])
```

Here is the available data:

- Asset List
    ```python
    returns_data.asset_list
    ```
    ```bash
    ['AAPL', 'GOOGL']
    ```

- Price Column
    ```python
    returns_data.col_price
    ```
    ```bash
    'Close'
    ```

- Start Date
    ```python
    returns_data.date_start_str
    ```
    ```bash
    '2000-01-01'
    ```

- End Date
    ```python
    returns_data.date_end_str
    ```
    ```bash
    '2020-12-31'
    ```

- Business Days No.
    ```python
    returns_data.business_day_num
    ```
    ```bash
    5478
    ```

- Signature
    ```python
    returns_data.signature
    ```
    ```bash
    'cfdd9b6cc8'
    ```

- Prices
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

- Returns
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

- Cumulative Returns
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

- Mean-SD Returns
    ```python
    returns_data.mean_sd
    ```
    ```bash
            mean        sd
    AAPL   0.001576  0.020908
    GOOGL  0.001107  0.019029
    ```
