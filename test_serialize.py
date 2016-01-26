from model.catalog import Product, Price, Catalog
from pyxml.serializer import PyXmlSerializer
from lxml import etree


p1 = Product('biere belge', 'leffe', 'on', [Price(12.3), Price(34.5)])
p2 = Product('ricard', 'ricard', 'off', [Price(12)])
catalog = Catalog([p1, p2])

element = PyXmlSerializer.serialize(catalog)

with open('output/catalog.xml', 'wb') as fd:
    fd.write(etree.tostring(element, pretty_print=True, xml_declaration=True, encoding='utf-8'))