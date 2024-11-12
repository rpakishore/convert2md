from pathlib import Path
from .parent import ParentParser
from docling.document_converter import DocumentConverter


class DoclingParser(ParentParser):
    def __init__(self) -> None:
        super().__init__()

    def _process_file(self, filepath: Path) -> str:
        converter = DocumentConverter()
        result = converter.convert(filepath)
        return result.document.export_to_markdown()
