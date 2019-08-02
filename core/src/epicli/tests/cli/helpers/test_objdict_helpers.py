from cli.helpers.objdict_helpers import merge_objdict, dict_to_objdict, objdict_to_dict
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

    assert type(converted) is ObjDict
    assert type(converted.field1) is ObjDict
    assert type(converted.field1.field2) is ObjDict
    assert type(converted.field1.field2.field3) is ObjDict
    assert type(converted.field1.field2.field3.field4) is str
    assert converted.field1.field2.field3.field4 == 'val'


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

    assert type(converted) is dict
    assert type(converted['field1']) is dict
    assert type(converted['field1']['field2']) is dict
    assert type(converted['field1']['field2']['field3']) is dict
    assert type(converted['field1']['field2']['field3']['field4']) is str
    assert converted['field1']['field2']['field3']['field4'] == 'val'


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


def test_dict_merge_replaces_list_when_same_key_exists():
    base = dict_to_objdict({'field1': 'test1', 'list': ['base1', 'base2', 'base3']})
    extend_by = dict_to_objdict({'list': ['replaced1', 'replaced2']})
    merge_objdict(base, extend_by)

    assert base.field1 == 'test1'
    assert base.list == ['replaced1', 'replaced2']


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
