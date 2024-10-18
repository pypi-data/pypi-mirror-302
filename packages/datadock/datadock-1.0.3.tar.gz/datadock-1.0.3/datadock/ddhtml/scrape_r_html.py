from bs4 import BeautifulSoup
import pyarrow as pa
from requests import Session

from datadock.config import sec_identity
from datadock.src.api_base import BaseRequest
from datadock.src.constants import SEC_DATA_URL

from datadock.src.custom_logger import CustomLogger
from typing import List, Optional, Tuple, Dict, Union
from rich.console import Group
from rich.panel import Panel
from rich.text import Text
from datadock.src._rich_ import (
    repr_rich,
    display_table_with_rich,
    table_with_rich,
)


class ScrapeResult:
    def __init__(
        self,
        scrape_result: Tuple[List[str], str],
        cik: str = None,
        accession: str = None,
    ) -> None:
        self.scrape_result = scrape_result
        self.cik = cik
        self.accession = accession
        self._document_handler: Optional["ScrapeDocumentHandler"] = None

    @property
    def get_filtered_links(self) -> "ScrapeDocumentHandler":
        return ScrapeDocumentHandler(
            urls=self._filtered_links(), cik=self.cik, accession=self.accession
        )

    def __len__(self) -> int:
        """Return the length of the SEC document."""
        # self._ensure_scrape_result()
        return len(self._filtered_links())

    def __getitem__(self, index: int) -> Optional[str]:
        """Return the document at the specified index."""
        return self._filtered_links()[index]

    def __call__(self):
        """Return the document at the first index."""
        return self._filtered_links(), self.scrape_result[1]

    def _filtered_links(self) -> List[str]:
        """Filter the R.htm links to include only R1 to R6."""
        return [
            link
            for link in self.scrape_result[0]
            if any(f"R{i}.htm" in link for i in range(1, 7))
        ]

    def __rich__(self) -> Panel:
        # self._ensure_scrape_result()
        html_links, filing_id = self._filtered_links(), self.scrape_result[1]

        # Show paging information
        page_info = f"Showing Total of {len(html_links)} scraped R.htm filings"

        return Panel(
            Group(
                display_table_with_rich(
                    html_links,
                    filing_id,
                    index_name="R.htm URLs",
                    title="DataDock Scraped R.htm URLs",
                ),
                Text(page_info),
            ),
        )

    def __repr__(self):
        return repr_rich(self.__rich__())


class ScrapeDocumentHandler(BaseRequest):

    def __init__(
        self,
        urls: Union[List[str], Dict[str, pa.Table]],
        cik: str = None,
        accession: str = None,
        base_url: str = SEC_DATA_URL,
        session: Optional[Session] = None,
        logger: Optional[CustomLogger] = None,
    ):
        super().__init__(
            base_url=base_url, identity=sec_identity, session=session, logger=logger
        )

        self.cik = cik
        self.accession = accession
        self.urls = urls
        self.data_tables: Dict[str, pa.Table] = {}

    def fetch_document(self, url: str = None) -> Optional[str]:
        """Fetch the SEC document using the GET method."""
        path_url = url.split("/edgar")[1]
        return self._request_url("GET", path_url)

    def scrape_tables_from_url(self, url: str) -> Optional[pa.Table]:
        """Scrape the document from the URL and extract all data from <table> tags."""
        html_content = self.fetch_document(url)
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all table elements
        tables = soup.find_all("table")

        # If no tables are found, return None
        if not tables:
            return None

        all_data = []

        for table in tables:
            headers = []
            rows_data = []

            # Extract headers (check for <th> elements first, otherwise fallback to the first row)
            header_row = table.find("tr")
            if header_row:
                th_elements = header_row.find_all("th")
                if th_elements:
                    headers = [th.get_text(strip=True) for th in th_elements]
                else:
                    headers = [
                        td.get_text(strip=True) for td in header_row.find_all("td")
                    ]

            # Extract rows (skip the first row if it was used for headers)
            rows = table.find_all("tr")[1:] if headers else table.find_all("tr")

            for row in rows:
                columns = row.find_all("td")
                if columns:
                    rows_data.append([col.get_text(strip=True) for col in columns])

            # If headers and rows exist, add them to the final data
            if headers and rows_data:
                all_data.append((headers, rows_data))

        # If no valid data was found, return None
        if not all_data:
            return None

        # Assuming we are processing the first valid table, or you can loop through each one
        headers, rows_data = all_data[0]

        # Transform the data into a pyarrow.Table
        return pa.Table.from_pydict(
            {headers[i]: [row[i] for row in rows_data] for i in range(len(headers))}
        )

    def cover_page(self) -> Union["TableDisplay", pa.Table]:
        """Scrape data from the first URL (cover page)."""
        # self.data_tables["cover_page"] = self.scrape_tables_from_url(self.urls[0])
        data_tables = self.scrape_tables_from_url(self.urls[0])
        return TableDisplay("cover_page", data_tables)

    def balance_sheet(self) -> Union["TableDisplay", pa.Table]:
        """Scrape data from the second URL (balance sheet)."""
        data_tables = self.scrape_tables_from_url(self.urls[1])
        return TableDisplay("balance_sheet", data_tables)

    def income(self) -> Union["TableDisplay", pa.Table]:
        """Scrape data from the third URL (income statement)."""
        data_tables = self.scrape_tables_from_url(self.urls[2])
        return TableDisplay("income", data_tables)

    def loss(self) -> Union["TableDisplay", pa.Table]:
        """Scrape data from the fourth URL (loss statement)."""
        data_tables = self.scrape_tables_from_url(self.urls[3])
        return TableDisplay("loss", data_tables)

    def net_income(self) -> Union["TableDisplay", pa.Table]:
        """Scrape data from the fifth URL (net income statement)."""
        data_tables = self.scrape_tables_from_url(self.urls[4])
        return TableDisplay("net_income", data_tables)

    def consolidation(self) -> Union["TableDisplay", pa.Table]:
        """Scrape data from the sixth URL (consolidation statement)."""
        data_tables = self.scrape_tables_from_url(self.urls[5])
        return TableDisplay("consolidation", data_tables)


class TableDisplay:
    def __init__(self, name: str, dict_table: pa.Table):
        self._name = name
        self._dict_table = dict_table

    def __rich__(self):
        return Panel(
            Group(
                table_with_rich(self._dict_table, title=self._name),
                Text("Showing Financial Statement"),
            ),
            title="DataDock Filings",
        )

    def __repr__(self):
        return repr_rich(self.__rich__())
