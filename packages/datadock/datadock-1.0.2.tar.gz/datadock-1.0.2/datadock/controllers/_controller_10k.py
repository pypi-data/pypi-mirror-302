import re
import pyarrow as pa
from typing import Optional, Dict

from bs4 import BeautifulSoup

from datadock.controllers._base_controllers import FormBaseController
from datadock.src.utils import clean
from datadock.core import table_array


class Clean10KController(FormBaseController):
    _SECTION_NAMES = [
        ("item1", "Business"),
        ("item1a", "Risk Factors"),
        ("item1b", "Unresolved Staff Comments"),
        ("item1c", "Cybersecurity"),
        ("item2", "Properties"),
        ("item3", "Legal Proceedings"),
        ("item4", "Mine Safety Disclosures"),
        (
            "item5",
            "Market for Registrant’s Common Equity, Related Stockholder Matters, and Issuer Purchases of Equity Securities",
        ),
        ("item6", "Selected Financial Data"),
        (
            "item7",
            "Management’s Discussion and Analysis of Financial Condition and Results of Operations",
        ),
        ("item7a", "Quantitative and Qualitative Disclosures about Market Risk"),
        ("item8", "Financial Statements and Supplementary Data"),
        (
            "item9",
            "Changes in and Disagreements with Accountants on Accounting and Financial Disclosure",
        ),
        ("item9a", "Controls and Procedures"),
        ("item9b", "Other Information"),
        (
            "item9c",
            "Disclosure Regarding Foreign Jurisdictions that Prevent Inspections",
        ),
        ("item10", "Directors, Executive Officers, and Corporate Governance"),
        ("item11", "Executive Compensation"),
        (
            "item12",
            "Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters",
        ),
        (
            "item13",
            "Certain Relationships and Related Transactions, and Director Independence",
        ),
        ("item14", "Principal Accountant Fees and Services"),
        ("item15", "Exhibit and Financial Statement Schedules"),
        ("item16", "Form 10-K Summary"),
    ]

    def _process(self) -> Optional[pa.Table]:
        raw_sections = {}
        doc_sections = self._document_processor.extract_sections("10-K")

        if "10-K" in doc_sections:
            document_10k = doc_sections["10-K"]

            # Parse the document with BeautifulSoup
            soup = BeautifulSoup(document_10k, "html.parser")

            # Extract section names from <td> tags with an <a> tag
            for td_tag in soup.find_all("td"):
                a_tag = td_tag.find("a", href=True)
                if not a_tag:
                    continue  # Skip if there is no <a> tag

                # Get the section name text from the <a> tag
                section_text = a_tag.get_text(strip=True)

                for item_pattern, section_name in self._SECTION_NAMES:
                    if re.search(section_name, section_text, re.IGNORECASE):
                        # Match the href with the corresponding content <p> tag by id
                        href_value = a_tag["href"].lstrip("#")
                        content_tag = soup.find(id=href_value)
                        section_content = ""

                        if content_tag:
                            # Check if the content_tag is part of a <span> tag with no direct text
                            if content_tag.name == "span" and not content_tag.get_text(
                                strip=True
                            ):
                                # Check if the parent contains the text (e.g., a <p> tag or another wrapping element)
                                parent_tag = content_tag.find_parent(["p", "span"])
                                if parent_tag:
                                    section_content = parent_tag.get_text(
                                        separator=" ", strip=True
                                    )
                            else:
                                section_content = content_tag.get_text(
                                    separator=" ", strip=True
                                )

                            # Gather all the content until the next section id is encountered
                            next_tag = content_tag.find_next_sibling()
                            while next_tag and not self._is_new_section(next_tag):
                                section_content += " " + next_tag.get_text(
                                    separator=" ", strip=True
                                )
                                next_tag = next_tag.find_next_sibling()

                            # Save the accumulated content for the current section
                            raw_sections[
                                f"{self._document_processor.unique_id}-{section_name}"
                            ] = section_content
                        break

            # Clean up sections by removing overlaps where a section contains the next section's name
            raw_sections = self._clean_overlapping_sections(raw_sections)

            # Clean the extracted section contents before returning
            for section_key, raw_content in raw_sections.items():
                cleaned_text = clean(raw_content)
                raw_sections[section_key] = cleaned_text

        return table_array(raw_sections) if raw_sections else None

    def _is_new_section(self, element) -> bool:
        """
        Checks if the current element contains the start of a new section.
        """
        if element.name in ["p", "span"] and element.get("id"):
            # Check if the id matches any section header
            for _, section_name in self._SECTION_NAMES:
                if re.search(section_name, element.get_text(), re.IGNORECASE):
                    return True
        return False

    def _clean_overlapping_sections(self, sections: Dict[str, str]) -> Dict[str, str]:
        """
        Ensure each section's content is unique and doesn't include the content of subsequent sections.
        """
        section_keys = list(sections.keys())
        for i, current_section_key in enumerate(section_keys):
            current_content = sections[current_section_key]

            # Look ahead to the next section to find and remove overlaps
            if i + 1 < len(section_keys):
                next_section_name = self._SECTION_NAMES[i + 1][1]
                next_section_pattern = re.escape(next_section_name)

                # Remove anything from the current content that includes the next section name
                next_section_match = re.search(
                    next_section_pattern, current_content, re.IGNORECASE
                )
                if next_section_match:
                    # Cut the content from the start of the next section's name
                    sections[current_section_key] = current_content[
                        : next_section_match.start()
                    ].strip()

        return sections
