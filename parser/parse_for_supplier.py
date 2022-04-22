"""This module contains methods to parse the data from a supplier."""

import typing as _t
import re
from datetime import date
from abc import ABC, abstractmethod
from .pdf import parser as pdf_parser

SUPPLIER_PARSERS = {
    "Amazon": {"parser": pdf_parser},
    "Amazon Order Summary": {
        "parser": pdf_parser,
        "class": "AmazonOrderSummary",
    },
    "Soak Rochford": {
        "parser": pdf_parser,
        "class": "SoakRochford",
    },
}


class BaseSupplierParser(ABC):
    """An abstract base class for parsing data from a supplier."""

    def __init__(self, file_path: str, supplier: str):
        """Initializes a new instance of the SupplierParser class."""
        self.file_path = file_path
        self.supplier = supplier

        # Default values. It is possible that not all of these attributes will
        # be set by `_summary`. Thefore, to avoid having to handle attributes
        # that do not exist, we set the default values here.
        self.order_number: str = None
        self.order_date: date = None
        self.subtotal: float = None
        self.vat: float = None
        self.delivery: float = None
        self.promotion: float = None
        self.total: float = None
        self.items_breakdown = None

        self.invoice_data = self.read_invoice()
        self.invoice_data_str = "\n".join(self.invoice_data)

    def __str__(self):
        if self.order_date:
            return f"{self.order_date} - {self.supplier}"
        else:
            return f"{self.supplier} - {self.file_path}"

    def __dict__(self) -> dict:
        return {
            "order_number": self.order_number,
            "order_date": self.order_date,
            "summary": self.summary(),
            "items": self.items_breakdown,
        }

    def process_invoice(self):
        self.items_breakdown = self._items_breakdown()
        self._summary()
        self._metadata()

    def summary(self) -> _t.Dict[str, str]:
        """Returns a summary of the invoice."""
        return {
            "subtotal": self.subtotal,
            "vat": self.vat,
            "delivery": self.delivery,
            "promotion": self.promotion,
            "total": self.total,
        }

    def read_invoice(self) -> _t.List[str]:
        """Parses the data from the supplier."""
        if self.supplier not in SUPPLIER_PARSERS:
            raise ValueError(f"Supplier {self.supplier} is not supported.")
        return SUPPLIER_PARSERS[self.supplier]["parser"](self.file_path)

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
        for i in range(len(self.invoice_data)):
            data = self.invoice_data[i]
            if data != "Items Ordered Price":
                continue

            # The product name starts here. The first element will also have
            # the quantity. e.g: 1of:product_name
            i += 1
            data = self.invoice_data[i]

            quantity = data.split("of:")[0]
            data = " ".join(data.split("of:")[1:])

            # The product name may span multiple items. Keep searching until
            # we find the end of the product name.
            product_name = ""
            search_limit = 100
            current_search = 0
            while not re.search(r"\d{2}\.\d{2}", data):
                if current_search > search_limit:
                    raise ValueError(f"Could not find price for {data}")
                else:
                    current_search += 1
                product_name += (
                    re.sub(r"( Sold by:.*| *Condition: New)", "", data) + " "
                )
                i += 1
                data = self.invoice_data[i]
            else:
                # Skip the first element as it contains the currency.
                price_inc_vat = data[1:]

            items[product_name.strip()] = {
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
            match = re.search(re_pattern, self.invoice_data_str)
            if match:
                setattr(self, field, match.groups()[1])

    def _metadata(self):
        pass


class SoakRochford(BaseSupplierParser):
    def _items_breakdown(self) -> _t.Dict[str, _t.Dict[str, str]]:
        items = {}
        for i in range(len(self.invoice_data)):
            data = self.invoice_data[i]
            if data != "SKU Product Quantity Price Total Price":
                continue

            # The next element contains the product name, quantity and price.
            # e.g: "07-05- 01 Pourer Spout Tops with Dust Caps 10 £0.25 £2.50".
            #   Product: 01 Pourer Spout Tops with Dust Caps
            #   Quantity: 10
            #   Price: £2.50
            i += 1
            data = self.invoice_data[i]
            search_limit = 100
            current_search = 0
            while not data.startswith("Subtotal"):
                if current_search > search_limit:
                    raise ValueError(f"Could not find price for {data}")
                else:
                    current_search += 1

                # If invoice spans to the next page.
                if data == "SKU Product Quantity Price Total Price":
                    i += 1
                    data = self.invoice_data[i]
                    continue

                data_groups = re.search(
                    r"([\d -]{1,} (.*?(\d{1,})) ($|£)\d{1,}\.\d{2} .*?(\d{1,}\.\d{2}))",  # noqa: E501
                    data,
                )
                quantity = data_groups.groups()[2]
                product = data_groups.groups()[1].rstrip(quantity).strip()

                # The product may have the weight mentioned twice. If so,
                # remove it.
                # eg: North Star Silver Mica Powder - 25g Weight : 25g
                product = re.sub(r" Weight : \d{1,}g", "", product)

                price = data_groups.groups()[4]
                items[product] = {"price_ex_vat": price, "quantity": quantity}

                i += 1
                data = self.invoice_data[i]

            return items

    def _summary(self):
        re_patterns = {
            "subtotal": r"(Subtotal £(\d{1,}\.\d{2}))",
            "delivery": r"(Shipping £(\d{1,}\.\d{2}))",
            "promotion": r"(Cart Discount -£(\d{1,}\.\d{2}))",
            "vat": r"(VAT £(\d{1,}\.\d{2}))",
            "total": r"(Total £(\d{1,}\.\d{2}))",
        }

        for field, re_pattern in re_patterns.items():
            match = re.search(re_pattern, self.invoice_data_str)
            if match:
                setattr(self, field, match.groups()[1])

    def _metadata(self):
        self.order_number = self._order_number()
        self.order_date = self._order_date()

    def _order_number(self) -> _t.Optional[str]:
        """Locates the order number."""
        order_number = re.search(r"(Order No: (.*?)\n)", self.invoice_data_str)
        if order_number:
            return order_number.groups()[1]

    def _order_date(self) -> _t.Optional[date]:
        """Locates the order date."""
        order_date = re.search(
            r"(Date: (\d{2}\/\d{2}\/\d{4})\n)",
            self.invoice_data_str,
        )
        if not order_date:
            return
        date_parts = order_date.groups()[1].split("/")

        return date(
            int(date_parts[2]),
            int(date_parts[1]),
            int(date_parts[0]),
        )
