from pyxml.decorators import pyxml_children, pyxml_attributes, pyxml_list, pyxml_text


@pyxml_attributes('currency')
@pyxml_text('value')
class Price:
    def __init__(self, value: float, currency: str='EU'):
        self.value = value
        self.currency = currency

    def __str__(self):
        return 'value: {}\n\t\tcurrency: {}\n\t\t'.format(self.value,
                                                self.currency)


@pyxml_children('brand', 'name')
@pyxml_attributes('autocomplete')
@pyxml_list('prices', items_type=Price, items_tag='price', parent='prices')
class Product:
    def __init__(self, name: str, brand: str, autocomplete: str, prices: list):
        self.name = name
        self.brand = brand
        self.autocomplete = autocomplete
        self.prices = prices

    def __str__(self):
        output = 'name: {}\n\tbrand: {}\n\tautocomplete: {}\n\tprices: \n\t\t'.format(self.name,
                                                                              self.brand,
                                                                              self.autocomplete)
        for price in self.prices:
            output += '{}\n\t\t'.format(price)
        return output


@pyxml_list('products', items_type=Product, items_tag='product')
class Catalog:
    def __init__(self, products: list):
        self.products = products

    def __str__(self):
        output =  'Products: \n\t'
        for product in self.products:
            output += '{}\n\t'.format(product)
        return output
