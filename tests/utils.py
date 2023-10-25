from pathlib import Path

import shutil
import pandas as pd

from dafin.utils import DEFAULT_CACHE_DIR

# assets
single_asset = ["SPY"]
double_assets = ["SPY", "BND"]
thriple_assets = ["SPY", "BND", "GDL"]
assets_list = [single_asset, double_assets, thriple_assets]

# dates
date_start_list = ["2015-01-01", "2015-01-01"]
date_end_list = ["2019-12-31", "2015-09-30"]

# cols
col_price_list = ["Open", "Close", "Adj Close"]

# path
DEFAULT_TEST_DIR = DEFAULT_CACHE_DIR / Path("test")

# params
def assert_returns(returns_assets, assets):

    if isinstance(assets, str):
        assets = [assets]

    assert isinstance(returns_assets, pd.DataFrame)
    assert not returns_assets.empty
    assert returns_assets.shape[1] == len(assets)
    assert all(returns_assets.isna())


def clean_dir(dir_path: Path) -> None:
    if dir_path.is_dir():
        shutil.rmtree(dir_path)


pnames_returns = "assets,date_start,date_end,col_price,path_cache"
params_returns = []
for a in assets_list:
    for s in date_start_list:
        for e in date_end_list:
            for c in col_price_list:
                params_returns.append((a, s, e, c, DEFAULT_TEST_DIR))

pnames_fundamental = "assets,path_cache"
params_fundamental = []
for a in assets_list:
    params_fundamental.append((a, DEFAULT_TEST_DIR))

pnames_performance = "assets,asset_single,path_cache"
params_performance = []
for a in assets_list:
    for s in [single_asset[0], None]:
        params_performance.append((a, s, DEFAULT_TEST_DIR))
