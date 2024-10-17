import re
from typing import Dict, Optional

from datadock.src.custom_logger import CustomLogger


class DocumentProcessor:
    def __init__(
        self,
        raw_text: str,
        accession_number: str,
        logger: Optional[CustomLogger] = None,
    ) -> None:
        self._raw_text = raw_text
        self._accession_number = accession_number
        self._logger = logger or CustomLogger().logger
        self._unique_id = self._generate_unique_id()

    def _generate_unique_id(self) -> str:
        # Generate a unique ID based on the raw text and accession number
        date_pattern = re.search(r"FILED\s*AS\s*OF\s*DATE:(.*?)\n", self._raw_text)

        if date_pattern:
            filed_date = re.sub(r"\s*", "", date_pattern.group(1))
            return f"{self._accession_number[:10]}-{filed_date}-{self._accession_number[14:]}"
        else:
            self._logger.error(
                f"Unable to retrieve the `filed date` for : {self._accession_number}"
            )

    def extract_sections(self, form_type: str) -> Optional[Dict[str, str]]:
        # Regex to find <DOCUMENT> tags
        doc_start_pattern = re.compile(r"<DOCUMENT>")
        doc_end_pattern = re.compile(r"</DOCUMENT>")
        type_pattern = re.compile(r"<TYPE>[^\n]+")

        doc_start_is = [x.end() for x in doc_start_pattern.finditer(self._raw_text)]
        doc_end_is = [x.start() for x in doc_end_pattern.finditer(self._raw_text)]
        doc_types = [x[len("<TYPE>") :] for x in type_pattern.findall(self._raw_text)]

        document = {}
        # Create a loop to go through each section type and save only the 10-K section in the dictionary
        for doc_type, doc_start, doc_end in zip(doc_types, doc_start_is, doc_end_is):
            if doc_type == form_type:
                document[doc_type] = self._raw_text[doc_start:doc_end]

        if form_type not in document:
            self._logger.warning(
                f"No {form_type} section not found in the document for {self._accession_number}"
            )
        return document

    @property
    def unique_id(self):
        return self._unique_id
