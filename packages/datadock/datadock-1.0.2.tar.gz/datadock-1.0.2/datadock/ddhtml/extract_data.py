from bs4 import BeautifulSoup, Tag
from typing import Union, List, Dict, Optional


def parse_html_content(html_content: str) -> BeautifulSoup:
    """Parse the HTML content into a BeautifulSoup object."""
    return BeautifulSoup(html_content, "html.parser")


def get_filing_data_html(
    doc_html: str,
) -> Dict[
    str, Union[Dict[str, str], List[Dict[str, str]], List[Dict[str, List[List[str]]]]]
]:
    soup = parse_html_content(doc_html)
    form_data_html = extract_form_info(soup)
    tables_data_html = extract_tables_info(soup)
    filer_data_html = extract_filer_info(soup)
    return {
        "form_data": form_data_html,
        "tables_data": tables_data_html,
        "filer_data": filer_data_html,
    }


def extract_child_text(
    tag: Tag, child_tag: str, child_id: str = None, child_class: str = None
) -> str:
    if child_id:
        child = tag.find(child_tag, {"id": child_id})
    elif child_class:
        child = tag.find(child_tag, {"class": child_class})
    else:
        child = tag.find(child_tag)

    return child.text.strip() if child else ""


def extract_form_info(
    soup: Union[Tag, BeautifulSoup],
    element: Union[Tag, str] = "div",
    attributes: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    # Parse the soup if a string is provided
    if isinstance(soup, str):
        soup = BeautifulSoup(soup, "html.parser")

    # Set default attributes if none are provided
    if attributes is None:
        attributes = {"id": "formDiv"}

    # Extract Filing Data from First View
    form_data = {}

    # Find the main form div
    form_div = soup.find(element, attributes)
    if form_div:
        # Extract Form Type and Accession Number
        form_data["Form Type"] = extract_child_text(
            form_div, "div", child_id="formName"
        )
        form_data["Accession Number"] = extract_child_text(
            form_div, "div", child_id="secNum"
        )

        # Extract other form details from the formGrouping divs
        info_groups = form_div.find_all("div", class_="formGrouping")
        for group in info_groups:
            info_heads = group.find_all("div", class_="infoHead")
            infos = group.find_all("div", class_="info")

            for head, info in zip(info_heads, infos):
                form_data[head.text.strip()] = info.text.strip()

    return form_data


def extract_filer_info(
    soup: Union[str, BeautifulSoup, Tag],
    element: Union[Tag, str] = "div",
    attributes: Optional[str] = "companyInfo",
) -> List[Dict[str, str]]:
    company_data_list = []

    # Parse the soup if it's a string
    if isinstance(soup, str):
        soup = BeautifulSoup(soup, "html.parser")

    # Find all divs that match the specified class (e.g., companyInfo)
    company_info_divs = soup.find_all(element, class_=attributes)

    for company in company_info_divs:
        form_data = {}

        # Extract the company name and issuer/filer status
        company_name_elem = company.find("span", class_="companyName")
        if company_name_elem:
            company_name = company_name_elem.text.split(" (")[0].strip()
            status = filer_status(company_name_elem.text)
            form_data["Company Name"] = company_name
            form_data["Status"] = status

        # Extract CIK
        cik_elem = company.find("acronym", {"title": "Central Index Key"})
        if cik_elem:
            form_data["CIK"] = cik_elem.find_next("a").text.split(" (")[0].strip()

        # Extract IRS No., File No., and SIC
        ident_info_p = company.find("p", class_="identInfo")
        if ident_info_p:
            # IRS No.
            irs_no_elem = ident_info_p.find(
                "acronym", {"title": "Internal Revenue Service Number"}
            )
            if irs_no_elem:
                form_data["IRS No."] = irs_no_elem.find_next("strong").text.strip()

            # File No.
            file_no_elem = ident_info_p.find(
                "a", href=lambda href: href and "filenum" in href
            )
            if file_no_elem:
                form_data["File No."] = file_no_elem.find("strong").text.strip()

            # SIC (Standard Industrial Code)
            sic_elem = ident_info_p.find(
                "acronym", {"title": "Standard Industrial Code"}
            )
            if sic_elem:
                form_data["SIC"] = sic_elem.find_next("b").text.strip()

        # Append the company data to the list
        company_data_list.append(form_data)

    return company_data_list


def filer_status(text: str) -> str:
    if "Issuer" in text:
        return "Issuer"
    elif "Filer" in text:
        return "Filer"
    elif "Reporting" in text:
        return "Reporting"


def extract_tables_info(
    soup: Union[str, BeautifulSoup, Tag],
    element: Union[Tag, str] = "table",
    attributes: Optional[Dict[str, str]] = None,
) -> List[Dict[str, List[str]]]:
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


def extract_xbrl_html_url(soup: BeautifulSoup):
    """Extract XBRL or iXBRL reference, or return the first document link if none found."""
    # soup = parse_html_content(html_text)
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


def extract_xml_url(soup: BeautifulSoup):
    """Extract XBRL or iXBRL reference, or return the first document link if none found."""
    # soup = parse_html_content(html_text)
    doc_table = soup.find_all("table", class_="tableFile")
    # xml_links = []

    for table in doc_table:
        rows = table.find_all("tr")
        for row in rows[1:]:  # Skip header row
            cells = row.find_all("td")
            if len(cells) > 3:  # Ensure there are enough columns
                document_link = cells[2].find("a")
                document_type = cells[3].get_text(strip=True)

                if document_link and "xml" in document_type.lower():
                    return document_link["href"]
                    # return xml_links
    return None
