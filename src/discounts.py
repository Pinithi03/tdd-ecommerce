class DiscountEngine:
    def apply_discounts(self, cart):
        total = self.calculate_subtotal(cart)
        total = self.apply_order_discount(total)
        return total

    def calculate_subtotal(self, cart):
        total = 0
        for sku, quantity in cart.items.items():
            product = cart.get_product(sku)
            total += self.apply_bulk_discount(product.price, quantity)
        return total

    def apply_bulk_discount(self, price, quantity):
        if quantity >= 10:
            return price * quantity * 0.9
        return price * quantity

    def apply_order_discount(self, total):
        if total >= 1000:
            return total * 0.95
        return total