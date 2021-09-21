from collections import OrderedDict

import pytest
from cli.helpers.objdict_helpers import dict_to_objdict, objdict_to_dict, is_named_list, assert_unique_names_in_named_list, merge_objdict, DuplicatesInNamedListException, TypeMismatchException, replace_yesno_with_booleans
from cli.helpers.ObjDict import ObjDict


def test_dict_to_objdict():
    base = {
        'field1': {
            'field2': {
                'field3': {
                    'field4': 'val'
                }
            }
        }
    }
    converted = dict_to_objdict(base)

    assert isinstance(converted, ObjDict)
    assert isinstance(converted.field1, ObjDict)
    assert isinstance(converted.field1.field2, ObjDict)
    assert isinstance(converted.field1.field2.field3, ObjDict)
    assert isinstance(converted.field1.field2.field3.field4, str)
    assert converted.field1.field2.field3.field4 == 'val'


def test_dict_to_objdict_different_dict_types():
    base = {
        'field1': ObjDict({
            'field2': {
                'field3': OrderedDict({
                    'field4': 'val'
                })
            }
        })
    }
    converted = dict_to_objdict(base)

    assert isinstance(converted, ObjDict)
    assert isinstance(converted.field1, ObjDict)
    assert isinstance(converted.field1.field2, ObjDict)
    assert isinstance(converted.field1.field2.field3, ObjDict)
    assert isinstance(converted.field1.field2.field3.field4, str)
    assert converted.field1.field2.field3.field4 == 'val'


def test_dict_to_objdict_nested_with_lists():
    base = {
        'field1': [
            {
                'field2': {
                    'field3': [
                        {
                            'field4': 'val'
                        },
                    ]
                }
            },
        ]
    }
    converted = dict_to_objdict(base)

    assert isinstance(converted, ObjDict)
    assert isinstance(converted.field1, list)
    assert isinstance(converted.field1[0], ObjDict)
    assert isinstance(converted.field1[0].field2, ObjDict)
    assert isinstance(converted.field1[0].field2.field3, list)
    assert isinstance(converted.field1[0].field2.field3[0], ObjDict)
    assert isinstance(converted.field1[0].field2.field3[0].field4, str)
    assert converted.field1[0].field2.field3[0].field4 == 'val'


def test_objdict_to_dict():
    base = ObjDict({
        'field1': ObjDict({
            'field2': ObjDict({
                'field3': ObjDict({
                    'field4': 'val'
                })
            })
        })
    })
    converted = objdict_to_dict(base)

    assert isinstance(converted, dict)
    assert isinstance(converted['field1'], dict)
    assert isinstance(converted['field1']['field2'], dict)
    assert isinstance(converted['field1']['field2']['field3'], dict)
    assert isinstance(converted['field1']['field2']['field3']['field4'], str)
    assert converted['field1']['field2']['field3']['field4'] == 'val'


def test_list_is_named_list():
    l = dict_to_objdict({
        'list': [
            {
                'name': 'name1',
                'value': 'value1'
            },
            {
                'name': 'name2',
                'value': 'value2'
            }
        ]
    })

    assert is_named_list(l['list'])


def test_list_is_not_named_list():
    l = dict_to_objdict({
        'list': [
            {
                'name': 'name1',
                'value': 'value1'
            },
            {
                'value': 'value2'
            }
        ]
    })

    assert is_named_list(l['list']) is False


def test_assert_unique_names_in_named_list():
    l = dict_to_objdict({
        'list': [
            {
                'name': 'name1',
                'value': 'value1'
            },
            {
                'name': 'name1',
                'value': 'value2'
            }
        ]
    })
    with pytest.raises(DuplicatesInNamedListException):
        assert_unique_names_in_named_list(l['list'], 'list', 'input')


def test_dict_merge_adds_key_when_is_missing():
    base = dict_to_objdict({'field1': 'test1', 'field2': 'val'})
    extend_by = dict_to_objdict({'field3': 'test3', 'field4': 'test4'})
    merge_objdict(base, extend_by)

    assert base.field3 == 'test3'
    assert base.field4 == 'test4'


