"""Parses PDF invoices."""

import typing as _t
from borb.pdf.pdf import PDF
from borb.toolkit.text.simple_text_extraction import SimpleTextExtraction


def parser(file_path: str) -> _t.List[str]:
    """Parses a PDF invoice."""
    extractor = SimpleTextExtraction()
    with open(file_path, "rb") as pdf_file:
        PDF.loads(pdf_file, [extractor])

    text = ""
    page = 0
    while True:
        page_text = extractor.get_text_for_page(page)
        if not bool(page_text):
            break
        text += page_text + "\n"
        page += 1

    return text.rstrip("\n").split("\n")
