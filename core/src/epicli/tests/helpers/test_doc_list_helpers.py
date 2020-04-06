from cli.helpers.doc_list_helpers import select_first, select_all
from cli.helpers.ObjDict import ObjDict

DATA = [ObjDict({'index': 1, 'name': 'test-name-1'}),
        ObjDict({'index': 2, 'name': 'test-name23'}),
        ObjDict({'index': 3, 'name': 'test-name23'})]


def test_select_first_should_return_first_matching_element():

    actual = select_first(DATA, lambda item: item.name == 'test-name-1')

    assert(actual.index == 1)


def test_select_first_should_return_first_matching_element_when_many_elements_matching():

    actual = select_first(DATA, lambda item: item.name == 'test-name23')

    assert(actual.index == 2)


def test_select_first_should_return_none_if_there_is_no_matching_elements():

    actual = select_first(DATA, lambda item: item.name == 'name-that-no-exists')

    assert(actual is None)


def test_select_first_should_return_none_if_data_is_none():

    actual = select_first(None, lambda item: item.name == 'name-that-no-exists')

    assert(actual is None)


def test_select_all_returns_all_matching_elements():
    actual = select_all(DATA, lambda item: item.name == 'test-name23')

    assert(len(actual) == 2)
    assert(actual[0].index == 2)
    assert(actual[1].index == 3)


def test_select_all_returns_empty_list_if_there_is_no_matching_elements():
    actual = select_all(DATA, lambda item: item.name == 'name-that-no-exists')

    assert(actual == [])
