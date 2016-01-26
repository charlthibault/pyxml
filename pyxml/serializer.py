from lxml import etree
from pyxml.helpers import get_pyxml_model
from pyxml.model import PyXmlModel


class PyXmlSerializer:
    @staticmethod
    def serialize(obj: object) -> etree.Element:
        model = get_pyxml_model(obj)
        element = etree.Element(model.name)

        if model.text is not None:
            value = getattr(obj, model.text.name)
            element.text = str(value)

        attrib = PyXmlSerializer.build_attrib(model, obj)
        PyXmlSerializer.serialize_children(element, model, obj)
        PyXmlSerializer.serialize_children_lists(element, model, obj)

        element.attrib.update(attrib)
        return element

    @staticmethod
    def build_attrib(model: PyXmlModel, obj: object) -> dict:
        attrib = dict()
        for attribute in model.attrib:
            value = getattr(obj, attribute.name)
            attrib[attribute.name] = value

        return attrib

    @staticmethod
    def serialize_children_lists(element: etree.Element, model: PyXmlModel, obj: object):
        for child_list in model.lists:
            if child_list.parent is not None:
                parent = etree.Element(child_list.parent)
                element.append(parent)
            else:
                parent = element

            items = getattr(obj, child_list.name)
            for item in items:
                if hasattr(item, 'pyxml__model'):
                    child_element = PyXmlSerializer.serialize(item)
                else:
                    child_element = etree.Element(child_list.items_name)
                    child_element.text = str(item)
                parent.append(child_element)

    @staticmethod
    def serialize_children(element: etree.Element, model: PyXmlModel, obj: object):
        for child in model.children:
            value = getattr(obj, child.name)
            if hasattr(value, 'pyxml__model'):
                child_element = PyXmlSerializer.serialize(value)
            else:
                child_element = etree.Element(child.name)
                child_element.text = child.type(value)
            element.append(child_element)
