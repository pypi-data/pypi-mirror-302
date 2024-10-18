from dataclasses import dataclass


@dataclass
class FilingsState:
    page_start: int
    num_filings: int


@dataclass
class FilingInfo:
    cik: str
    accession_number: str


@dataclass
class FilingDocInfo:
    filing: FilingInfo
    form_type: str
    file_number: str
    IRS: str
    SIC: str
