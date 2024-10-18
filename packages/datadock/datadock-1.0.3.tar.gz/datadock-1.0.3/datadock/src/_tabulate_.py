import itertools
from typing import Union, Optional
import pandas as pd
import pyarrow as pa
from tabulate import tabulate
from colorama import Fore, Style, init


# Initialize colorama
init(autoreset=True)

# Define styles using colorama
table_styles = {
    "Form": Fore.YELLOW,
    "FilingDate": Fore.CYAN,
    "Filing Date": Fore.CYAN,
    "File Number": Fore.MAGENTA,
    "CIK": Fore.GREEN,
    "Accepted Date": Fore.BLUE,
    "Accession Number": Fore.RED,
}


def colorize_row(row, column_styles):
    """
    Apply color to each cell in a row based on the column's style.

    Parameters:
        row (pd.Series): A row from the DataFrame.
        column_styles (dict): A dictionary mapping column names to their color styles.

    Returns:
        list: A list of colorized strings representing the row's cells.
    """
    return [
        f"{column_styles.get(column, '')}{value}{Style.RESET_ALL}"
        for column, value in row.items()
    ]


def df_to_tabulate_table(
    df: Union[pd.DataFrame, pa.Table],
    index_name: Optional[str] = None,
    title: Optional[str] = None,
    max_rows: int = 20,
    table_format: str = "simple",
) -> str:
    """
    Convert a Pandas DataFrame or PyArrow Table into a tabulate-formatted table string.

    Parameters:
        df (Union[pd.DataFrame, pa.Table]): The DataFrame or PyArrow Table to convert.
        index_name (Optional[str]): Name to use for the index column header.
        title (Optional[str]): An optional title for the table.
        max_rows (int): Maximum number of rows to display. Default is 20.
        table_format (str): The format of the table (e.g., 'plain', 'simple', 'grid').

    Returns:
        str: A string representation of the table formatted by tabulate.
    """
    # Convert PyArrow Table to Pandas DataFrame if needed
    if isinstance(df, pa.Table):
        df = df.to_pandas()

    # Determine if we need to truncate the DataFrame
    if len(df) > max_rows:
        head = df.head(max_rows // 2)
        tail = df.tail(max_rows // 2)
        df_for_display = pd.concat(
            [
                head,
                pd.DataFrame([{col: "..." for col in df.columns}], index=["..."]),
                tail,
            ]
        )
    else:
        df_for_display = df

    # Reset the index and optionally name the index column
    df_for_display = df_for_display.reset_index()
    if index_name:
        df_for_display = df_for_display.rename(columns={"index": index_name})

    # Apply color to headers
    headers = []
    for column in df_for_display.columns:
        color = table_styles.get(column, "")
        headers.append(f"{color}{column}{Style.RESET_ALL}")

    # # Apply color to each cell in the DataFrame
    # colored_rows = df_for_display.apply(
    #     colorize_row, axis=1, column_styles=table_styles
    # ).tolist()

    # Convert the DataFrame to a tabulate table
    table_string = tabulate(
        df_for_display, headers=headers, tablefmt=table_format, showindex=False
    )

    # Add the title if provided
    if title:
        table_string = f"{title}\n\n{table_string}"

    return table_string
