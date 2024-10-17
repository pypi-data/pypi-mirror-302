from typing import Optional

from datadock.src.filings import Filings
from datadock.src.blob_storage import BlobStorageCSV


class CurrentFilings(Filings):
    def __init__(self, scrape: bool = False) -> None:
        index_table = BlobStorageCSV().table_array()
        self._scrape = scrape
        super().__init__(index_table, scrape=self._scrape)

    def get_filings(self) -> Optional[Filings]:

        filings = Filings(self.data)

        if not filings:
            return None

        # Finally sort by filing date
        filings = Filings(filings.data.sort_by([("Filing Date", "descending")]))
        return filings
