import pytest
import pandas as pd

from dafin import FundamentalData
from .utils import clean_dir, pnames_fundamental, params_fundamental


@pytest.mark.parametrize(pnames_fundamental, params_fundamental)
def test_use_case_fundamental_data(assets, path_cache):

    clean_dir(path_cache)

    for _ in range(2):
        fundamental_data = FundamentalData(
            assets=assets,
            path_cache=path_cache,
        )

        fundamental_info = fundamental_data.info
        assert isinstance(fundamental_info, pd.DataFrame)
        assert fundamental_info.shape[0] == len(assets)

    clean_dir(path_cache)
