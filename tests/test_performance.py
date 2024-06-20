from pathlib import Path

import pandas as pd
import pytest

from dafin import Performance, ReturnsData

from .utils import assert_returns, clean_dir, params_performance, pnames_performance


@pytest.mark.parametrize(pnames_performance, params_performance)
def test_use_case_performance(assets, asset_single, path_cache):

    clean_dir(path_cache)

    returns_assets = ReturnsData(assets, path_cache=path_cache).get_returns()
    assert_returns(returns_assets, assets)

    if asset_single:
        returns_rf = ReturnsData(asset_single, path_cache=path_cache).get_returns()
        returns_benchmark = ReturnsData(
            [asset_single], path_cache=path_cache
        ).get_returns()
        assert_returns(returns_rf, asset_single)
        assert_returns(returns_benchmark, asset_single)
    else:
        returns_rf = None
        returns_benchmark = None

    performance = Performance(
        returns_assets=returns_assets,
        returns_rf=returns_rf,
        returns_benchmark=returns_benchmark,
    )
    performance.save_results(path_cache / Path("test_results"))
    assert (performance.summary["Alpha"], pd.DataFrame)
    performance.plot_returns(yscale="symlog")
    print(performance)

    clean_dir(path_cache)
