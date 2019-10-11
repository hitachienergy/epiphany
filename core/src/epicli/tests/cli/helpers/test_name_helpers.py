from cli.helpers.naming_helpers import to_role_name, to_feature_name, resource_name, cluster_tag, storage_account_name


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


def test_storage_account_name_no_prefix1():
    actual = storage_account_name('default', 'Cluster', 'use')
    assert actual == "clusteruse"


def test_storage_account_name_no_prefix2():
    actual = storage_account_name('', 'Cluster', 'use')
    assert actual == "clusteruse"  


def test_storage_account_name_no_prefix3():
    actual = storage_account_name(None, 'Cluster', 'use')
    assert actual == "clusteruse"    


def test_storage_account_short():
    actual = storage_account_name('Prefix', 'Cluster', 'Use')
    assert actual == "prefixclusteruse"   


def test_storage_account_long():
    actual = storage_account_name('Prefix', 'SuperLongClusterName', 'SuperLongUse')
    assert len(actual) == 24
    assert actual == "prefixsuperlongclussuper"            

