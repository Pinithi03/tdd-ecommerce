class CheckoutService:
    def __init__(self, payment_gateway, discount_engine, order_repository=None):
        self.payment_gateway = payment_gateway
        self.discount_engine = discount_engine
        self.order_repository = order_repository

    def validate_cart(self, cart):
        if not cart.items:
            raise ValueError("Cart is empty")

    def checkout(self, cart, token):
        try:
            self.validate_cart(cart)
            total = self.discount_engine.apply_discounts(cart)
            self.payment_gateway.charge(total, token)

            return {
                "success": True,
                "message": "Checkout successful",
                "total": total
            }
        except ValueError as e:
            return {
                "success": False,
                "message": str(e)
            }