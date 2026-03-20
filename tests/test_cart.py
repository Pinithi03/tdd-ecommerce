import pytest
from src.cart import Cart
from src.product import Product
from src.catalog import Catalog


class FakeInventory:
    def __init__(self, stock):
        self.stock = stock

    def getAvailable(self, sku):
        return self.stock.get(sku, 0)


def setup_catalog():
    catalog = Catalog()
    catalog.add_product(Product("P001", "Laptop", 1000))
    catalog.add_product(Product("P002", "Mouse", 100))
    return catalog


def test_add_item_fails_when_inventory_insufficient():
    catalog = setup_catalog()
    inventory = FakeInventory({"P001": 2})
    cart = Cart(catalog, inventory)

    with pytest.raises(ValueError, match="Insufficient inventory"):
        cart.add_item("P001", 3)


def test_add_item_succeeds_when_inventory_is_enough():
    catalog = setup_catalog()
    inventory = FakeInventory({"P001": 5})
    cart = Cart(catalog, inventory)

    cart.add_item("P001", 3)

    assert cart.items["P001"] == 3