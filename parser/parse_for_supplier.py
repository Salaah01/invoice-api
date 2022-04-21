"""This module contains methods to parse the data from a supplier."""

import typing as _t
import re
from datetime import date
from abc import ABC, abstractmethod
from .pdf import parser as pdf_parser

SUPPLIER_PARSERS = {"Amazon": pdf_parser, "Amazon Order Summary": pdf_parser}


class BaseSupplierParser(ABC):
    """An abstract base class for parsing data from a supplier."""

    def __init__(self, file_path: str, supplier: str):
        """Initializes a new instance of the SupplierParser class."""
        self.file_path = file_path
        self.supplier = supplier

        if self.supplier not in SUPPLIER_PARSERS:
            raise ValueError(f"Supplier {self.supplier} is not supported.")

        self.parsed_data = self.parse()
        self.parsed_data_str = "\n".join(self.parsed_data)

        self.order_number: str = None
        self.order_date: date = None
        self.subtotal: float = None
        self.vat: float = None
        self.delivery: float = None
        self.promotion: float = None
        self.total: float = None

    def parse(self) -> _t.List[str]:
        """Parses the data from the supplier."""
        return SUPPLIER_PARSERS[self.supplier](self.file_path)

    @abstractmethod
    def _items_breakdown(self) -> _t.Dict[str, _t.Dict[str, str]]:
        """Process the passed data returning a breakdown of the costs of each
        invoice item.
        Returns:
            A dictionary of items purchased where each key represents an item
            purchased and each value is a dictionary containing item price
            (ex Vat), VAT and quantity.
        """

    @abstractmethod
    def _summary(self) -> _t.Dict[str, str]:
        """Process the passed data returning a summary of the invoice. The
        information would include the total amount paid, any discount and
        delivery.
        """

    def _metadata(self) -> _t.Dict[str, _t.Any]:
        """Process the passed data returning a dictionary of anything that may
        be considered to be additional/metadata about the invoice.
        """
        return {}


class AmazonOrderSummary(BaseSupplierParser):
    """Parses the data from an Amazon Order Summary PDF."""

    def _items_breakdown(self) -> _t.Dict[str, _t.Dict[str, str]]:
        items = {}
        for i in range(len(self.parsed_data)):
            data = self.parsed_data[i]
            if data != "Items Ordered Price":
                continue

            # The product name starts here. The first element will also have
            # the quantity. e.g: 1of:product_name
            i += 1
            data = self.parsed_data[i]

            quantity = data.split("of:")[0]
            data = " ".join(data.split("of:")[1:])

            # The product name may span multiple items. Keep searching until
            # we find the end of the product name.
            product_name = ""
            search_limit = 50
            current_search = 0
            while not re.search(r"\d{2}\.\d{2}", data):
                if current_search > search_limit:
                    raise ValueError(f"Could not find price for {data}")

                product_name += data + " "
                i += 1
                data = self.parsed_data[i]
            else:
                # Skip the first element as it contains the currency.
                price_inc_vat = data[1:]

            items[product_name] = {
                "price_inc_vat": price_inc_vat,
                "quantity": quantity,
            }

        return items

    def _summary(self):

        re_patterns = {
            "subtotal": r"(Item\(s\) Subtotal: *.?(\d{1,}\.\d{2}))",
            "delivery": r"(Postage & Packing: *.?(\d{1,}\.\d{2}))",
            "vat": r"(VAT: *.?(\d{1,}\.\d{2}))",
            "total": r"(Grand Total: *.?(\d{1,}\.\d{2}))",
        }

        for field, re_pattern in re_patterns.items():
            match = re.search(re_pattern, self.parsed_data_str)
            if match:
                setattr(self, field, match.groups()[1])

    def _metadata(self):
        pass
