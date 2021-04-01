from cache_to_db_decorator import *
import numpy as np
import json
import requests
import time


# pytest tests
def test_decor1():
    @cache_to_db
    def caunt_cache(arr):
        for i in range(len(arr)):
            arr[i] = arr[i] ** 2
        return arr

    def caunt(arr):
        for i in range(len(arr)):
            arr[i] = arr[i] ** 2
        return arr

    assert caunt_cache([1, 2, 3]) == [1, 4, 9]
    assert caunt([23, 43, 87]) == caunt_cache([23, 43, 87])
    assert caunt([21, 21, 3]) == caunt_cache([21, 21, 3])


def test_decor_set():
    settings(drop_table=False)
    @cache_to_db
    def np_m_cache(arr):
        return arr.T * arr

    def np_m(arr):
        return arr.T * arr

    assert np_m(np.array([1, 2, 3])).all() == np_m_cache(np.array([1, 2, 3])).all()

def test_decot_time():
    settings(drop_table=False)
    @cache_to_db
    def get_data_cache():
        s = time.time()
        resp = requests.get('https://raw.githubusercontent.com/openfootball/world-cup.json/master/2018/worldcup.json')
        data = json.loads(resp.text)
        return data, time.time() - s

    def get_data():
        s = time.time()
        resp = requests.get('https://raw.githubusercontent.com/openfootball/world-cup.json/master/2018/worldcup.json')
        data = json.loads(resp.text)
        return data, time.time() - s

    print(get_data_cache()[1])
    print(get_data()[1])
    print(get_data_cache()[1])
    print(get_data()[1])
    assert get_data_cache()[0] == get_data()[0]