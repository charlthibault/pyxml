from lxml import etree
from pyxml.helpers import get_pyxml_model, get_constructor_parameters, find, find_all


class PyXmlParser:
    @staticmethod
    def parse(file: str, cls: object):
        model = get_pyxml_model(cls)

        tree = etree.parse(file).getroot()
        return PyXmlParser.parse_element(tree, model)

    @staticmethod
    def parse_element(element, model):
        attrib = element.attrib
        object_attr = dict()

        PyXmlParser.parse_lists(element, model, object_attr)
        PyXmlParser.parser_children(element, model, object_attr)
        PyXmlParser.parse_attributes(attrib, model, object_attr)

        if model.text is not None:
            object_attr[model.text.name] = model.text.type(element.text)
        if len(object_attr) == 0:
            object_attr[model.name] = model.type(element.text)

        return PyXmlParser.build_object(model, object_attr)

    @staticmethod
    def parse_lists(element, model, object_attr):
        for sublist in model.lists:
            new_list = list()
            if sublist.parent is None:
                parent = element
            else:
                parent = find(sublist.parent, element, model)

            for item_element in find_all(sublist.items_tag, parent, model):
                sublist_items_model = get_pyxml_model(sublist.items_type)
                if sublist_items_model is not None:
                    sublist_item = PyXmlParser.parse_element(item_element, sublist_items_model)
                else:
                    sublist_item = sublist.items_type(item_element.text)
                new_list.append(sublist_item)
            object_attr[sublist.name] = new_list

    @staticmethod
    def parser_children(element, model, object_attr):
        for child_model in model.children:
            child_element = find(child_model.name, element, model)
            if hasattr(child_model.type, 'pyxml__model'):
                child_obj = PyXmlParser.parse_element(child_element, child_model.type.pyxml__model)
            else:
                child_obj = child_model.type(child_element.text)
            object_attr[child_model.name] = child_obj

    @staticmethod
    def parse_attributes(attrib, model, object_attr):
        for attr in model.attrib:
            if attr.name in attrib:
                object_attr[attr.name] = attr.type(attrib[attr.name])

    @staticmethod
    def build_object(model, object_attr):
        constructor_params = list()
        parameters = get_constructor_parameters(model.type)
        for name in parameters:
            if name != 'self' and name in object_attr:
                constructor_params.append(object_attr[name])
        return model.type(*constructor_params)
