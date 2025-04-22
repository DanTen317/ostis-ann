import re
from pathlib import PurePath
from pprint import pprint
from typing import Union, Optional, Literal, Iterator, List

from langchain_community.document_loaders.parsers import BaseImageBlobParser
from langchain_community.document_loaders.parsers.pdf import logger
from langchain_core.documents import Document
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTPage, LTTextContainer, LTTextBox, LTTextLine
from pdfminer.pdfdocument import PDFDocument

from api.custom_loaders.parsers.cleaners.scientific_cleaner import ScientificCleaner


class PDFMinerParser:
    def __init__(
            self,
            file_path: Union[str, PurePath],
            *,
            password: Optional[str] = None,
            mode: Literal["single", "page"] = "single",
            extract_images: bool = False,
            images_parser: Optional[BaseImageBlobParser] = None,
            concatenate_pages: Optional[bool] = None,
    ):
        """Initialize a parser based on PDFMiner.

        Args:
            file_path: The path to the PDF file to be parsed.
            password: Optional password for opening encrypted PDFs.
            mode: Extraction mode to use. Either "single" or "page" for page-wise
                extraction.
            extract_images: Whether to extract images from PDF.
            concatenate_pages: Deprecated. If True, concatenate all PDF pages
                into one a single document. Otherwise, return one document per page.

        Returns:
            This method does not directly return data. Use the `parse` or `lazy_parse`
            methods to retrieve parsed documents with content and metadata.

        Raises:
            ValueError: If the `mode` is not "single" or "page".

        Warnings:
            `concatenate_pages` parameter is deprecated. Use `mode='single' or 'page'
            instead.
        """
        if mode not in ["single", "page"]:
            raise ValueError("mode must be single or page")
        if extract_images and not images_parser:
            images_parser = None
        self.file_path = PurePath(file_path)
        self.password = password
        self.extract_images = extract_images
        self.images_parser = images_parser
        self.text_cleaner = ScientificCleaner()
        if concatenate_pages is not None:
            logger.warning(
                "`concatenate_pages` parameter is deprecated. "
                "Use `mode='single' or 'page'` instead."
            )
            self.mode = "single" if concatenate_pages else "page"

    def lazy_parse(self) -> List[Document]:
        docs = []
        for page_num, page in enumerate(extract_pages(self.file_path)):
            page_metadata = {
                "page_number": page.pageid,
                "page_header": ""
            }
            self.extract_objects(page)

    def extract_text(self, element):
        line_text = element.get_text()
        line_text = re.sub(r"\(cid:\d+\)", "", line_text)

        line_text = self.text_cleaner.clean_text(text=line_text)
        # print(element.bbox)

        return str(line_text)

    def extract_objects(self, page: LTPage):
        objects = []
        for element in page:
            pprint({"page:": page.pageid,
                    "page_size": page.bbox,
                    "box:": [element.x0, element.y0, element.x1, element.y1],
                    "type:": type(element),
                    "text:": self.extract_text(element) if isinstance(element, (LTTextContainer, LTTextBox,
                                                                                LTTextLine)) else None
                    },sort_dicts=False)

    def text_is_on_image(self):
        pass

    def merge_by_sections(self, documents: List[Document]):
        merged_docs = []
        current_section = []
        pass


pser = PDFMinerParser(r"C:\Users\Danii\Downloads\Golovko-9-21.pdf")
a = pser.lazy_parse()
