from typing import Optional, Union

from requests import Session

from datadock.config import sec_identity
from datadock.src import DocumentProcessor
from datadock.controllers._base_controllers import FormBaseController
from datadock.controllers._controller_8k import Clean8KController
from datadock.controllers._controller_10k import Clean10KController
from datadock.src.custom_logger import CustomLogger
from datadock.src.constants import IntString, SEC_DATA_URL
from datadock.controllers._factory import (
    FormControllerFactory,
    ConcreteFormControllerFactory,
)
from datadock.src.api_base import BaseRequest, build_url


class FormControl(BaseRequest):
    def __init__(
        self,
        cik: Optional[Union[str, IntString]],
        accession: Optional[Union[str, IntString]],
        form_type: Optional[str],
        base_url: str = SEC_DATA_URL,
        session: Optional[Session] = None,
        logger: Optional[CustomLogger] = None,
        amendments: bool = False,
        scrape: bool = False,
    ):
        super().__init__(
            base_url=base_url, identity=sec_identity, session=session, logger=logger
        )
        self._cik = cik
        self._accession_number = accession
        self._form_type = form_type
        self._amendments = amendments
        self._scrape = scrape
        self.url = build_url(
            cik=self._cik,
            accession_number=self._accession_number,
            name="data",
            extra_path=self._accession_number,
            path_ext=".txt",
        )
        self._document_processor = self._get_document_processor()
        self._factory: FormControllerFactory = ConcreteFormControllerFactory()

    def fetch_document(self) -> Optional[str]:
        """Fetch the SEC document using the GET method."""
        return self._request_url("GET", self.url)

    def _get_document_processor(self) -> DocumentProcessor:
        raw_text = self.fetch_document()
        return DocumentProcessor(raw_text, self._accession_number)

    def get_controller(self) -> FormBaseController:
        if self._form_type == "8-K" or self._amendments:
            return Clean8KController(
                cik=self._cik,
                accession_number=self._accession_number,
                form_type=self._form_type,
                logger=self._logger,
                document_processor=self._document_processor,
            )
        elif self._form_type == "10-K" or self._amendments:
            return Clean10KController(
                cik=self._cik,
                accession_number=self._accession_number,
                form_type=self._form_type,
                logger=self._logger,
                document_processor=self._document_processor,
            )
        else:
            self._logger.error(f"Unsupported form type: {self._form_type}")
            raise ValueError(f"Unsupported form type: {self._form_type}")
