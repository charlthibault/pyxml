from inspect import getmembers, signature
from pyxml.model import PyXmlModel


def get_pyxml_model(obj: object) -> PyXmlModel:
    if hasattr(obj, 'pyxml__model'):
        return getattr(obj, 'pyxml__model')
    else:
        if isinstance(obj, type):
            name = obj.__name__.lower()
            obj_type = obj
        else:
            name = obj.__class__.__name__.lower()
            obj_type = type(obj)
        model = PyXmlModel(name, obj_type)
        setattr(obj, 'pyxml__model', model)
        return model


def get_constructor_parameters(cls):
    for member in getmembers(cls):
        if member[0] == '__init__':
            return signature(member[1]).parameters


def get_parameter_type(parameter_name, cls):
    parameters = get_constructor_parameters(cls)
    for name, parameter in parameters.items():
        if name == parameter_name:
            return parameter.annotation

    return None
