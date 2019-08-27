from cli.helpers.naming_helpers import to_role_name, to_feature_name, resource_name


def test_to_role_name():
    actual = to_role_name("infrastructure/route-table-association")
    assert actual == "infrastructure/route_table_association"


def test_to_feature_name():
    actual = to_feature_name("route_table_association")
    assert actual == "route-table-association"


def test_resource_name_cn_rt():
    actual = resource_name('default', 'Cluster', 'Type')
    assert actual == "cluster-type"


def test_resource_name_pr_cn_rt():
    actual = resource_name('prefix', 'Cluster', 'Type')
    assert actual == "prefix-cluster-type"


def test_resource_name_cn_rt_cmp():
    actual = resource_name('default', 'Cluster', 'Type', component='Component')
    assert actual == "cluster-component-type"


def test_resource_name_pr_cn_rt_cmp():
    actual = resource_name('prefix', 'Cluster', 'Type', component='Component')
    assert actual == "prefix-cluster-component-type"

