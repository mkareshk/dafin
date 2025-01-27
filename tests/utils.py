import pandas as pd

# assets
single_asset = ["SPY"]
double_assets = ["SPY", "BND"]
thriple_assets = ["SPY", "BND", "GDL"]
assets_list = [single_asset, double_assets, thriple_assets]

# dates
date_start_list = ["2015-01-01", "2015-01-01"]
date_end_list = ["2019-12-31", "2015-09-30"]

# cols
col_price_list = ["Open", "Close"]


# params
def assert_returns(returns_assets, assets):

    if isinstance(assets, str):
        assets = [assets]

    assert isinstance(returns_assets, pd.DataFrame)
    assert not returns_assets.empty
    assert returns_assets.shape[1] == len(assets)
    assert all(returns_assets.isna())


pnames_returns = "assets,date_start,date_end,col_price"
params_returns = []
for a in assets_list:
    for s in date_start_list:
        for e in date_end_list:
            for c in col_price_list:
                params_returns.append((a, s, e, c))

pnames_performance = "assets,asset_single"
params_performance = []
for a in assets_list:
    for s in [single_asset[0], None]:
        params_performance.append((a, s))
