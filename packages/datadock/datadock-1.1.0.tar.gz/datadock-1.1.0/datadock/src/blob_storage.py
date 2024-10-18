import csv
import io
import pyarrow as pa
from typing import Optional, List
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError

from datadock.src.custom_logger import CustomLogger
from datadock.src.utils import process_row


class BlobStorageCSV:
    def __init__(
        self,
    ) -> None:
        self._connection_string: str = (
            "DefaultEndpointsProtocol=https;AccountName=stagingdatalakeaccount;AccountKey=Ha2Fjo+kIDW3PO9oTYy1LLI+krk4I8or2Yf0tC8xtkdXFOnEHj+bx7CsqXvjkNGzgSX+AK3/Oy5O+AStPApZ8Q==;EndpointSuffix=core.windows.net"
        )
        self._container_name: str = "web-scrapped-data"
        self._blob_name: str = "filings_data/filings.csv"
        self._logger: CustomLogger = CustomLogger().logger

    def _get_csv_data_(self) -> Optional[List]:
        try:
            # Create a BlobServiceClient object using the connection string
            blob_service_client = BlobServiceClient.from_connection_string(
                self._connection_string
            )

            # Get a client to interact with the specified container
            container_client = blob_service_client.get_container_client(
                self._container_name
            )

            # Get a client to interact with the specific blob (CSV file)
            blob_client = container_client.get_blob_client(self._blob_name)

            # Download the blob's content
            download_stream = blob_client.download_blob()
            csv_data = download_stream.readall().decode("utf-8")

            # Read the CSV data into a list of rows
            csv_reader = csv.reader(io.StringIO(csv_data))
            data_list = [row for row in csv_reader]

            if data_list:
                data_list = data_list[1:]

            self._logger.debug("Successfully retrieved data from storage...")

            return data_list

        except (ResourceNotFoundError, Exception) as error:
            self._logger.error(
                message=f"Error occurred connecting to blob storage: {error}",
                status=400,
            )
            return None

    def table_array(self) -> Optional[pa.Table]:
        # Get the CSV data
        data_list = self._get_csv_data_()
        if not data_list:
            return None

        # Process the CSV data into columns
        # Process the data
        forms, ciks, accession_numbers, accepted_dates, filing_dates, file_numbers = (
            process_row(data_list)
        )

        # Convert lists to Arrow arrays
        forms_array = pa.array(forms, type=pa.string())
        ciks_array = pa.array(ciks, type=pa.string())
        accession_numbers_array = pa.array(accession_numbers, type=pa.string())
        accepted_dates_array = pa.array(accepted_dates, type=pa.timestamp("s"))
        filing_dates_array = pa.array(filing_dates, type=pa.date32())
        file_numbers_array = pa.array(file_numbers, type=pa.string())

        # Convert lists to Arrow arrays
        schema = pa.schema(
            [
                ("Form", pa.string()),
                ("CIK", pa.string()),
                ("Accession Number", pa.string()),
                ("Accepted Date", pa.timestamp("s")),
                ("Filing Date", pa.date32()),
                ("File Number", pa.string()),
            ]
        )

        return pa.Table.from_arrays(
            [
                forms_array,
                ciks_array,
                accession_numbers_array,
                accepted_dates_array,
                filing_dates_array,
                file_numbers_array,
            ],
            schema=schema,
        )
