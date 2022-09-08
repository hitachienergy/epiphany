from io import StringIO

from pytest_mock import MockerFixture

from cli.src.helpers.objdict_helpers import dict_to_objdict
from cli.src.helpers.yaml_helpers import safe_load_all
from cli.src.schema.ManifestHandler import ManifestHandler
from tests.unit.data.schema.ManifestReader_data import (
    EXPECTED_PARSED_MANIFEST_DOCS,
    EXPECTED_UPDATED_DOC_BASE,
    EXPECTED_UPDATED_DOC_WITH_NEW_DOC_ADDED,
    EXPECTED_UPDATED_DOC_WITH_TWO_INFRA_DOCS,
    INPUT_DOC_TO_UPDATE_BASE,
    INPUT_DOC_TO_UPDATE_TWO_INFRA_DOCS,
    INPUT_MANIFEST_DOCS
)
from tests.unit.mocks.StreamMock import StreamMock


def test_read_manifest(mocker: MockerFixture):
    mocker.patch('cli.src.schema.ManifestHandler.load_yamls_file', return_value=safe_load_all(StringIO(INPUT_MANIFEST_DOCS)))
    mocker.patch('cli.src.schema.ManifestHandler.Path.exists', return_value=True)

    mhandler = ManifestHandler(cluster_name='cluster')
    mhandler.read_manifest()

    assert mhandler.docs == EXPECTED_PARSED_MANIFEST_DOCS


def test_write_manifest(mocker: MockerFixture):
    stream = StreamMock()
    mocker.patch('cli.src.schema.ManifestHandler.Path.open', return_value=stream)

    mhandler = ManifestHandler(cluster_name='cluster')
    mhandler.add_docs(EXPECTED_PARSED_MANIFEST_DOCS)
    mhandler.write_manifest()

    assert stream.data == INPUT_MANIFEST_DOCS


def test_update_doc_existing():
    """
    Test update_doc() method by using same doc with changed `specification/field` value.
    """
    mhandler = ManifestHandler(cluster_name='cluster')
    mhandler.add_docs(INPUT_DOC_TO_UPDATE_TWO_INFRA_DOCS)

    doc = {
        'kind': 'infrastructure/virtual-machine',
        'title': 'Some infrastructure doc',
        'provider': 'azure',
        'name': 'some-machine',
        'specification': {
            'field': True,
        },
        'version': '2.0.1dev'}

    mhandler.update_doc(doc)

    assert mhandler.docs == EXPECTED_UPDATED_DOC_WITH_TWO_INFRA_DOCS


def test_update_doc_non_existing():
    """
    Test update_doc() method by adding second document with the same `kind`.
    """
    mhandler = ManifestHandler(cluster_name='cluster')
    mhandler.add_docs(INPUT_DOC_TO_UPDATE_BASE)

    doc = {
        'kind': 'infrastructure/virtual-machine',
        'title': 'Some infrastructure doc',
        'provider': 'azure',
        'name': 'some-machine',
        'specification': {
            'field': True,
        },
        'version': '2.0.1dev'}

    mhandler.update_doc(doc)

    assert mhandler.docs == EXPECTED_UPDATED_DOC_WITH_TWO_INFRA_DOCS


def test_update_doc_new_doc_added():
    """
    Test update_doc() method by adding document with new `kind`.
    """
    mhandler = ManifestHandler(cluster_name='cluster')
    mhandler.add_docs(INPUT_DOC_TO_UPDATE_BASE)

    doc = {'kind': 'some/other',
           'title': 'Some other doc',
           'provider': 'azure',
           'version': '2.0.1dev'}

    mhandler.update_doc(doc)

    assert mhandler.docs == EXPECTED_UPDATED_DOC_WITH_NEW_DOC_ADDED
