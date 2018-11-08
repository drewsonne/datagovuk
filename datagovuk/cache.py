import hashlib
import os
from pathlib import Path

import pandas as pd


class DataCache(object):
    def __init__(self):
        self._path = Path(os.path.join(
            os.path.expanduser('~'),
            '.cache'
        ))
        if not self._path.exists():
            self._path.mkdir(exist_ok=True)
        self._path = self._path / 'datagovuk'
        if not self._path.exists():
            self._path.mkdir(exist_ok=True)

    def __call__(self, identifier):
        cache_file = self._path / (hashlib.md5(identifier.encode()).hexdigest() + '.parquet')

        def func_wrapper(func):
            def cache_handler(*args, **kwargs):
                if cache_file.exists():
                    df = pd.read_parquet(cache_file)
                else:
                    df = func(*args, **kwargs)
                    df.to_parquet(cache_file)
                return df

            return cache_handler

        return func_wrapper

cache = DataCache()
