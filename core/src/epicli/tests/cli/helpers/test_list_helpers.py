import unittest
from cli.helpers.list_helpers import select_first


class ListHelpersTestCase(unittest.TestCase):
    def setUp(self):
        self.data = [{'index': 1, 'name': 'test-name-1'}, {'index': 2, 'name': 'test-name23'}, {'index': 3, 'name': 'test-name23'}]

    def test_select_first_should_return_first_matching_element_when_many_elements_matching(self):

        actual = select_first(self.data, lambda item: item['name'] == 'test-name23')

        self.assertEqual(actual['index'], 2)
