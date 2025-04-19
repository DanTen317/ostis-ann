from pathlib import PurePath
from typing import Union, Optional, Literal

from langchain_community.document_loaders.parsers import BaseImageBlobParser
from langchain_community.document_loaders.parsers.pdf import logger


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
        self.file_path = file_path
        self.password = password
        self.extract_images = extract_images
        self.images_parser = images_parser
        if concatenate_pages is not None:
            logger.warning(
                "`concatenate_pages` parameter is deprecated. "
                "Use `mode='single' or 'page'` instead."
            )
            self.mode = "single" if concatenate_pages else "page"
