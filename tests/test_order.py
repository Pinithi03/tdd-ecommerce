from src.cart import Cart
from src.product import Product
from src.catalog import Catalog
from src.discounts import DiscountEngine
from src.checkout import CheckoutService


class FakePaymentGateway:
    def __init__(self, should_succeed=True):
        self.should_succeed = should_succeed

    def charge(self, amount, token):
        if not self.should_succeed:
            raise ValueError("Payment failed")
        return True


class FakeInventory:
    def __init__(self, stock):
        self.stock = stock

    def getAvailable(self, sku):
        return self.stock.get(sku, 0)


class FakeOrderRepository:
    def __init__(self):
        self.orders = []

    def save(self, order):
        self.orders.append(order)


def setup_order_dependencies(payment_success=True):
    catalog = Catalog()
    catalog.add_product(Product("P001", "Laptop", 100))
    catalog.add_product(Product("P002", "Mouse", 200))

    inventory = FakeInventory({"P001": 20, "P002": 10})
    payment_gateway = FakePaymentGateway(should_succeed=payment_success)
    discount_engine = DiscountEngine()
    order_repository = FakeOrderRepository()

    cart = Cart(catalog, inventory)
    return cart, payment_gateway, discount_engine, order_repository


def test_successful_checkout_creates_order():
    cart, payment_gateway, discount_engine, order_repository = setup_order_dependencies(True)
    cart.add_item("P001", 2)

    checkout_service = CheckoutService(payment_gateway, discount_engine, order_repository)
    result = checkout_service.checkout(cart, "tok_success")

    assert result["success"] is True
    assert len(order_repository.orders) == 1

    saved_order = order_repository.orders[0]
    assert saved_order.total == 200
    assert len(saved_order.items) == 1
    assert saved_order.items[0]["sku"] == "P001"
    assert saved_order.items[0]["quantity"] == 2


def test_failed_payment_does_not_create_order():
    cart, payment_gateway, discount_engine, order_repository = setup_order_dependencies(False)
    cart.add_item("P001", 2)

    checkout_service = CheckoutService(payment_gateway, discount_engine, order_repository)
    result = checkout_service.checkout(cart, "tok_fail")

    assert result["success"] is False
    assert len(order_repository.orders) == 0