from cli.helpers.naming_helpers import to_role_name


def test_replaces_all_hyphens_in_variable():

    actual = to_role_name("infrastructure/route-table-association")

    assert actual == "infrastructure/route_table_association"
