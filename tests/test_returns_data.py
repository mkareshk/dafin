import pytest

from dafin import ReturnsData

from .utils import assert_returns, clean_dir, params_returns, pnames_returns


@pytest.mark.parametrize(pnames_returns, params_returns)
def test_use_case_returns_data(assets, date_start, date_end, col_price, path_cache):

    clean_dir(path_cache)

    for _ in range(2):

        returns_data = ReturnsData(
            assets=assets,
            col_price=col_price,
            path_cache=path_cache,
        )
        returns_assets = returns_data.get_returns(
            date_start=date_start, date_end=date_end
        )

        assert_returns(returns_assets, assets)

        str(returns_data)
        hash(returns_data)

    clean_dir(path_cache)