def test_dict_merge_updates_value_when_same_key_exists():
    base = dict_to_objdict({'field1': 'test1', 'field2': 'val'})
    extend_by = dict_to_objdict({'field1': 'test22'})
    merge_objdict(base, extend_by)

    assert base.field1 == 'test22'
    assert base.field2 == 'val'


def test_dict_merge_asserts_on_different_types():
    base = dict_to_objdict({
        'field1': 'test1' # string type
    })
    extend_by = dict_to_objdict({
        'field1': 1 # integer type
    })
    with pytest.raises(TypeMismatchException):
        merge_objdict(base, extend_by)


def test_dict_merge_updates_nested_object():
    base = dict_to_objdict({'field1': 'test1',
            'complex1':
                {'nested_field1': 'nested_val1',
                 'nested_field2': 'nested_val2'}
            })
    extend_by = dict_to_objdict({'complex1':
                     {'nested_field1': 'nested_val3',
                      'nested_field2': 'nested_val4'}
                 })
    merge_objdict(base, extend_by)

    assert base.field1 == 'test1'
    assert base.complex1.nested_field1 == 'nested_val3'
    assert base.complex1.nested_field2 == 'nested_val4'


def test_dict_merge_add_field_to_nested_object():
    base = dict_to_objdict({'field1': 'test1',
            'complex1':
                {'nested_field1': 'nested_val1',
                 'nested_field2': 'nested_val2'}
            })
    extend_by = dict_to_objdict({'complex1':
                     {'nested_field1': 'nested_val3',
                      'nested_field2': 'nested_val4',
                      'nested_field3': 'nested_val5'}
                 })
    merge_objdict(base, extend_by)

    assert base.field1 == 'test1'
    assert base.complex1.nested_field1 == 'nested_val3'
    assert base.complex1.nested_field2 == 'nested_val4'
    assert base.complex1.nested_field3 == 'nested_val5'


def test_dict_merge_replaces_list_of_strings_when_same_key_exists():
    base = dict_to_objdict({'field1': 'test1', 'list': ['base1', 'base2', 'base3']})
    extend_by = dict_to_objdict({'list': ['replaced1', 'replaced2']})
    merge_objdict(base, extend_by)

    assert base.field1 == 'test1'
    assert base.list == ['replaced1', 'replaced2']


def test_dict_overwrite_named_list_in_undefined_merge_mode():
    base = dict_to_objdict({
        'field1': 'test1',
        'list': [
            {
                'name': 'test1',
                'value': 'base1'
            },
            {
                'name': 'test2',
                'value': 'base2'
            }
        ]
    })
    extend_by = dict_to_objdict({
        'list': [
            {
                'name': 'test3',
                'value': 'extend3'
            }
        ]
    })
    merge_objdict(base, extend_by)

    assert base.field1 == 'test1'
    assert base.list == [
            {
                'name': 'test3',
                'value': 'extend3'
            }  ]


def test_dict_overwrite_named_list_in_overwrite_mode():
    base = dict_to_objdict({
        'field1': 'test1',
        'list': [
            {
                'name': 'test1',
                'value': 'base1'
            },
            {
                'name': 'test2',
                'value': 'base2'
            }
        ]
    })
    extend_by = dict_to_objdict({
        'list': [
            {
                '_merge': False
            },
            {
                'name': 'test3',
                'value': 'extend3'
            }
        ]
    })
    merge_objdict(base, extend_by)

    assert base.field1 == 'test1'
    assert base.list == [
            {
                'name': 'test3',
                'value': 'extend3'
            }  ]


