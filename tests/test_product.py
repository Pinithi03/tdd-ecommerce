from src.product import Product
import pytest


def test_create_product_success():
    product = Product("P001", "Laptop", 1500.00)
    assert product.sku == "P001"
    assert product.name == "Laptop"
    assert product.price == 1500.00


def test_create_product_fails_when_price_negative():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        Product("P002", "Mouse", -100.00)


def test_create_product_fails_when_sku_missing():
    with pytest.raises(ValueError, match="SKU is required"):
        Product("", "Keyboard", 2500.00)


def test_create_product_fails_when_name_missing():
    with pytest.raises(ValueError, match="Name is required"):
        Product("P003", "", 500.00)