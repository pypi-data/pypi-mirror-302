import re
import pyarrow as pa
from typing import Optional

from bs4 import BeautifulSoup

from datadock.src.utils import clean, ticker_generator
from datadock.controllers._base_controllers import FormBaseController
from datadock.core import table_array


class Clean8KController(FormBaseController):
    _SECTION_NAMES = [
        (
            r"(>Item\s*(1.01)(&#160;|&nbsp;)*)|(>ITEM\s*(1.01))|(>Item\s*(1.01)(&#160;|&nbsp;)*)|(Item\s*(1.01))",
            "Entry into a Material Definitive Agreement",
        ),
        (
            r"(>Item\s*(1.02)(&#160;|&nbsp;)*)|(>ITEM\s*(1.02))|(>Item\s*(1.02)(&#160;|&nbsp;)*)|(Item\s*(1.02))",
            "Termination of a Material Definitive Agreement",
        ),
        (
            r"(>Item\s*(1.03)(&#160;|&nbsp;)*)|(>ITEM\s*(1.03))|(>Item\s*(1.03)(&#160;|&nbsp;)*)|(Item\s*(1.03))",
            "Bankruptcy or Receivership",
        ),
        (
            r"(>Item\s*(1.04)(&#160;|&nbsp;)*)|(>ITEM\s*(1.04))|(>Item\s*(1.04)(&#160;|&nbsp;)*)|(Item\s*(1.04))",
            "Mine Safety – Reporting of Shutdowns and Patterns of Violations",
        ),
        (
            r"(>Item\s*(1.05)(&#160;|&nbsp;)*)|(>ITEM\s*(1.05))|(>Item\s*(1.05)(&#160;|&nbsp;)*)|(Item\s*(1.05))",
            "Material Cybersecurity Incidents",
        ),
        (
            r"(>Item\s*(2.01)(&#160;|&nbsp;)*)|(>ITEM\s*(2.01))|(>Item\s*(2.01)(&#160;|&nbsp;)*)|(Item\s*(2.01))",
            "Completion of Acquisition or Disposition of Assets",
        ),
        (
            r"(>Item\s*(2.02)(&#160;|&nbsp;)*)|(>ITEM\s*(2.02))|(>Item\s*(2.02)(&#160;|&nbsp;)*)|(Item\s*(2.02))",
            "Results of Operations and Financial Condition",
        ),
        (
            r"(>Item\s*(2.03)(&#160;|&nbsp;)*)|(>ITEM\s*(2.03))|(>Item\s*(2.03)(&#160;|&nbsp;)*)|(Item\s*(2.03))",
            "Creation of a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement of a Registrant",
        ),
        (
            r"(>Item\s*(2.04)(&#160;|&nbsp;)*)|(>ITEM\s*(2.04))|(>Item\s*(2.04)(&#160;|&nbsp;)*)|(Item\s*(2.04))",
            "Triggering Events That Accelerate or Increase a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement",
        ),
        (
            r"(>Item\s*(2.05)(&#160;|&nbsp;)*)|(>ITEM\s*(2.05))|(>Item\s*(2.05)(&#160;|&nbsp;)*)|(Item\s*(2.05))",
            "Costs Associated with Exit or Disposal Activities",
        ),
        (
            r"(>Item\s*(2.06)(&#160;|&nbsp;)*)|(>ITEM\s*(2.06))|(>Item\s*(2.06)(&#160;|&nbsp;)*)|(Item\s*(2.06))",
            "Material Impairments",
        ),
        (
            r"(>Item\s*(3.01)(&#160;|&nbsp;)*)|(>ITEM\s*(3.01))|(>Item\s*(3.01)(&#160;|&nbsp;)*)|(Item\s*(3.01))",
            "Notice of Delisting or Failure to Satisfy a Continued Listing Rule or Standard; Transfer of Listing",
        ),
        (
            r"(>Item\s*(3.02)(&#160;|&nbsp;)*)|(>ITEM\s*(3.02))|(>Item\s*(3.02)(&#160;|&nbsp;)*)|(Item\s*(3.02))",
            "Unregistered Sales of Equity Securities",
        ),
        (
            r"(>Item\s*(3.03)(&#160;|&nbsp;)*)|(>ITEM\s*(3.03))|(>Item\s*(3.03)(&#160;|&nbsp;)*)|(Item\s*(3.03))",
            "Material Modification to Rights of Security Holders",
        ),
        (
            r"(>Item\s*(4.01)(&#160;|&nbsp;)*)|(>ITEM\s*(4.01))|(>Item\s*(4.01)(&#160;|&nbsp;)*)|(Item\s*(4.01))",
            "Changes in Registrant’s Certifying Accountant",
        ),
        (
            r"(>Item\s*(4.02)(&#160;|&nbsp;)*)|(>ITEM\s*(4.02))|(>Item\s*(4.02)(&#160;|&nbsp;)*)|(Item\s*(4.02))",
            "Non-Reliance on Previously Issued Financial Statements or a Related Audit Report or Completed Interim Review",
        ),
        (
            r"(>Item\s*(5.01)(&#160;|&nbsp;)*)|(>ITEM\s*(5.01))|(>Item\s*(5.01)(&#160;|&nbsp;)*)|(Item\s*(5.01))",
            "Changes in Control of Registrant",
        ),
        (
            r"(>Item\s*(5.02)(&#160;|&nbsp;)*)|(>ITEM\s*(5.02))|(>Item\s*(5.02)(&#160;|&nbsp;)*)|(Item\s*(5.02))",
            "Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers; Compensatory Arrangements of Certain Officers",
        ),
        (
            r"(>Item\s*(5.03)(&#160;|&nbsp;)*)|(>ITEM\s*(5.03))|(>Item\s*(5.03)(&#160;|&nbsp;)*)|(Item\s*(5.03))",
            "Amendments to Articles of Incorporation or Bylaws; Change in Fiscal Year",
        ),
        (
            r"(>Item\s*(5.04)(&#160;|&nbsp;)*)|(>ITEM\s*(5.04))|(>Item\s*(5.04)(&#160;|&nbsp;)*)|(Item\s*(5.04))",
            "Temporary Suspension of Trading Under Registrant’s Employee Benefit Plans",
        ),
        (
            r"(>Item\s*(5.05)(&#160;|&nbsp;)*)|(>ITEM\s*(5.05))|(>Item\s*(5.05)(&#160;|&nbsp;)*)|(Item\s*(5.05))",
            "Amendments to the Registrant’s Code of Ethics, or Waiver of a Provision of the Code of Ethics",
        ),
        (
            r"(>Item\s*(5.07)(&#160;|&nbsp;)*)|(>ITEM\s*(5.07))|(>Item\s*(5.07)(&#160;|&nbsp;)*)|(Item\s*(5.07))",
            "Submission of Matters to a Vote of Security Holders",
        ),
        (
            r"(>Item\s*(5.08)(&#160;|&nbsp;)*)|(>ITEM\s*(5.08))|(>Item\s*(5.08)(&#160;|&nbsp;)*)|(Item\s*(5.08))",
            "Shareholder Director Nominations",
        ),
        (
            r"(>Item\s*(6.01)(&#160;|&nbsp;)*)|(>ITEM\s*(6.01))|(>Item\s*(6.01)(&#160;|&nbsp;)*)|(Item\s*(6.01))",
            "ABS Informational and Computational Material",
        ),
        (
            r"(>Item\s*(6.02)(&#160;|&nbsp;)*)|(>ITEM\s*(6.02))|(>Item\s*(6.02)(&#160;|&nbsp;)*)|(Item\s*(6.02))",
            "Change of Servicer or Trustee",
        ),
        (
            r"(>Item\s*(6.03)(&#160;|&nbsp;)*)|(>ITEM\s*(6.03))|(>Item\s*(6.03)(&#160;|&nbsp;)*)|(Item\s*(6.03))",
            "Change in Credit Enhancement or Other External Support",
        ),
        (
            r"(>Item\s*(6.04)(&#160;|&nbsp;)*)|(>ITEM\s*(6.04))|(>Item\s*(6.04)(&#160;|&nbsp;)*)|(Item\s*(6.04))",
            "Failure to Make a Required Distribution",
        ),
        (
            r"(>Item\s*(6.05)(&#160;|&nbsp;)*)|(>ITEM\s*(6.05))|(>Item\s*(6.05)(&#160;|&nbsp;)*)|(Item\s*(6.05))",
            "Securities Act Updating Disclosure",
        ),
        (
            r"(>Item\s*(6.06)(&#160;|&nbsp;)*)|(>ITEM\s*(6.06))|(>Item\s*(6.06)(&#160;|&nbsp;)*)|(Item\s*(6.06))",
            "Static Pool",
        ),
        (
            r"(>Item\s*(7.01)(&#160;|&nbsp;)*)|(>ITEM\s*(7.01))|(>Item\s*(7.01)(&#160;|&nbsp;)*)|(Item\s*(7.01))",
            "Regulation FD Disclosure",
        ),
        (
            r"(>Item\s*(8.01)(&#160;|&nbsp;)*)|(>ITEM\s*(8.01))|(>Item\s*(8.01)(&#160;|&nbsp;)*)|(Item\s*(8.01))",
            "Other Events",
        ),
        (
            r"(>Item\s*(9.01)(&#160;|&nbsp;)*)|(>ITEM\s*(9.01))|(>Item\s*(9.01)(&#160;|&nbsp;)*)|(Item\s*(9.01))",
            "Financial Statements and Exhibits",
        ),
    ]

    def _process(self) -> Optional[pa.Table]:
        ticker = ticker_generator(self.cik, self.accession_number)
        raw_sections = {}

        # Extract the HTML sections from the document
        doc_sections = self._document_processor.extract_sections("8-K")

        if "8-K" in doc_sections:
            document_8k = doc_sections["8-K"]

            # Parse the document with BeautifulSoup
            soup = BeautifulSoup(document_8k, "html.parser")

            current_section = None  # Track the current section being processed
            previous_text = ""  # Variable to store the previous text

            # Iterate through all relevant tags to find section headers and their content
            for element in soup.find_all(["div", "span", "td", "p", "table"]):
                item_pattern_found = False
                # Check if the element text matches any section header pattern
                for item_pattern, section_name in self._SECTION_NAMES:
                    if re.search(item_pattern, element.get_text(), re.IGNORECASE):
                        # We've found a new section header
                        current_section = section_name
                        raw_sections[
                            f"{self._document_processor.unique_id}-{ticker}-{current_section}"
                        ] = ""
                        previous_text = ""  # Reset previous text for the new section
                        item_pattern_found = True
                        break  # Move on to processing content under this section

                if current_section:
                    # Accumulate the content under the current section header
                    if element.name in ["p", "span", "td", "div"]:
                        # Only add previous_text if the current element is not a section header
                        if previous_text and not item_pattern_found:
                            raw_sections[
                                f"{self._document_processor.unique_id}-{ticker}-{current_section}"
                            ] += (" " + previous_text.strip())

                        # Update previous_text with the current element's text
                        previous_text = element.get_text(separator=" ", strip=True)

                    # Handle the special case where "SIGNATURE" marks the end of relevant sections
                    if "SIGNATURE" in element.get_text():
                        current_section = (
                            None  # Stop accumulating content for the current section
                        )

            # After exiting the loop, add the last accumulated text (if any)
            if current_section and previous_text:
                raw_sections[
                    f"{self._document_processor.unique_id}-{ticker}-{current_section}"
                ] += (" " + previous_text.strip())

            # Clean the extracted section contents before returning
            for section_key, raw_content in raw_sections.items():
                cleaned_text = clean(raw_content)
                raw_sections[section_key] = cleaned_text

        return table_array(raw_sections)
