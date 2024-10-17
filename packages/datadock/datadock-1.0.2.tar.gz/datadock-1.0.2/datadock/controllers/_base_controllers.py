from abc import ABC, abstractmethod
from typing import Optional, List, Union
import pyarrow as pa
import pandas as pd
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from datadock.src import DocumentProcessor

from datadock.src.custom_logger import CustomLogger
from datadock.core import DataPager
from datadock.src._rich_ import repr_rich
from datadock.src.constants import IntString
from datadock.src.filters import filter_by_section_titles
from datadock.src.dataclasses import FilingsState


class FormBaseController(ABC):
    def __init__(
        self,
        cik: str,
        accession_number: str,
        form_type: str,
        logger: CustomLogger,
        document_processor: DocumentProcessor,
    ):
        self.cik = cik
        self.accession_number = accession_number
        self.form_type = form_type
        self._logger = logger
        self._document_processor = document_processor
        self.data_table: Optional[pa.Table] = self._process()
        self.data: FormDataSections = FormDataSections(self.data_table)

    @abstractmethod
    def _process(self) -> Optional[pa.Table]:
        pass

    def to_pandas(self, *columns) -> Optional[pd.DataFrame]:
        if not self.data:
            return None
        data_frame = self.data.data.to_pandas()
        return data_frame.filter(columns) if len(columns) > 0 else data_frame

    """
    Next step is to implement using rich or tabulate to display the pyarrow table result to users
    """

    def filter(
        self,
        titles: Optional[Union[str, List[IntString]]] = None,
    ) -> Optional["FormDataSections"]:
        filing_index = self.data.data
        section_titles = titles

        if isinstance(section_titles, list):
            section_titles = [str(title) for title in section_titles]

        # Filter by form
        if section_titles:
            filing_index = filter_by_section_titles(filing_index, titles=section_titles)
        return FormDataSections(filing_index)

    @property
    def get_all_sections(self):
        return self.data


class FormDataSections:

    def __init__(
        self,
        filing_index: pa.Table,
        original_state: Optional[FilingsState] = None,
        logger: Optional[CustomLogger] = None,
    ) -> None:
        self.data = filing_index
        self.original_state = original_state or FilingsState(0, len(filing_index))
        self.data_pager = DataPager(self.data)
        self._logger: CustomLogger = logger or CustomLogger().logger

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
        # Convert the PyArrow table to a pandas DataFrame for easier processing
        df = self.data.to_pandas()

        # Create a list to hold all sections
        sections_content = []

        # Add each section ID and its content to the list
        for section_id, section_text in zip(df["Section Title"], df["Section Content"]):
            section_id_text = Text(section_id, style="bold blue")
            section_content_text = Text(section_text)

            # Create a sub-panel for each section
            section_sub_panel = Panel(section_content_text, title=section_id_text)
            sections_content.append(section_sub_panel)

        # Create a main panel that contains all sections
        sections_panel = Panel(
            Group(*sections_content),
            title="DataDock Filings Sections and Contents",
            border_style="green",
        )

        return sections_panel

    def __repr__(self):
        return repr_rich(self.__rich__())
