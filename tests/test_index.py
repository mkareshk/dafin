from dafin import get_index_tickers


def test_index_tickers():
    dow_list = get_index_tickers("dow")
    assert isinstance(dow_list, list)
    assert len(dow_list) > 25
