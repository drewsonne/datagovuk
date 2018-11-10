import csv
from io import StringIO

import chardet

from datagovuk.data_processors.base import PluginBase


class CSVProcessor(PluginBase):
    handlers = ['csv']

    def _process(self, data):
        response = []

        encoding = chardet.detect(data)['encoding']

        csvfile = StringIO(data.decode(encoding))
        sample = csvfile.read(1024)
        csvfile.seek(0)

        sniffer = csv.Sniffer()
        skip_first = sniffer.has_header(sample)

        reader = csv.reader(csvfile)
        for row in reader:
            if skip_first:
                header = row
                skip_first = False
                continue
            response.append(dict(zip(header, row)))
        return response
