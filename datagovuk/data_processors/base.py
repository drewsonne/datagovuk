import requests


class PluginBase(object):
    handlers = []

    def fetch(self, df):
        return self._process(
            self.get_raw_data(df['url'])
        )

    def get_raw_data(self, url):
        return requests.get(url).content

    def _process(self, data):
        raise NotImplemented()
