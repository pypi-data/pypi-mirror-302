from typing import Optional, Dict, List, Union

from rich import box
from rich.table import Table
from pydantic import BaseModel

from datadock.src import SECRequestHandler
from datadock.ddhtml.extract_data import get_filing_data_html
from datadock.src._rich_ import repr_rich
from datadock.ddhtml.scrape_r_html import ScrapeResult


class CompanyDataDisplay(BaseModel):
    form_data: Dict[str, str]
    filer_info: List[Dict[str, str]]
    tables: List[Dict[str, Union[List[str], List[List[str]]]]]

    def __rich__(self):
        box_table = Table(
            title="SEC DataDock Filing",
            title_justify="center",
            box=box.SQUARE,
            show_header=False,
        )

        items = list(self.form_data.items())
        table_items = self.tables
        filer_items = self.filer_info

        first_two_items = items[:2]
        remaining_items = items[2:]

        form_info_table = Table(
            title="Filing Information",
            box=box.HORIZONTALS,
            show_header=False,
        )

        # Add the first two items to the first row
        form_info_table.add_row(f"[bold]{first_two_items[0][1]}[/bold]")
        form_info_table.add_row(f"[bold]{first_two_items[1][1]}[/bold]")
        # # Add remaining items in a new row
        remaining_data = [
            f"[bold]{key}[/bold]: {value}" for key, value in remaining_items
        ]
        form_info_table.add_row(*remaining_data)

        # Add a row for CIK and Accession Number
        box_table.add_row(form_info_table)

        for index, table_data in enumerate(table_items):
            headers = table_data.get("headers")
            rows = table_data.get("rows")

            table_info = Table(
                title=f"Table {index + 1}: Filing Documents",
                box=box.DOUBLE_EDGE,
            )

            for header in headers:
                table_info.add_column(header, justify="left")
            for row in rows:
                table_info.add_row(*row)

            box_table.add_row(table_info)

        for index, company_info in enumerate(filer_items):
            # Create a new table for each dictionary
            box_style = (
                box.SQUARE if index % 2 == 0 else box.ROUNDED
            )  # Alternate box styles
            filer_table = Table(
                title=f"Filer Information {index + 1}",
                title_justify="center",
                box=box_style,
                show_header=False,
            )

            # Add rows for the current company's information
            for key, value in company_info.items():
                filer_table.add_row(f"[bold]{key}[/bold]", str(value))

            box_table.add_row(filer_table)

        return box_table

    def __repr__(self):
        return repr_rich(self.__rich__())


class CompanyFilingInfo:
    def __init__(self, cik: str, accession_number: str) -> None:
        self.cik = cik
        self.accession_number = accession_number
        self._req_handler: SECRequestHandler = SECRequestHandler(
            self.cik, self.accession_number
        )
        self.doc_html = self._req_handler.fetch_document()
        self.filing_info = None

    def _get_filing_info(self):
        if self.filing_info is None:
            self._extract_filing_info()

    def _extract_filing_info(self) -> Optional[Dict[str, str]]:
        """Fetch and extract filing information"""
        if self.filing_info is None:
            # doc_html = self._req_handler.fetch_document()
            self.filing_info = get_filing_data_html(self.doc_html)
        return self.filing_info

    def company_info(self):
        self._get_filing_info()
        return CompanyDataDisplay(
            form_data=self.filing_info["form_data"],
            filer_info=self.filing_info["filer_data"],
            tables=self.filing_info["tables_data"],
        )

    def __call__(self, *args, **kwargs):
        return self._extract_filing_info()

    def open(self):
        self._req_handler.open()

    def get_r_doc(self):
        result, cik, accession = self._req_handler.get_link_formats(to_scrape=True)
        return ScrapeResult(scrape_result=result)
