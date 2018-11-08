import pandas as pd

from datagovuk.cache import cache


class BaseCall(object):
    indices = []
    column_types = {}
    cache_identifier = None
    columns = []

    def __init__(self):
        self.session = None

    def __call__(self, session):
        @cache(self.cache_identifier)
        def call_hander():
            self.session = session
            response = self._fetch()

            def indexer(i):
                indices = [o[i] for o in response]
                return list(set(indices))

            indices = list(map(
                indexer,
                self.indices
            ))

            df = pd.DataFrame(
                response,
                columns=self.columns,
                index=indices
            )

            for col, dtype in self.column_types.items():
                df[col] = df[col].astype(dtype)

            return df

        return call_hander()

    def _fetch(self):
        raise NotImplemented()
