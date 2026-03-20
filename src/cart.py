class Cart:
    def __init__(self, catalog):
        self.catalog = catalog
        self.items = {}

    def get_product(self, sku):
        product = self.catalog.find_by_sku(sku)
        if not product:
            raise ValueError("Product not found")
        return product

    def add_item(self, sku, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        self.get_product(sku)  

        if sku in self.items:
            self.items[sku] += quantity
        else:
            self.items[sku] = quantity

    def remove_item(self, sku):
        if sku in self.items:
            del self.items[sku]

    def total(self):
        total = 0
        for sku, quantity in self.items.items():
            product = self.get_product(sku)  
            total += product.price * quantity
        return total