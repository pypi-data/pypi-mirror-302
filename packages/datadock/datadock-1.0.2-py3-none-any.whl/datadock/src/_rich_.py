from typing import Union, Optional, List, Any

import pandas as pd
import pyarrow as pa
from rich import box
from rich.table import Table
from rich.text import Text
import itertools

table_styles = {
    "Form": "yellow2",
    "FilingDate": "deep_sky_blue1",
    "Filing Date": "deep_sky_blue1",
    "File Number": "sandy_brown",
    "CIK": "dark_sea_green4",
    "Accepted Date": "dark_slate_gray1",
    "Accession Number": "light_coral",
    "HTML URLs": "yellow2",
    "Document File No": "yellow2",
    "R.htm URLs": "yellow2",
}


def df_to_rich_table(
    df: Union[pd.DataFrame, pa.Table],
    index_name: Optional[str] = None,
    title: str = "",
    title_style: str = "",
    max_rows: int = 20,
    table_box: box.Box = box.SIMPLE_HEAVY,
) -> Table:
    """
    Convert a dataframe to a rich table


    :param index_name: The name of the index
    :param df: The dataframe to convert to a rich Table
    :param max_rows: The maximum number of rows in the rich Table
    :param title: The title of the Table
    :param title_style: The title of the Table
    :param table_box: The rich box style e.g. box.SIMPLE
    :return: a rich Table
    """
    if isinstance(df, pa.Table):
        # For speed, learn to sample the head and tail of the pyarrow table
        df = df.to_pandas()

    rich_table = Table(
        box=table_box,
        row_styles=["bold", ""],
        title=title,
        title_style=title_style or "bold",
        title_justify="center",
    )
    index_name = str(index_name) if index_name else ""
    index_style = table_styles.get(index_name)
    rich_table.add_column(
        index_name, style=index_style, header_style=index_style, justify="right"
    )

    for column in df.columns:
        style_name = table_styles.get(column)
        rich_table.add_column(
            column, style=style_name, header_style=style_name, justify="right"
        )

    if len(df) > max_rows:
        head = df.head(max_rows // 2)
        tail = df.tail(max_rows // 2)
        data_for_display = pd.concat(
            [
                head,
                pd.DataFrame([{col: "..." for col in df.columns}], index=["..."]),
                tail,
            ]
        )
    else:
        data_for_display = df

    data_for_display = data_for_display.reset_index()

    for index, value_list in enumerate(data_for_display.values.tolist()):
        # row = [str(index)] if show_index else []
        row = [str(x) for x in value_list]
        rich_table.add_row(*row)

    return rich_table


def repr_rich(renderable) -> str:
    """
    This renders a rich object to a string

    It implements one of the methods of capturing output listed here

    https://rich.readthedocs.io/en/stable/console.html#capturing-output

     This is the recommended method if you are testing console output in unit tests

        from io import StringIO
        from rich.console import Console
        console = Console(file=StringIO())
        console.print("[bold red]Hello[/] World")
        str_output = console.file.getvalue()

    :param renderable:
    :return:
    """
    from rich.console import Console

    console = Console()
    with console.capture() as capture:
        console.print(renderable)
    str_output = capture.get()
    return str_output


def colorize_words(words, colors=None) -> Text:
    """Colorize a list of words with a list of colors" """
    colors = colors or ["deep_sky_blue3", "red3", "dark_sea_green4"]
    colored_words = []
    color_cycle = itertools.cycle(colors)

    for word in words:
        color = next(color_cycle)
        colored_words.append((word, color))

    return Text.assemble(*colored_words)


def display_table_with_rich(
    arrow_table: Union[pa.Table, List[Any]],
    filing_id: str = None,
    index_name: Optional[str] = None,
    title: str = "",
    title_style: str = "",
    table_box: box.Box = box.SQUARE,
) -> Table:
    # console = Console()
    rich_table = Table(
        box=table_box,
        row_styles=["bold", ""],
        title=title,
        title_style=title_style or "bold",
        title_justify="center",
        caption=filing_id,
    )
    index_name = str(index_name) if index_name else ""
    index_style = table_styles.get(index_name)
    rich_table.add_column(
        index_name, style=index_style, header_style=index_style, justify="right"
    )

    if isinstance(arrow_table, pa.Table):
        # Add headers
        for column in arrow_table.column_names:
            # table.add_column(col)
            style_name = table_styles.get(column)
            rich_table.add_column(
                column, style=style_name, header_style=style_name, justify="right"
            )

        # Add rows
        for row in arrow_table.to_pandas().itertuples(index=False):
            rich_table.add_row(*map(str, row))
        return rich_table
    elif isinstance(arrow_table, list):
        # If it's a list, we can display it directly
        for link in arrow_table:
            rich_table.add_row(link)
        return rich_table


def format_value(value: Any) -> str:
    """Format the value for display in the rich table."""
    if isinstance(value, list):
        return ", ".join(map(str, value))  # Join list items with a comma
    return str(value)


def table_with_rich(
        df: Union[pa.Table, List[Any]],
        index_name: Optional[str] = None,
        title: str = "",
        title_style: str = "",
        table_box: box.Box = box.SQUARE,
) -> Table:
    """Create a rich table from a pyarrow table."""
    rich_table = Table(
        box=table_box,
        row_styles=["bold", ""],
        title=title,
        title_style=title_style or "bold",
        title_justify="center",
    )

    if isinstance(df, pa.Table):
        # Convert pyarrow table to pandas DataFrame for easier manipulation
        df = df.to_pandas()

        # Add columns dynamically based on the DataFrame columns
        for column in df.columns:
            column_type = str(df[column].dtype)
            column_style = table_styles.get(column_type, "white")  # Default style

            # Add column to the rich table
            rich_table.add_column(column, style=column_style, justify="left")

        # Populate the table rows with formatted data
        for index in range(len(df)):
            row_data = [format_value(df[col].iloc[index]) for col in df.columns]
            rich_table.add_row(*row_data)

    # Add index column if specified
    if index_name:
        rich_table.add_column(index_name, style="white", justify="right")
        for index in range(len(df)):
            rich_table.add_row(*[""] + [format_value(df[col].iloc[index]) for col in df.columns])

    return rich_table
