from pathlib import PurePath
from typing import Union, Optional, Literal, Iterator

from langchain_community.document_loaders.parsers import BaseImageBlobParser
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document


class ScientificPDFMinerLoader(BaseLoader):
    def __init__(
            self,
            file_path: Union[str, PurePath],
            *,
            password: Optional[str] = None,
            mode: Literal["single", "page"] = "single",
            extract_images: bool = False,
            images_parser: Optional[BaseImageBlobParser] = None,
            concatenate_pages: Optional[bool] = None,
    ) -> None:
        """Initialize with a file path.

        Args:
            file_path: The path to the PDF file to be loaded.
            mode: Extraction mode to use. Either "single" or "page" for page-wise
                extraction.
            password: Optional password for opening encrypted PDFs.
            extract_images: Whether to extract images from the PDF.
            images_parser: Optional image blob parser.
            concatenate_pages: Deprecated. If True, concatenate all PDF pages into one
                a single document. Otherwise, return one document per page.

        Returns:
            This method does not directly return data. Use the `load`, `lazy_load` or
            `aload` methods to retrieve parsed documents with content and metadata.
        """
        self.file_path = file_path
        self.password = password
        self.extract_images = extract_images
        self.images_parser = images_parser
        self.concatenate_pages = concatenate_pages

    def lazy_load(self) -> Iterator[Document]:
        pass

    @property
    def source(self) -> str:
        return self.file_path
