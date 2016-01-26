from model.catalog import Catalog
from pyxml.parser import PyXmlParser

catalog = PyXmlParser.parse('output/catalog.xml', Catalog)

print(catalog)