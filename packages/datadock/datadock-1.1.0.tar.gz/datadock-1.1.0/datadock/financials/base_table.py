import pyarrow as pa
import pandas as pd
from bs4 import BeautifulSoup


def extract_table_data(table):
    # a generator that can be converted ta a list
    return (
        [cell.get_text(strip=True) for cell in row.find_all("td")]
        for row in table.find_all("tr")
        if row.find_all("td")
    )


# def extract_headers(table):
#     headers_list = []
#     plain_headers_list = []
#
#     for row in table.find_all("tr"):
#         header_elements = row.find_all("th")
#         if not header_elements:
#             continue  # Skip rows without header elements
#
#         # Extract the text, colspan, and rowspan in a single pass
#         header_list = {
#             "header": [header.get_text(strip=True) for header in header_elements],
#             "colspan": [
#                 header.get("colspan", "1") for header in header_elements
#             ],  # Default to '1' if not present
#             "rowspan": [
#                 header.get("rowspan", "1") for header in header_elements
#             ],  # Default to '1' if not present
#         }
#
#         # Collect the plain headers
#         plain_header_list = header_list["header"]
#
#         # Append to respective lists
#         headers_list.append(header_list)
#         plain_headers_list.append(plain_header_list)
#
#     return headers_list, plain_headers_list


def extract_headers(table):
    plain_headers_list = []

    for row in table.find_all("tr"):
        header_elements = row.find_all("th")
        if not header_elements:
            continue  # Skip rows without header elements

        # Extract the text
        plain_header_list = [header.get_text(strip=True) for header in header_elements]

        # Append to the list
        plain_headers_list.append(plain_header_list)

    # Flatten the list of headers if there are multiple rows
    if plain_headers_list:
        return plain_headers_list[0]  # Take the first row of headers
    return []


# def process_colspan_rowspan(headers_list, plain_headers_list, num_columns):
#     # Iterate over each header row in headers_list
#     for i, header_row in enumerate(headers_list):
#         for x, header in enumerate(header_row["header"]):
#             if header:
#                 # Process colspan
#                 colspan = int(
#                     header_row["colspan"][x] or 1
#                 )  # Default to 1 if None or empty
#                 if colspan > 1:
#                     plain_headers_list[i][x : x + 1] = [header] + [" "] * (
#                         colspan - 1
#                     )  # Expand the header list efficiently
#
#                 # Process rowspan
#                 rowspan = int(
#                     header_row["rowspan"][x] or 1
#                 )  # Default to 1 if None or empty
#                 if rowspan > 1:
#                     for row_offset in range(1, rowspan):
#                         target_row = i + row_offset
#                         if target_row >= len(plain_headers_list):
#                             plain_headers_list.append(
#                                 [" "] * num_columns
#                             )  # Extend with empty rows if necessary
#                         if x < len(plain_headers_list[target_row]):
#                             plain_headers_list[target_row][x] = " "
#                         else:
#                             plain_headers_list[target_row].append(" ")
#
#     # Ensure all rows have the correct number of columns
#     for header_idx, header_row in enumerate(plain_headers_list):
#         if len(header_row) < num_columns:
#             plain_headers_list[header_idx].extend(
#                 [" "] * (num_columns - len(header_row))
#             )  # Fill missing columns
#
#     return plain_headers_list


# def parse_html(html_content: str, filling_id: str):
#
#     # html_content = get_html_content(url)
#     soup = BeautifulSoup(html_content, "html.parser")
#     table_elements = soup.find_all("table")
#
#     for table in table_elements:
#         rows = list(extract_table_data(table))  # list of rows
#         print(f"Rows: {rows}")
#
#         dataframe = pd.DataFrame(rows)
#         num_columns = dataframe.shape[1]
#
#         print(f"Number of columns: {num_columns}")  # gives the number of columns
#         headers_list, plain_headers_list = extract_headers(table)
#
#         print(f"Headers: \n{headers_list}")  # table headers in a list
#         print(f"Headers List: \n{plain_headers_list}")
#
#         if headers_list:
#             plain_headers_list = process_colspan_rowspan(
#                 headers_list, plain_headers_list, num_columns
#             )
#             # attach filling identity to the header of the table
#
#             plain_headers_list[0][0] = f"{plain_headers_list[0][0]}-{filling_id}"
#             dataframe_from_header = pd.DataFrame(plain_headers_list)
#
#             # Concatenate the dataframe_from_header  with the existing DataFrame
#             combined_dataframe = pd.concat(
#                 [dataframe_from_header, dataframe], ignore_index=True
#             )
#
#             # Convert to pyarrow table for efficiency
#             arrow_table = pa.Table.from_pandas(combined_dataframe)
#
#             return arrow_table
#
#             # return plain_headers_list, combined_dataframe
#
#     return None, None


def parse_html_new(html_content: str, filing_id: str):
    soup = BeautifulSoup(html_content, "html.parser")
    table_elements = soup.find_all("table")

    for table in table_elements:
        headers = extract_headers(table)
        rows = list(extract_table_data(table))  # List of rows

        # Convert rows to pyarrow Table
        if rows:
            # Find the max number of columns to handle uneven rows
            max_columns = max(len(row) for row in rows)

            # Standardize rows to have the same number of columns
            standardized_rows = [row + [""] * (max_columns - len(row)) for row in rows]
            if len(headers) < max_columns:
                headers += [f"extra_col_{i}" for i in range(max_columns - len(headers))]
            headers = headers[:max_columns]  # Truncate if headers are too many

            # Convert to pyarrow Table
            pa_table = pa.Table.from_pydict(
                {
                    headers[i]: [row[i] for row in standardized_rows]
                    for i in range(max_columns)
                }
            )
            # print(f"PyArrow Table:\n{pa_table}")
            return pa_table, filing_id
    return None
