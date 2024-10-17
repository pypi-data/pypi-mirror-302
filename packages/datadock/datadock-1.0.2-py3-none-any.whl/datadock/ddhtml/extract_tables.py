from bs4 import BeautifulSoup, Tag
from typing import Union, Dict, Optional


def get_tables(
    soup: Union[str, BeautifulSoup, Tag],
    element: Union[Tag, str] = "table",
    attributes: Optional[Dict[str, str]] = None,
):
    """Find all tables that match the specified element and attributes."""
    if isinstance(soup, str):
        soup = BeautifulSoup(soup, "html.parser")

    # Find all elements matching the specified tag and attributes
    tables = (
        soup.find_all(element, attrs=attributes)
        if attributes
        else soup.find_all(element)
    )

    # List to hold table data
    all_table_data = []

    # Loop through each table and extract data
    for table in tables:
        table_data = []
        rows = table.find_all("tr")

        # Extract column headers
        headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]

        # Extract row data
        for row in rows[1:]:
            columns = row.find_all("td")
            row_data = [col.get_text(strip=True) for col in columns]
            table_data.append(row_data)

        # Store table headers and data
        all_table_data.append({"headers": headers, "rows": table_data})

    return all_table_data
