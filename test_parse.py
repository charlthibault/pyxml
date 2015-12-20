from model.catalog import Catalog
from pyxml.parser import parse

catalog = parse('output/catalog.xml', Catalog)

print(catalog)