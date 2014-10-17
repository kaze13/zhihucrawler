import json
from scrapy.contrib.exporter import BaseItemExporter

class UnicodeJsonLinesItemExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        self._configure(kwargs)
        self.file = file
        self.encoder = json.JSONEncoder(ensure_ascii=False, **kwargs)

    def export_item(self, item):
        itemdict = dict(self._get_serialized_fields(item))
        self.file.write(self.encoder.encode(itemdict) + '\n')