def test_dict_merge_updates_named_list_when_same_name_key_exists_in_merge_mode():
    base = dict_to_objdict({
        'field1': 'test1',
        'list': [
            {
                'name': 'test1',
                'value': 'base1'
            },
            {
                'name': 'test2',
                'value': 'base2'
            }
        ]
    })
    extend_by = dict_to_objdict({
        'list': [
            {
                '_merge': True
            },
            {
                'name': 'test2',
                'value': 'base_new'
            }
        ]
    })
    merge_objdict(base, extend_by)

    assert base.field1 == 'test1'
    assert base.list == [
            {
                'name': 'test1',
                'value': 'base1'
            },
            {
                'name': 'test2',
                'value': 'base_new'
            }]


def test_dict_merge_extends_named_list_with_new_key_in_merge_mode():
    base = dict_to_objdict({
        'field1': 'test1',
        'list': [
            {
                'name': 'test1',
                'value': 'base1'
            },
            {
                'name': 'test2',
                'value': 'base2'
            }
        ]
    })
    extend_by = dict_to_objdict({
        'list': [
            {
                '_merge': True
            },
            {
                'name': 'test3',
                'value': 'extend3'
            }
        ]
    })
    merge_objdict(base, extend_by)

    assert base.field1 == 'test1'
    assert base.list == [
            {
                'name': 'test1',
                'value': 'base1'
            },
            {
                'name': 'test2',
                'value': 'base2'
            },
            {
                'name': 'test3',
                'value': 'extend3'
            }]


def test_dict_merge_asserts_on_base_named_list_with_duplicate_name_in_merge_mode():
    base = dict_to_objdict({
        'list': [
            {
                'name': 'test1',
                'value': 'base1'
            },
            {
                'name': 'test1',
                'value': 'base2'
            }
        ]
    })
    extend_by = dict_to_objdict({
        'list': [
            {
                '_merge': True
            },
            {
                'name': 'test3',
                'value': 'extend3'
            }
        ]
    })
    with pytest.raises(DuplicatesInNamedListException):
        merge_objdict(base, extend_by)


def test_dict_merge_asserts_on_extend_named_list_with_duplicate_name_in_merge_mode():
    base = dict_to_objdict({
        'list': [
            {
                'name': 'test1',
                'value': 'base1'
            }
        ]
    })
    extend_by = dict_to_objdict({
        'list': [
            {
                '_merge': True
            },
            {
                'name': 'test2',
                'value': 'extend2'
            },
            {
                'name': 'test2',
                'value': 'extend3'
            }
        ]
    })
    with pytest.raises(DuplicatesInNamedListException):
        merge_objdict(base, extend_by)


def test_dict_atrribute_asserts_on_unknown_merge_mode():
    base = dict_to_objdict({
        'list': [
            {
                'name': 'test1',
                'value': 'base1'
            }
        ]
    })
    extend_by = dict_to_objdict({
        'list': [
            {
                '_merge': 'string' # String instead of boolean
            },
            {
                'name': 'test2',
                'value': 'extend2'
            },
        ]
    })
    with pytest.raises(AttributeError):
        merge_objdict(base, extend_by)


def test_replace_yesno_with_boolean_true_values():
    objdict = ObjDict({
        'field1': ObjDict({
            'field2': ObjDict({
                'value1': 'y',
                'value2': 'Y',
                'value3': 'yes',
                'value4': 'Yes',
                'value5': 'YES',
            })
        })
    })

    replace_yesno_with_booleans(objdict)

    assert objdict.field1.field2.value1 is True
    assert objdict.field1.field2.value2 is True
    assert objdict.field1.field2.value3 is True
    assert objdict.field1.field2.value4 is True
    assert objdict.field1.field2.value5 is True


def test_replace_yesno_with_boolean_false_values():
    objdict = ObjDict({
        'field1': ObjDict({
            'field2': ObjDict({
                'value1': 'n',
                'value2': 'N',
                'value3': 'no',
                'value4': 'No',
                'value5': 'NO',
            })
        })
    })

    replace_yesno_with_booleans(objdict)

    assert objdict.field1.field2.value1 is False
    assert objdict.field1.field2.value2 is False
    assert objdict.field1.field2.value3 is False
    assert objdict.field1.field2.value4 is False
    assert objdict.field1.field2.value5 is False
