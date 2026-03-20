import pytest
from src.cart import Cart
from src.product import Product
from src.catalog import Catalog


def setup_catalog():
    catalog = Catalog()
    catalog.add_product(Product("P001", "Laptop", 1000))
    catalog.add_product(Product("P002", "Mouse", 100))
    return catalog


def test_add_item_success():
    catalog = setup_catalog()
    cart = Cart(catalog)

    cart.add_item("P001", 2)

    assert cart.items["P001"] == 2


def test_add_item_invalid_quantity():
    catalog = setup_catalog()
    cart = Cart(catalog)

    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        cart.add_item("P001", 0)


def test_add_item_product_not_found():
    catalog = setup_catalog()
    cart = Cart(catalog)

    with pytest.raises(ValueError, match="Product not found"):
        cart.add_item("INVALID", 1)


def test_remove_item():
    catalog = setup_catalog()
    cart = Cart(catalog)

    cart.add_item("P001", 2)
    cart.remove_item("P001")

    assert "P001" not in cart.items


def test_total_calculation():
    catalog = setup_catalog()
    cart = Cart(catalog)

    cart.add_item("P001", 1)  # 1000
    cart.add_item("P002", 2)  # 200

    assert cart.total() == 1200