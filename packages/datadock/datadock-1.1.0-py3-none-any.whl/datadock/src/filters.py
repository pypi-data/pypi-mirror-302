import re
from datetime import datetime, date
import pyarrow as pa
import pyarrow.compute as pc
from fastcore.basics import listify
from typing import Union, List, Optional, Tuple

from datadock.src.constants import IntString, DATE_RANGE_PATTERN
from datadock.src.custom_logger import CustomLogger


def filter_by_form(
    data: pa.Table, form_type: Union[str, List[str]], amendments: bool = False
) -> pa.Table:
    forms = [str(item) for item in listify(form_type)]
    if amendments:
        forms = list(
            set(forms + [f"{val}/A" for val in forms])
        )  # Add amendment indicator to forms
    data = data.filter(pc.is_in(data["Form"], pa.array(forms)))
    return data


def filter_by_cik(data: pa.Table, cik: Union[IntString, List[IntString]]) -> pa.Table:
    """Return the data filtered by form"""
    # Ensure that forms is a list of strings ... it can accept int like form 3, 4, 5
    ciks = [str(el) for el in listify(cik)]
    data = data.filter(pc.is_in(data["CIK"], pa.array(ciks)))
    return data


def filter_by_accession(
    data: pa.Table, accession_number: Union[IntString, List[IntString]]
) -> pa.Table:
    """Return the data filtered by form"""
    # Ensure that forms is a list of strings ... it can accept int like form 3, 4, 5
    accession = [str(el) for el in listify(accession_number)]
    data = data.filter(pc.is_in(data["Accession Number"], pa.array(accession)))
    return data


def filter_by_file_no(
    data: pa.Table, file_no: Union[IntString, List[IntString]]
) -> pa.Table:
    """Return the data filtered by form"""
    # Ensure that forms is a list of strings ... it can accept int like form 3, 4, 5
    file_number = [str(el) for el in listify(file_no)]
    data = data.filter(pc.is_in(data["File Number"], pa.array(file_number)))
    return data


def extract_dates(input_date: str) -> Tuple[Optional[str], Optional[str], bool]:
    """
    Split a date or a date range into start_date and end_date
        split_date("2022-03-04")
          2022-03-04, None, False
       split_date("2022-03-04:2022-04-05")
        2022-03-04, 2022-04-05, True
       split_date("2022-03-04:")
        2022-03-04, None, True
       split_date(":2022-03-04")
        None, 2022-03-04, True
    :param input_date: The date to split
    :return:
    """
    log = CustomLogger().logger
    match = re.match(DATE_RANGE_PATTERN, input_date)
    if match:
        start_date, _, end_date = match.groups()
        try:
            start_date_tm = (
                datetime.strptime(start_date, "%Y-%m-%d") if start_date else None
            )
            end_date_tm = datetime.strptime(end_date, "%Y-%m-%d") if end_date else None
            if start_date_tm or end_date_tm:
                return start_date_tm, end_date_tm, ":" in input_date
        except ValueError:
            log.error(
                f"The date {input_date} cannot be extracted using date pattern YYYY-MM-DD"
            )
    raise Exception(
        f"""
    Cannot extract a date or date range from string {input_date}
    Provide either 
        1. A date in the format "YYYY-MM-DD" e.g. "2022-10-27"
        2. A date range in the format "YYYY-MM-DD:YYYY-MM-DD" e.g. "2022-10-01:2022-10-27"
        3. A partial date range "YYYY-MM-DD:" to specify dates after the value e.g.  "2022-10-01:"
        4. A partial date range ":YYYY-MM-DD" to specify dates before the value  e.g. ":2022-10-27"
    """
    )


def filter_by_date(
    data: pa.Table, date_input: Union[str, datetime], date_col: str
) -> pa.Table:
    # If datetime convert to string
    if isinstance(date_input, date) or isinstance(date_input, datetime):
        date_input = date_input.strftime("%Y-%m-%d")

    # Extract the date parts ... this should raise an exception if we cannot
    date_parts = extract_dates(date_input)
    start_date, end_date, is_range = date_parts
    if is_range:
        filtered_data = data
        if start_date:
            filtered_data = filtered_data.filter(
                pc.field(date_col) >= pc.scalar(start_date)
            )
        if end_date:
            filtered_data = filtered_data.filter(
                pc.field(date_col) <= pc.scalar(end_date)
            )
    else:
        # filter by filings on date
        filtered_data = data.filter(pc.field(date_col) == pc.scalar(start_date))
    return filtered_data


def filter_by_section_titles(
    data: pa.Table, titles: Union[IntString, List[IntString]]
) -> pa.Table:
    """Return the data filtered by form"""
    # Ensure that forms is a list of strings ... it can accept int like form 3, 4, 5
    title = [str(el) for el in listify(titles)]
    data = data.filter(pc.is_in(data["Section Title"], pa.array(title)))
    return data
