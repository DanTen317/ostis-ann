import re


class ScientificCleaner:
    def __init__(self):
        # Page structure patterns
        self.page_header_regex = \
            r"^(?:\d+\s*(?:(?:Глава|Раздел)\s*\d+(?:\.\d+)*\..*)|(?:\d+(?:\.\d+)*\.\s+.*\s*\d+))(?:\n|$)"  # Headers with page numbers
        self.page_footer_regex = r"\n.*(?:\n.*){0,2}$"  # Last 1-3 lines of text
        self.page_number_regex = r"\b(?:Page\s+)?\d+(?:\s+of\s+\d+)?\b"
        self.timestamp_regex = r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{2}:\d{2}(?::\d{2})?"
        self.url_regex = r"https?://(?:[\w-]|\.|/|\?|=|%|&|#)+(?:\b|$)"
        self.email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        self.bullet_points_regex = r"(?:^|\n)[\s]*[•\-\*][\s]+"
        self.section_header_regex = r"(?:^|\n)(?:[A-ZА-Я][A-Za-zА-Яа-я\s\-]{2,}:|\d+\.\s+[A-ZА-Я])"

        self._word_wrap_regex = r"(?<=[A-Za-zА-Яа-я])-\n(?=[a-zа-я]+)"
        self._multi_spase_regex = r"\s\s+"
        self._multi_newline_regex = r"\n(\n\s+)+"
        self._image_regex = r"(Рис|Рисунок)\.?\s*\d+(\.\d+)?(\.)?\s*(.+)"
        self._unicode_private_use_area_regex = r"[\uf000-\uffff]"
        self._em_space_regex = r"\u2003"

    def clean_text(self, text: str):
        text = re.sub(self._multi_spase_regex, " ", text)
        text = re.sub(self._word_wrap_regex, "", text)
        text = re.sub(self._multi_newline_regex, "\n", text)
        text = re.sub(self._unicode_private_use_area_regex, "", text)
        text = re.sub(self._em_space_regex, " ", text)
        return text