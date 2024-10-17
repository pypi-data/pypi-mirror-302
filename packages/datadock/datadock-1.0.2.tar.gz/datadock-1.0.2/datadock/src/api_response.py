"""  This represents the response from the Edgar SEC API server after making HTTP requests. """

from dataclasses import dataclass
from typing import NamedTuple, Optional, Union, Dict, Any


# @dataclass
# class DataDockResponse(NamedTuple):
#     """
#     Edgar SEC API Response from the server after HTTP requests have been made
#     """
#
#     status_code: int
#     status: bool
#     message: str
#     data: Optional[Union[Dict[str, Any], None]]
