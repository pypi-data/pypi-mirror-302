import pyarrow as pa
import pandas as pd
from typing import Union, Tuple, Optional, Dict

default_page_size = 50


class DataPager:
    def __init__(
        self, data: Union[pa.Table, pd.DataFrame], page_size=default_page_size
    ):
        self.data: Union[pa.Table, pd.DataFrame] = data
        self.page_size = page_size
        self.total_pages = (len(self.data) // page_size) + 1
        self.current_page = 1

    def next(self):
        """Get the next page of data"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            return self.current()
        else:
            return None

    def previous(self):
        """Get the previous page of data"""
        if self.current_page > 1:
            self.current_page -= 1
            return self.current()
        else:
            return None

    @property
    def current_range(self) -> Tuple[int, int]:
        """Get the current start and end index for the data"""
        start_index = (self.current_page - 1) * self.page_size
        end_index = min(len(self.data), start_index + self.page_size)
        return start_index, end_index

    def current(self) -> pa.Table:
        """
        Get the current data page as a pyarrow Table
        :return:
        """
        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size
        if isinstance(self.data, pa.Table):
            return self.data.slice(offset=start_index, length=self.page_size)
        else:
            return self.data.iloc[start_index:end_index]

    @property
    def start_index(self):
        return (self.current_page - 1) * self.page_size

    @property
    def end_index(self):
        return self.start_index + self.page_size


def table_array(section_dict: Dict[str, str]) -> Optional[pa.Table]:

    if not section_dict:
        return None

    # Extract the keys (section titles) and values (section contents) from the dictionary
    section_ids = list(section_dict.keys())
    section_content = list(section_dict.values())

    # Convert lists to Arrow arrays
    section_id_array = pa.array(section_ids, type=pa.string())
    section_content_array = pa.array(section_content, type=pa.string())

    # Convert lists to Arrow arrays
    schema = pa.schema(
        [
            ("Section Title", pa.string()),
            ("Section Content", pa.string()),
        ]
    )

    return pa.Table.from_arrays(
        [
            section_id_array,
            section_content_array,
        ],
        schema=schema,
    )
