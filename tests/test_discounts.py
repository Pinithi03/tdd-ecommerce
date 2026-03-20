import pytest
from src.cart import Cart
from src.product import Product
from src.catalog import Catalog
from src.discounts import DiscountEngine


def setup_cart():
    catalog = Catalog()
    catalog.add_product(Product("P001", "Laptop", 100))
    cart = Cart(catalog)
    return cart


def test_bulk_discount_applied():
    cart = setup_cart()
    cart.add_item("P001", 10)  # 100 * 10 = 1000

    engine = DiscountEngine()
    total = engine.apply_discounts(cart)

    # 10% off → 1000 - 100 = 900
    assert total == 900


def test_order_discount_applied():
    catalog = Catalog()
    catalog.add_product(Product("P001", "Laptop", 100))
    catalog.add_product(Product("P002", "Mouse", 100))

    cart = Cart(catalog)
    cart.add_item("P001", 10)  # 1000 → bulk → 900
    cart.add_item("P002", 2)   # +200 → total = 1100 before discounts

    engine = DiscountEngine()
    total = engine.apply_discounts(cart)

    # bulk → P001 becomes 900
    # +200 = 1100
    # order discount → 1100 * 0.95 = 1045
    assert total == 1045