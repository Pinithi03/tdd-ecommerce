from src.product import Product
from src.catalog import Catalog


def test_catalog_can_add_and_find_product_by_sku():
    catalog = Catalog()
    product = Product("P001", "Laptop", 1500.00)

    catalog.add_product(product)

    assert catalog.find_by_sku("P001") == product


def test_catalog_returns_none_for_missing_sku():
    catalog = Catalog()

    assert catalog.find_by_sku("UNKNOWN") is None