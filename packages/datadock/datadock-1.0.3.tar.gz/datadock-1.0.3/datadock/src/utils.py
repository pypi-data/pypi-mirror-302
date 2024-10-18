import re
from typing import Optional, List, Tuple, Dict

import pandas as pd
from bs4 import BeautifulSoup
from datadock.src.constants import SEC_BASE_URL


def check_link_format(link) -> bool:
    """
    Checks if the given link follows a specific format.

    The function uses a regular expression pattern to match links that have
    a format like 'R<digits>.htm', where <digits> represents one or more numeric
    digits. The function returns True if the link matches the format, and False otherwise.

    Parameters:
    - link (str): The link to be checked for the specified format.

    Returns:
    bool: True if the link matches the format, False otherwise.

    Example:
    >>> check_link_format('R12345.htm')
    True
    >>> check_link_format('invalid_link.htm')
    False
    """
    return bool(re.search(r"R\d+\.htm$", link))


def parse_html_content(html_content: str) -> BeautifulSoup:
    """Parse the HTML content into a BeautifulSoup object."""
    return BeautifulSoup(html_content, "html.parser")


def clean_text(text: str) -> str:
    """Clean the extracted text content."""
    cleaned_text = re.sub(
        r"<font\s*\n?style.*$|<p\s*\n?style.*$|<span\s*\n?style.*$|<span\s*\n?class.*$|<p\s*\n?class.*$|<font\s*\n?class.*$",
        "",
        text,
    )
    cleaned_text = re.sub(r"\n{2,}", "\n", cleaned_text)
    cleaned_text = re.sub(r"\xa0|\n\s*\n", "", cleaned_text)
    cleaned_text = cleaned_text.replace("\\n", "\n").strip()
    return cleaned_text


def clean(raw_content: str) -> str:
    """Clean the raw sections' content."""
    soup = parse_html_content(raw_content)
    text = soup.get_text("\n")
    return clean_text(text)


def extract_viewer_links(html_text: str):
    """Extract all viewer links containing /cgi-bin/viewer."""
    soup = parse_html_content(html_text)
    return [
        a_tag["href"]
        for a_tag in soup.find_all("a", href=True)
        if "/cgi-bin/viewer" in a_tag["href"]
    ]


def extract_xbrl_or_first_document(soup: BeautifulSoup) -> Optional[str]:
    """Extract XBRL or iXBRL reference, or return the first document link if none found."""
    doc_table = soup.find("table", {"summary": "Document Format Files"})

    if doc_table:
        for row in doc_table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) >= 3 and any(
                x in cols[2].text.lower() for x in ["xbrl", "ixbrl"]
            ):
                return cols[2].find("a")["href"]

        # Return the first document link if no XBRL found
        if len(doc_table.find_all("tr")) > 1:
            return doc_table.find_all("tr")[1].find("a")["href"]
    return None


def scrape_r_links(response: str):
    if not response:
        return []

    # Parse the HTML content using BeautifulSoup
    soup = parse_html_content(response)

    # Use a generator expression for efficiency and scalability
    return (
        f"{SEC_BASE_URL}{a_tag['href']}"
        for a_tag in soup.find_all("a", href=True)
        if check_link_format(a_tag["href"])
    )


# Helper function for checking link format
def check_cgi_link_format(link: str) -> bool:
    """Check if the link format is valid (e.g., contains '/cgi-bin/viewer')."""
    return "/cgi-bin/viewer" in link


def ticker_generator(cik: str, accession_number: str) -> Optional[str]:
    """
    Generates and returns the company ticker symbol for a company based on its CIK (Central Index Key).

    Parameters:
    - cik (str): The CIK (Central Index Key) of the company, typically obtained from financial databases.

    Returns:
    - str or None: The stock ticker symbol associated with the given CIK. Returns None if the CIK is not found.

    Company Information:
    - The function has a predefined dictionary of companies with their CIK and ticker symbol.
    - The CIK provided should be in the format 'xxxxxxxxxx-xx-xxxxxx', and leading zeros before the first non-zero
    digit are ignored.

    Example:
    >>> ticker_generator("320193", "00003456-23-345678")
    'META'

    Note:
    - This function uses the CIK to look up the corresponding ticker symbol in the predefined company dictionary.
    - If the CIK is not found or if the provided CIK is not in the expected format, the function returns None.
    """
    companies = {
        "Microsoft": {"cik": 789019, "ticker": "MSFT"},
        "Apple": {"cik": 320193, "ticker": "AAPL"},
        "CVS": {"cik": 64803, "ticker": "CVS"},
        "DELTA": {"cik": 27904, "ticker": "DAL"},
        "EXXON": {"cik": 34088, "ticker": "XOM"},
        "ALPHABET": {"cik": 1652044, "ticker": "GOOGL"},
        "The Goldman Sachs": {"cik": 886982, "ticker": "GS"},
        "Facebook": {"cik": 1326801, "ticker": "META"},
        "Meta": {"cik": 1326801, "ticker": "META"},
        "THE HOME DEPOT": {"cik": 354950, "ticker": "HD"},
        "RITE AID": {"cik": 84129, "ticker": "RAD"},
        "United Parcel Service": {"cik": 1090727, "ticker": "UPS"},
        "3M": {"cik": 66740, "ticker": "MMM"},
    }

    ticker = next(
        (company["ticker"] for company in companies.values() if company["cik"] == cik),
        "DD",
    )
    return f"{ticker}-{accession_number.lstrip('0')}" if ticker else None


def process_row(data_list: List) -> Tuple:
    # Initialize lists for each column
    forms = []
    ciks = []
    accession_numbers = []
    accepted_dates = []
    filing_dates = []
    file_numbers = []

    # Process each row
    for row in data_list:
        # Append values to the lists
        forms.append(row[0])
        ciks.append(row[1])
        accession_numbers.append(row[2])
        accepted_date_str = row[3]  # Convert and format "Accepted Date"
        # Handle datetime format
        try:
            # Convert to pandas timestamp
            accepted_date = pd.to_datetime(accepted_date_str, format="%Y-%m-%d%H:%M:%S")
            accepted_dates.append(accepted_date)
        except ValueError:
            # Handle any invalid date formats
            accepted_dates.append(None)
        # Convert to date
        filing_dates.append(pd.to_datetime(row[4], format="%m/%d/%Y").date())
        file_numbers.append(row[5])
    return forms, ciks, accession_numbers, accepted_dates, filing_dates, file_numbers
