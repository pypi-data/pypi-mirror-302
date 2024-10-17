import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from typing import List, Union, Optional, Iterator
from rich import box
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from datadock.src.custom_logger import CustomLogger
from datadock.core import DataPager
from datadock.src.constants import IntString
from datadock.src.filters import (
    filter_by_form,
    filter_by_cik,
    filter_by_date,
    filter_by_accession,
    filter_by_file_no,
)
from datadock.src._rich_ import df_to_rich_table, repr_rich
from datadock.src.dataclasses import FilingsState
from datadock.src.constants import unicode_for_form
from datadock.src.api_base import SECRequestHandler


class Filings:

    def __init__(
        self,
        filing_index: pa.Table,
        original_state: Optional[FilingsState] = None,
        logger: Optional[CustomLogger] = None,
        scrape: bool = False,
    ) -> None:
        self.data = filing_index
        self.original_state = original_state or FilingsState(0, len(filing_index))
        self.data_pager = DataPager(self.data)
        self._logger: CustomLogger = logger or CustomLogger().logger
        self.scrape = scrape

    def to_pandas(self, *columns) -> Optional[pd.DataFrame]:
        if not self.data:
            return None
        data_frame = self.data.to_pandas()
        return data_frame.filter(columns) if len(columns) > 0 else data_frame

    def filter(
        self,
        form: Optional[Union[str, List[IntString]]] = None,
        cik: Union[IntString, List[IntString]] = None,
        accession: Union[IntString, List[IntString]] = None,
        file_number: Union[IntString, List[IntString]] = None,
        date_input: Optional[str] = None,
        amendments: bool = False,
    ) -> Optional["Filings"]:
        filing_index = self.data
        forms = form

        if isinstance(forms, list):
            forms = [str(form) for form in forms]

        # Filter by form
        if forms:
            filing_index = filter_by_form(
                filing_index, form_type=forms, amendments=amendments
            )

        # filing_date and date are aliases
        if date_input:
            try:
                filing_index = filter_by_date(filing_index, date_input, "Filing Date")
            except Exception as error:
                self._logger.error(str(error))
                return None

        if cik:
            filing_index = filter_by_cik(filing_index, cik)

        if accession:
            filing_index = filter_by_accession(filing_index, accession)

        if file_number:
            filing_index = filter_by_file_no(filing_index, file_number)
        return Filings(filing_index, scrape=self.scrape)

    def save_parquet(self, location: str) -> None:
        """Save the filing index as parquet"""
        pq.write_table(self.data, location)

    def save(self, location: str) -> None:
        """Save the filing index as parquet"""
        self.save_parquet(location)

    def latest(self, n: int = 1) -> "Filings":
        """Get the latest n filings"""
        sort_indices = pc.sort_indices(
            self.data, sort_keys=[("Filing Date", "descending")]
        )
        sort_indices_top = sort_indices[: min(n, len(sort_indices))]
        latest_filing_index = pc.take(data=self.data, indices=sort_indices_top)
        filings = Filings(latest_filing_index, scrape=self.scrape)
        return filings

    def current(self) -> "Filings":
        return self

    def next(self) -> Optional["Filings"]:
        """Show the next page"""
        data_page = self.data_pager.next()
        if data_page is None:
            self._logger.warning("End of data .. use prev() \u2190 ")
            return None
        start_index, _ = self.data_pager.current_range
        filings_state = FilingsState(page_start=start_index, num_filings=len(self))
        return Filings(data_page, original_state=filings_state, scrape=self.scrape)

    def previous(self) -> Optional["Filings"]:
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
        return Filings(data_page, original_state=filings_state, scrape=self.scrape)

    def prev(self) -> "Filings":
        """Alias for self.previous()"""
        return self.previous()

    @property
    def summary_filings(self) -> str:
        return (
            f"Showing {self.data_pager.page_size} of "
            f"{self.original_state.num_filings:,} filings"
        )

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator:
        self.n = 0
        return self

    def __getitem__(self, index: int) -> "Filing":
        """Return a Filing object at the specified index."""
        if index < 0 or index >= len(self.data):
            raise IndexError("Index out of range")

        # Fetch the row from the `pyarrow.Table`
        row = self.data.to_pandas().iloc[index]

        # Create and return a `Filing` object
        return Filing(
            cik=row["CIK"],
            form=row["Form"],
            filing_date=row["Filing Date"],
            accession_no=row["Accession Number"],
            file_no=row["File Number"],
            scrape=self.scrape,
        )

    def __next__(self) -> "Filing":
        if self.n >= len(self.data):
            raise StopIteration
        filing: Filing = self[self.n]
        self.n += 1
        return filing

    def _page_index(self) -> range:
        """Create the range index to set on the page dataframe depending on where in the data we are"""
        if self.original_state:
            return range(
                self.original_state.page_start,
                self.original_state.page_start
                + min(self.data_pager.page_size, len(self.data)),
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
                    page, title="DataDock Filings Data", max_rows=len(page)
                ),
                Text(page_info),
            ),
            title="DataDock Filings",
        )

    def __repr__(self) -> str:
        return repr_rich(self.__rich__())


class Filing:
    """
    A single SEC filing. Allow you to access the documents and data for that filing
    """

    def __init__(
        self,
        cik: int,
        form: str,
        filing_date: str,
        accession_no: str,
        file_no: str,
        scrape: bool = False,
    ) -> None:
        self._cik = cik
        self._file_no = file_no
        self._form = form
        self._filing_date = filing_date
        self._accession_no = accession_no
        self._scrape = scrape

    @property
    def accession_number(self) -> str:
        return self._accession_no

    @property
    def cik(self) -> str:
        return str(self._cik)

    @property
    def form(self) -> str:
        return self._form

    def list_scrape(self):
        if self._scrape:
            req_handler = SECRequestHandler(self.cik, self.accession_number)
            return req_handler

    def __hash__(self) -> int:
        return hash(self._accession_no)

    def __eq__(self, other) -> bool:
        return isinstance(other, Filing) and self._accession_no == other._accession_no

    def __ne__(self, other) -> bool:
        return not self == other

    def __rich__(self) -> Panel:
        """
        Produce a table version of this filing e.g.
         ╭──────────────────────┬─────────┬────────────┬────────────────────┬───╮
         │ 0001493152-24-033795 │ 1893173 │ 2024-08-23 │ 001-40998241237651 │ 4 │
         ╰──────────────────────┴─────────┴────────────┴────────────────────┴───╯
        :return: a rich table version of this filing
        """
        summary_table = Table(box=box.ROUNDED, show_header=False)
        summary_table.add_column(
            "Accession#", style="bold deep_sky_blue1", header_style="bold"
        )
        summary_table.add_column("Filed")
        summary_table.add_row(
            self._accession_no,
            str(self._cik),
            str(self._filing_date),
            self._file_no,
            self._form,
        )

        return Panel(
            Group(summary_table),
            title=Text(
                f"{self._file_no} [{self._cik}] {self._form} {unicode_for_form(self._form)}",
                style="bold",
            ),
            box=box.ROUNDED,
        )

    def __repr__(self) -> str:
        return repr_rich(self.__rich__())
