from cli.helpers.ObjDict import ObjDict
import pytest


obj = ObjDict({'read': 1, 'set_existing_field': 1, 'delete_existing_field': 1})


def test_objdict_access_existing_field():
    assert obj.read == 1
    assert obj['read'] == 1


def test_objdict_access_non_existing_field_exception():
    with pytest.raises(AttributeError) as excinfo:
        obj.non_existing
    assert 'No such attribute: non_existing' in str(excinfo.value)


def test_objdict_set_existing_field():
    assert obj.set_existing_field == 1
    assert obj['set_existing_field'] == 1

    obj.set_existing_field = 2

    assert obj.set_existing_field == 2
    assert obj['set_existing_field'] == 2

def test_objdict_set_non_existing_field_as_member():
    with pytest.raises(AttributeError) as excinfo:
        obj.set_non_existing_field_as_member
    assert 'No such attribute: set_non_existing_field_as_member' in str(excinfo.value)

    obj.set_non_existing_field_as_member = 1

    assert obj.set_non_existing_field_as_member == 1
    assert obj['set_non_existing_field_as_member'] == 1

def test_objdict_set_non_existing_field_as_dict_entry():
    with pytest.raises(AttributeError) as excinfo:
        obj.set_non_existing_field_as_dict_entry
    assert 'No such attribute: set_non_existing_field_as_dict_entry' in str(excinfo.value)

    obj['set_non_existing_field_as_dict_entry'] = 1

    assert obj.set_non_existing_field_as_member == 1
    assert obj['set_non_existing_field_as_member'] == 1


def test_objdict_delete_non_existing_field_exception():
    with pytest.raises(AttributeError) as excinfo:
        del(obj.non_existing)
    assert 'No such attribute: non_existing' in str(excinfo.value)


def test_objdict_delete_existing_field():
    assert obj.delete_existing_field == 1

    del(obj.delete_existing_field)

    with pytest.raises(AttributeError) as excinfo:
        obj.delete_existing_field
    assert 'No such attribute: delete_existing_field' in str(excinfo.value)







