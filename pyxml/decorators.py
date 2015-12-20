from pyxml.helpers import get_pyxml_model, get_parameter_type
from pyxml.model import PyXmlAttribute, PyXmlList, PyXmlModel, PyXmlText


def pyxml_text(text_name: str):
    def refine_model(cls):
        model = get_pyxml_model(cls)
        type = get_parameter_type(text_name, cls)
        model.text = PyXmlText(text_name, type)
        return cls

    return refine_model


def pyxml_name(node_name: str):
    def refine_model(cls):
        model = get_pyxml_model(cls)
        model.name = node_name
        return cls

    return refine_model


def pyxml_attributes(*attribute_names):
    def refine_model(cls):
        model = get_pyxml_model(cls)

        for attribute_name in attribute_names:
            type = get_parameter_type(attribute_name, cls)
            attribute = PyXmlAttribute(attribute_name, type)
            model.attrib.append(attribute)
        return cls

    return refine_model


def pyxml_children(*children_names):
    def refine_model(cls):
        model = get_pyxml_model(cls)

        for child_name in children_names:
            type = get_parameter_type(child_name, cls)
            if hasattr(type, 'pyxml__model'):
                child = type.pyxml__model
            else:
                child = PyXmlModel(child_name, type)
            model.children.append(child)
        return cls

    return refine_model


# def pyxml_lists(*list_names):
#     def refine_model(cls):
#         model = get_pyxml_model(cls)
#
#         for list_name in list_names:
#             child_list = PyXmlList(list_name, list_name)
#             model.lists.append(child_list)
#         return cls
#
#     return refine_model


def pyxml_list(name, items_type: type, items_tag: str=None, parent: str=None):
    def refine_model(cls):
        model = get_pyxml_model(cls)

        child_list = PyXmlList(name, items_type, items_tag, parent)
        model.lists.append(child_list)
        return cls

    return refine_model
