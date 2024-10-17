"""
BaseAPI serves as the base for creating client APIs to interact with the SEC Edgar API
with methods for handling HTTP requests, constructing HTTP headers, joining URLs with the API base URL,
and logging response information.
"""

import json
from abc import ABC, abstractmethod
from typing import Union, Optional, Dict, List, Any, Tuple
from urllib.parse import urljoin

from requests import Response, Session, RequestException

from datadock.src.api_errors import (
    DataDockServerError,
    InvalidRequestMethodError,
)
from datadock.config import sec_identity
from datadock.src.custom_logger import CustomLogger
from datadock.src.utils import scrape_r_links, ticker_generator
from datadock.src.constants import SEC_DATA_URL, SEC_BASE_URL


def build_url(
        cik: str = None,
        accession_number: str = None,
        name: str = "",
        extra_path: str = "",
        path_ext: str = "",
) -> str:
    if accession_number is None:
        raise ValueError("Accession number is None, cannot build url")
    cleaned_accession = accession_number.replace("-", "")
    return f"{name}/{cik}/{cleaned_accession}/{extra_path}{path_ext}"


class BaseRequest(ABC):
    """Base Client API for DataDockPy"""

    _VALID_HTTP_METHODS: set[str] = {"GET"}

    # pylint: disable=too-few-public-methods
    def __init__(
            self,
            identity: str = sec_identity,
            base_url: str = SEC_BASE_URL,
            session: Optional[Session] = None,
            logger: Optional[CustomLogger] = None,
    ) -> None:
        self._identity = identity
        self._base_url = base_url
        self._headers = self._make_http_headers()
        self._logger = logger or self._default_logger()
        self._session = session or Session()

    @classmethod
    def _default_logger(cls) -> CustomLogger:
        return CustomLogger().logger

    def _join_url(self, path: str) -> str:
        """
        Join URL with Paystack API URL
        :param path:
        :return:
        """
        if path.startswith("/"):
            path = path[1:]
        return urljoin(self._base_url, path)

    def _make_http_headers(self) -> dict:
        """
        Make Paystack HTTP Headers
        :return:
        """
        return {
            "User-Agent": self._identity,
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json",
        }

    # @abstractmethod
    def _request_url(
        self,
        method: str,
        url: str,
        data: Optional[Union[Dict[str, Any], List[Any], None]] = None,
        params: Optional[Union[Dict[str, Any], None]] = None,
        **kwargs,
    ) -> Union[str, Response]:
        """
        Handles the request to Paystack API
        :param method:
        :param url:
        :param data:
        :param params:
        :param kwargs:
        :return:
        """
        if method.upper() not in self._VALID_HTTP_METHODS:
            error_message = (
                f"Invalid HTTP method. '{method}'. Supported methods are GET"
            )
            self._logger.error(error_message)
            raise InvalidRequestMethodError(error_message)

        url = self._join_url(url)
        self._logger.debug(url)

        # Filtering params and data, then converting data to JSON
        params = (
            {key: value for key, value in params.items() if value is not None}
            if params
            else None
        )
        data = json.dumps(data) if data else None

        try:
            with self._session.request(
                method,
                url=url,
                headers=self._headers,
                timeout=10,
                params=params,
                data=data,
                **kwargs,
            ) as response:
                response_data = response.text
                self._logger.info("Response Status Code: %s", response.status_code)
                if 400 <= response.status_code <= 500:
                    error_message = f"Client error occurred: {response.status_code}"
                    self._logger.error(error_message)
                    raise DataDockServerError(
                        message=error_message, status_code=response.status_code
                    )
                # Handle server error
                elif 500 <= response.status_code <= 600:
                    error_message = f"Server error occurred: {response.status_code}"
                    self._logger.error(error_message)
                    raise DataDockServerError(
                        message=error_message, status_code=response.status_code
                    )

                return response_data
        except (RequestException, Exception) as error:
            # Extract status code if available from the exception
            self._logger.error("Unable to make a request Error %s", error)
            raise

    @abstractmethod
    def fetch_document(self) -> Optional[str]:
        """Fetch the SEC document using the GET method."""
        pass


class SECRequestHandler(BaseRequest):
    def __init__(
        self,
        cik: str = None,
        accession_number: str = None,
        base_url: str = SEC_DATA_URL,
        session: Optional[Session] = None,
        logger: Optional[CustomLogger] = None,
        scrape_result: Tuple[List[str], str] = None,
    ):
        super().__init__(
            base_url=base_url,
            identity=sec_identity,
            session=session,
            logger=logger,
        )
        self._cik = cik
        self._accession_number = accession_number
        self._html_r_url = build_url(
            cik=self._cik, accession_number=self._accession_number, name="data"
        )
        self._scrape_result = scrape_result or None

    @property
    def get_html_url(self) -> str:
        return build_url(
            self._cik,
            self._accession_number,
            name="data",
            extra_path=self._accession_number,
            path_ext="-index.html",
        )

    def fetch_document(self, scrape: bool = False) -> Optional[str]:
        """Fetch the SEC document using the GET method."""
        if scrape is True:
            return self._request_url("GET", self._html_r_url)
        html_url = self.get_html_url
        return self._request_url("GET", html_url)

    def open(self) -> None:
        import webbrowser

        html_url = self.get_html_url
        webbrowser.open(self._join_url(html_url))

    def _ensure_scrape_result(self) -> None:
        """Helper method to ensure scraping is done only once."""
        if self._scrape_result is None:
            self.get_link_formats(to_scrape=True)

    def get_link_formats(self, to_scrape: bool = False) -> Tuple[Tuple[List[str], str], str, str]:
        if self._scrape_result is None:
            response = self.fetch_document(scrape=to_scrape)
            self._scrape_result = list(scrape_r_links(response)), ticker_generator(
                self._cik, self._accession_number
            )

        # scrape_url_list, filing_id =
        return self._scrape_result, self._cik, self._accession_number
