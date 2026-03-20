import pytest
from src.cart import Cart
from src.product import Product
from src.catalog import Catalog
from src.discounts import DiscountEngine
from src.checkout import CheckoutService


class FakePaymentGateway:
    def __init__(self, should_succeed=True):
        self.should_succeed = should_succeed
        self.charged_amount = None
        self.token_used = None

    def charge(self, amount, token):
        if not self.should_succeed:
            raise ValueError("Payment failed")
        self.charged_amount = amount
        self.token_used = token
        return True


class FakeInventory:
    def __init__(self, stock):
        self.stock = stock

    def getAvailable(self, sku):
        return self.stock.get(sku, 0)


def setup_checkout_dependencies(payment_success=True):
    catalog = Catalog()
    catalog.add_product(Product("P001", "Laptop", 100))
    catalog.add_product(Product("P002", "Mouse", 200))

    inventory = FakeInventory({"P001": 20, "P002": 10})
    payment_gateway = FakePaymentGateway(should_succeed=payment_success)
    discount_engine = DiscountEngine()

    cart = Cart(catalog, inventory)
    return cart, payment_gateway, discount_engine


def test_checkout_success():
    cart, payment_gateway, discount_engine = setup_checkout_dependencies(payment_success=True)
    cart.add_item("P001", 2)  # 200

    checkout_service = CheckoutService(payment_gateway, discount_engine)
    result = checkout_service.checkout(cart, "tok_123")

    assert result["success"] is True
    assert result["message"] == "Checkout successful"
    assert result["total"] == 200
    assert payment_gateway.charged_amount == 200
    assert payment_gateway.token_used == "tok_123"


def test_checkout_fails_when_payment_fails():
    cart, payment_gateway, discount_engine = setup_checkout_dependencies(payment_success=False)
    cart.add_item("P001", 2)  # 200

    checkout_service = CheckoutService(payment_gateway, discount_engine)
    result = checkout_service.checkout(cart, "tok_456")

    assert result["success"] is False
    assert result["message"] == "Payment failed"