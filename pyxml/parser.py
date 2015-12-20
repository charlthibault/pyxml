from lxml import etree

from pyxml.helpers import get_pyxml_model, get_constructor_parameters


def parse(file: str, cls: object):
    model = get_pyxml_model(cls)

    tree = etree.parse(file).getroot()
    return parse_element(tree, model)


def parse_element(element, model):
    attrib = element.attrib
    object_attr = dict()

    for sublist in model.lists:
        new_list = list()
        if sublist.parent is None:
            for item_element in element.findall(sublist.items_tag):
                sublist_items_model = get_pyxml_model(sublist.items_type)
                if sublist_items_model is not None:
                    sublist_item = parse_element(item_element, sublist_items_model)
                else:
                    sublist_item = sublist.items_type(item_element.text)
                new_list.append(sublist_item)
        else:
            parent = element.find(sublist.parent)
            for item_element in parent.findall(sublist.items_tag):
                sublist_items_model = get_pyxml_model(sublist.items_type)
                if sublist_items_model is not None:
                    sublist_item = parse_element(item_element, sublist_items_model)
                else:
                    sublist_item = sublist.items_type(item_element.text)
                new_list.append(sublist_item)
        object_attr[sublist.name] = new_list

    for child_model in model.children:
        child_element = element.find(child_model.name)
        if child_model is not None:
            child_obj = parse_element(child_element, child_model)
        else:
            child_obj = sublist.items_type(child_element.text)
        object_attr[child_model.name] = child_obj


    for attr in model.attrib:
        if attr.name in attrib:
            object_attr[attr.name] = attr.type(attrib[attr.name])

    if model.text is not None:
        object_attr[model.text.name] = model.text.type(element.text)

    if len(object_attr) == 0:
        object_attr[model.name] = model.type(element.text)

    constructor_params = list()
    parameters = get_constructor_parameters(model.type)
    for name in parameters:
        if name != 'self' and name in object_attr:
            constructor_params.append(object_attr[name])

    return model.type(*constructor_params)



# for child in tree.children():
# if model.name not in child.tag:
# raise Exception('Model does not match xml file')
#
#
# if model.text is not None:
#         text_attribute



