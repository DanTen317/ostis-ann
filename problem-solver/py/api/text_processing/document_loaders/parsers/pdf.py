from pathlib import PurePath
from typing import Optional, Union, Iterator

from api.text_processing.document_loaders.parsers.classifiers import ObjectsClassifier
from api.text_processing.document_loaders.parsers.extractors import PDFMinerExtractor
from api.text_processing.document_loaders.base import BaseFileParser
from api.text_processing.objects import Document


class PDFMinerParser(BaseFileParser):
    def __init__(
            self,
            *,
            password: Optional[str] = None
    ):
        super().__init__()
        self.password = password
        self.extractor = PDFMinerExtractor(print_logs=True)
        self.object_classifier = ObjectsClassifier()

    @staticmethod
    def decode_text(s: Union[bytes, str]) -> str:
        from pdfminer.utils import PDFDocEncoding
        if isinstance(s, bytes) and s.startswith(b"\xfe\xff"):
            return str(s[2:], "utf-16be", "ignore")
        try:
            ords = (ord(c) if isinstance(c, str) else c for c in s)
            return "".join(PDFDocEncoding[o] for o in ords)
        except IndexError:
            return str(s)

    def lazy_parse(self, file_path: Union[str, PurePath]):
        try:
            import pdfminer
            from pdfminer.converter import PDFLayoutAnalyzer
            from pdfminer.layout import (
                LAParams
            )
            from pdfminer.pdfpage import PDFPage

        except ImportError:
            raise ImportError(
                "pdfminer package not found, please install it"
                "with `pip install pdfminer.six"
            )
        objects = self.extractor.load(file_path)

        objects = self.object_classifier.classify(objects)
        self.extractor.save_to_json(objects, f"output.json")
        return objects
