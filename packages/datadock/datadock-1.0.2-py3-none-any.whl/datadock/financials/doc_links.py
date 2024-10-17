import re
import pandas as pd
import pyarrow as pa
from dataclasses import dataclass
from typing import Tuple, List, Optional, Union

from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from datadock.core import DataPager
from datadock.src.api_base import SECRequestHandler
from datadock.src._rich_ import df_to_rich_table, repr_rich
from datadock.src._tabulate_ import df_to_tabulate_table
from datadock.src.custom_logger import CustomLogger


def get_document_url(cik, accession):
    if not cik and accession:
        return None
    da = DocumentFinancial(cik, accession)


class DocumentFinancial:
    def __init__(self, cik: str, accession_number: str) -> None:
        self._cik = cik
        self._accession_number = accession_number
        self._logger = self._get_logger()
        self._request_handler = self._get_request_handler()

    @classmethod
    def _get_logger(cls) -> CustomLogger:
        return CustomLogger().logger

    def _get_request_handler(self) -> SECRequestHandler:
        return SECRequestHandler(self._cik, self._accession_number)

    def get_document_links(self) -> Optional[Union[pa.Table, "DataDocFiling"]]:
        html_links, filing_id = self._request_handler

        if not html_links:
            return None

        html_links = self.get_r_html_links(html_links)

        # convert to pyarrow array table format
        html_link_array = pa.array(html_links, type=pa.string())
        # Convert lists to Arrow arrays
        schema = pa.schema(
            [
                ("HTML URLs", pa.string()),
            ]
        )

        html_pa_table = pa.Table.from_arrays([html_link_array], schema=schema)

        doc_table = DataDocFiling(html_pa_table, filing_id)

        return doc_table

    def parse_document_url(self, url: str):
        return self._request_handler.parse_document(url)

    @staticmethod
    def get_r_html_links(html_links: List[str]) -> List[str]:
        pattern = re.compile(r"R[1-9]\.htm$")
        r_htm_links = [link for link in html_links if pattern.search(link)]
        return r_htm_links


@dataclass
class FilingsState:
    page_start: int
    num_filings: int


class DataDocFiling:
    def __init__(
        self,
        html_link_index: pa.Table,
        filing_id: str,
        original_state: FilingsState = None,
    ) -> None:
        self.html_table = html_link_index
        self.filing_id = filing_id
        self._logger = CustomLogger().logger
        self.original_state = original_state or FilingsState(0, len(self.html_table))
        self.data_pager = DataPager(self.html_table)

    def to_pandas(self, *columns) -> Optional[pd.DataFrame]:
        if not self.html_table:
            return None
        data_frame = self.html_table.to_pandas()
        return data_frame.filter(columns) if len(columns) > 0 else data_frame

    def get_html_url(self, value: int):
        return CurrentDocument(html_url=self.html_table["HTML URLs"][value].as_py())

    def current(self):
        return self

    def next(self):
        """Show the next page"""
        data_page = self.data_pager.next()
        if data_page is None:
            self._logger.warning("End of data .. use prev() \u2190 ")
            return None
        start_index, _ = self.data_pager.current_range
        filings_state = FilingsState(page_start=start_index, num_filings=len(self))
        return DataDocFiling(
            data_page, filing_id=self.filing_id, original_state=filings_state
        )

    def previous(self):
        """
        Show the previous page of the data
        :return:
        """
        data_page = self.data_pager.previous()
        if data_page is None:
            self._logger.warning(" No previous data .. use next() \u2192 ")
            return None
        start_index, _ = self.data_pager.current_range
        filings_state = FilingsState(page_start=start_index, num_filings=len(self))
        return DataDocFiling(
            data_page, filing_id=self.filing_id, original_state=filings_state
        )

    def prev(self):
        """Alias for self.previous()"""
        return self.previous()

    def __iter__(self):
        self.n = 0
        return self

    def __len__(self) -> int:
        return len(self.html_table)

    def __getitem__(self, index: int):
        return self.get_html_url(index)

    def _page_index(self) -> range:
        """Create the range index to set on the page dataframe depending on where in the data we are"""
        if self.original_state:
            return range(
                self.original_state.page_start,
                self.original_state.page_start
                + min(self.data_pager.page_size, len(self.html_table)),
            )  # set the index to the size of the page
        else:
            return range(*self.data_pager.current_range)

    def __rich__(self) -> Panel:
        page = self.data_pager.current().to_pandas()
        page.index = self._page_index()

        # Show paging information
        page_info = (
            f"Showing {len(page)} of {self.original_state.num_filings:,} filings"
        )

        return Panel(
            Group(
                df_to_rich_table(
                    page,
                    title=f"DataDock HTML URL Filings ID: {self.filing_id}",
                    max_rows=len(page),
                ),
                Text(page_info),
            ),
            title="DataDock HTML URL Filings",
        )

    def __repr__(self):
        return repr_rich(self.__rich__())


class CurrentDocument:
    def __init__(self, html_url: str) -> None:
        self.html_url = html_url
        self._logger = CustomLogger().logger

    def open(self):
        import webbrowser

        return webbrowser.open(self.html_url)

    def __str__(self):
        """
        Return a string version of this filing e.g.

        Filing(form='10-K', filing_date='2018-03-08', company='CARBO CERAMICS INC',
              cik=1009672, accession_no='0001564590-18-004771')
        :return:
        """
        return f"HTML Filing URL: (url='{self.html_url}')"

    # def __tabulate__(self) -> Panel:
    #     page = self.data_pager.current().to_pandas()
    #     page.index = self._page_index()
    #
    #     # Show paging information
    #     page_info = (
    #         f"Showing {len(page)} of {self.original_state.num_filings:,} filings"
    #     )
    #
    #     # Generate the table string using tabulate
    #     table_str = df_to_tabulate_table(
    #         page, max_rows=len(page), title="DataDock Filings Data"
    #     )
    #
    #     return Panel(
    #         Group(table_str, Text(page_info)),
    #         title="DataDock Filings",
    #     )
    #
    def __repr__(self):
        return f"HTML Filing URL: (url='{self.html_url}')"
