class Catalog:
    def __init__(self):
        self.products = {}

    def add_product(self, product):
        self.products[product.sku] = product

    def find_by_sku(self, sku):
        return self.products.get(sku)