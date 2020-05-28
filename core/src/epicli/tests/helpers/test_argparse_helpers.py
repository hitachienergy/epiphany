from cli.helpers.argparse_helpers import get_component_parser, components_to_dict
from cli.helpers.ObjDict import ObjDict


def test_get_component_parser():
    """Test component parser."""

    component_string = 'aaa ,  bbb,  ,, ,'
    available_components = {'aaa', 'bbb', 'ccc'}

    parser = get_component_parser(available_components)
    parsed_components = parser(component_string)

    assert isinstance(parsed_components, set)
    assert parsed_components != available_components
    assert parsed_components.issubset(available_components)


def test_get_component_parser_special_arguments():
    """Test component parser (special arguments)."""

    available_components = {'aaa', 'bbb', 'ccc'}

    parser = get_component_parser(available_components)

    parsed_components = parser(', ,, , , all, ,, ,')
    assert parsed_components == available_components

    parsed_components = parser(', ,, , , none, ,, ,')
    assert parsed_components == set()


def test_get_component_parser_incorrect_value():
    """Test component parser (incorrect value)."""

    component_string = 'aaa ,  bbb,  ,xxx, ,'
    available_components = {'aaa', 'bbb', 'ccc'}

    try:
        parser = get_component_parser(available_components)
        parser(component_string)
        return False
    except:
        return True


def test_components_to_dict():
    """Test conversion to {component -> boolean} ObjDict."""

    available_components = {'aaa', 'bbb', 'ccc'}
    parsed_components = {'bbb'}

    component_dict = components_to_dict(parsed_components, available_components)

    assert component_dict.aaa is False
    assert component_dict.bbb is True
    assert component_dict.ccc is False


def test_components_to_dict_incorrect_value():
    """Test conversion to {component -> boolean} ObjDict (incorrect value)."""

    available_components = {'aaa', 'bbb', 'ccc'}
    parsed_components = {'xxx'}

    try:
        components_to_dict(parsed_components, available_components)
        return False
    except:
        return True
