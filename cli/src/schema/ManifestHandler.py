from collections import defaultdict
from itertools import chain
from pathlib import Path
from typing import Union

from cli.src.helpers.ObjDict import ObjDict
from cli.src.helpers.build_io import get_build_path
from cli.src.helpers.data_loader import load_yamls_file
from cli.src.helpers.objdict_helpers import dict_to_objdict, objdict_to_dict
from cli.src.helpers.yaml_helpers import dump_all


class ManifestHandler:
    """
    An Interface for manifest file used in epicli cluster configuration.

    Data is stored in a form of:
        dict[str, list[dict]]

    where:
    - `key` is document's `kind` attribute
    - `value` is a list of documents matching the `kind`
    """

    def __init__(self, build_path: Path = None, cluster_name: str = '', input_file: Path = None):
        """
        Handler can by constructed by providing any of the arguments:

        :param build_path: path to the build directory with manifest file
        :param cluster_name: target cluster name used by the epicli configuration
        :param input_file: path to manifest file provided by the `-f|--file` argument
        """
        self.__build_path: Path
        self.__manifest_file_path: Path
        self.__docs: dict[str, list[dict]] = defaultdict(list)

        if not input_file:
            self.__build_path = Path(get_build_path(cluster_name)) if cluster_name else Path(build_path)
            self.__manifest_file_path = self.__build_path / 'manifest.yml'
        else:
            self.__manifest_file_path = input_file.absolute()
            self.__build_path = self.__manifest_file_path.parent

    def __getitem__(self, doc_name: str) -> ObjDict:
        return dict_to_objdict(self.__docs[doc_name])

    @property
    def manifest_path(self) -> Path:
        return self.__manifest_file_path

    @property
    def docs(self) -> list[ObjDict]:
        return [dict_to_objdict(doc) for doc in chain(*self.__docs.values())]

    @property
    def infra_docs(self) -> list[ObjDict]:
        return [dict_to_objdict(doc) for doc in chain(*self.__docs.values()) if doc['kind'].startswith('infrastructure')]

    @property
    def cluster_model(self) -> dict:
        return dict_to_objdict(self.__docs['epiphany-cluster'][0])

    @property
    def cluster_name(self) -> str:
        return self.__docs['epiphany-cluster'][0].specification.name

    def exists(self) -> bool:
        return self.__manifest_file_path.exists()

    def update_doc(self, doc: Union[dict, ObjDict]):
        """
        Try to update the document with matching `kind` and `name`.
        If the document does not exist add a new one.

        :param doc: document that will be updated/added
        """
        docs = self.__docs[doc['kind']]  # defaultdict will not raise an error

        for doc_idx, _ in enumerate(docs):
            if docs[doc_idx]['name'] == doc['name']:
                docs[doc_idx] = doc
                return

        self.add_doc(doc)  # no document found with matching kind/name, add it

    def update_docs(self, docs: list[Union[dict, ObjDict]]):
        for doc in docs:
            self.update_doc(doc)

    def add_doc(self, doc: Union[dict, ObjDict]):
        self.__docs[doc['kind']].append(objdict_to_dict(doc))

    def add_docs(self, docs: list[Union[dict, ObjDict]]):
        for doc in docs:
            self.add_doc(doc)

    def get_selected_components(self) -> set:
        """
        Return components used in the manifest.
        """
        components_doc = self.__docs['epiphany-cluster'][0]['specification']['components']
        return {component for component in components_doc if components_doc[component]['count'] > 0}

    def get_selected_features(self) -> set:
        """
        Return only features that have existing components.
        """
        features_doc = self.__docs['configuration/feature-mappings'][0]['specification']['mappings']
        selected_features: set = set()
        for component in self.get_selected_components():
            for feature in features_doc[component]:
                selected_features.add(feature)
        return selected_features

    def write_manifest(self, file_name: str = ''):
        """
        Create the manifest file by merging all of the docs.

        :param file_name: optional file name instead default one
        """
        manifest_path = self.__build_path / f'{file_name}.yml' if file_name else self.__manifest_file_path
        with manifest_path.open(mode='w', encoding='utf-8') as stream:
            dump_all(list(chain(*self.__docs.values())), stream)

    def read_manifest(self):
        """
        Read all the docs from the manifest file.
        """
        if not self.__manifest_file_path.exists():
            raise Exception('No manifest.yml inside the build folder')

        docs: list[dict] = load_yamls_file(self.__manifest_file_path)
        for doc in docs:
            self.__docs[doc['kind']].append(doc)
