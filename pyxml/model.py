class PyXmlAttribute:
    def __init__(self, name: str, type: type):
        self.name = name
        self.type = type


class PyXmlText:
    def __init__(self, name: str, type: type):
        self.name = name
        self.type = type


class PyXmlList:
    def __init__(self, name: str, items_type, items_tag: str=None, parent: str=None):
        self.name = name
        self.items_type = items_type
        self.items_tag = items_tag if items_tag is not None else name
        self.parent = parent


class PyXmlModel:
    def __init__(self, name, type):
        self.lists = list()
        self.attrib = list()
        self.children = list()
        self.text = None
        self.name = name
        self.type = type

    def get_child(self, name):
        for child in self.children:
            if child.name == name:
                return child

        return None
