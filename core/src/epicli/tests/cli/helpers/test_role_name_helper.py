from cli.helpers.role_name_helper import adjust_name


def test_replaces_all_hyphens_in_variable():

    actual = adjust_name("infrastructure/route-table-association")

    assert actual == "infrastructure/route_table_association"
