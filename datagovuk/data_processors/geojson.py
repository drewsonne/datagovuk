import tempfile

import geopandas as gpd

from datagovuk.data_processors.base import PluginBase


class GeoJSONProcessor(PluginBase):
    handlers = ['geojson']

    def _process(self, data):
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(data)
            tmp.seek(0)

            df = gpd.read_file(tmp.name)

        return df

    def encoder(self):
        pass
