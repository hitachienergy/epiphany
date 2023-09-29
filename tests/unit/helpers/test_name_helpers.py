from cli.src.helpers.naming_helpers import (cluster_tag, resource_name,
                                            to_feature_name, to_role_name)


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


def test_cluster_tag_no_prefix1():
    actual = cluster_tag('default', 'Cluster')
    assert actual == "cluster"


def test_cluster_tag_no_prefix2():
    actual = cluster_tag('', 'Cluster')
    assert actual == "cluster"


def test_cluster_tag_no_prefix3():
    actual = cluster_tag(None, 'Cluster')
    assert actual == "cluster"


def test_cluster_tag():
    actual = cluster_tag('prefix', 'Cluster')
    assert actual == "prefix-cluster"
